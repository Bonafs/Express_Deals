from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils import timezone
import stripe
import json
import logging

from orders.models import Order
from .models import Payment, StripeWebhookEvent

# Configure logging
logger = logging.getLogger(__name__)

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(LoginRequiredMixin, View):
    """
    Create Stripe Payment Intent and render payment page
    """
    template_name = 'payments/payment.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Check if order is already paid
        if order.payment_status == 'paid':
            messages.info(request, 'This order has already been paid.')
            return redirect('orders:order_detail', pk=order.id)
        
        try:
            # Create or get existing payment intent
            payment, created = Payment.objects.get_or_create(
                order=order,
                user=request.user,
                defaults={
                    'amount': order.total,
                    'status': 'pending',
                    'payment_method': 'stripe',
                }
            )
            
            # Create Stripe Payment Intent
            if not payment.stripe_payment_intent_id:
                intent = stripe.PaymentIntent.create(
                    amount=int(order.total * 100),  # Convert to cents
                    currency='usd',
                    metadata={
                        'order_id': order.id,
                        'payment_id': payment.id,
                        'user_id': request.user.id,
                    },
                    automatic_payment_methods={
                        'enabled': True,
                    },
                )
                
                payment.stripe_payment_intent_id = intent.id
                payment.save()
            else:
                # Retrieve existing payment intent
                intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)
            
            context = {
                'order': order,
                'payment': payment,
                'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
                'client_secret': intent.client_secret,
            }
            
            return render(request, self.template_name, context)
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {str(e)}")
            messages.error(request, 'There was an error processing your payment. Please try again.')
            return redirect('orders:cart')
        except Exception as e:
            logger.error(f"Error in PaymentView: {str(e)}")
            messages.error(request, 'An unexpected error occurred. Please try again.')
            return redirect('orders:cart')


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    """
    Display payment success page
    """
    template_name = 'payments/payment_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get payment intent ID from URL parameters
        payment_intent_id = self.request.GET.get('payment_intent')
        
        if payment_intent_id:
            try:
                payment = Payment.objects.get(
                    stripe_payment_intent_id=payment_intent_id,
                    user=self.request.user
                )
                context['order'] = payment.order
                context['payment'] = payment
            except Payment.DoesNotExist:
                messages.error(self.request, 'Payment not found.')
        
        return context


class PaymentCancelView(LoginRequiredMixin, TemplateView):
    """
    Display payment cancellation page
    """
    template_name = 'payments/payment_cancel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get payment intent ID from URL parameters
        payment_intent_id = self.request.GET.get('payment_intent')
        
        if payment_intent_id:
            try:
                payment = Payment.objects.get(
                    stripe_payment_intent_id=payment_intent_id,
                    user=self.request.user
                )
                context['order'] = payment.order
                context['payment'] = payment
            except Payment.DoesNotExist:
                pass
        
        return context


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """
    Handle Stripe webhook events
    """
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            logger.error("Invalid payload in Stripe webhook")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid signature in Stripe webhook")
            return HttpResponse(status=400)
        
        # Store webhook event
        webhook_event, created = StripeWebhookEvent.objects.get_or_create(
            stripe_event_id=event['id'],
            defaults={
                'event_type': event['type'],
                'data': event['data'],
            }
        )
        
        if not created and webhook_event.processed:
            return HttpResponse(status=200)
        
        # Handle the event
        try:
            if event['type'] == 'payment_intent.succeeded':
                self._handle_payment_succeeded(event['data']['object'])
            elif event['type'] == 'payment_intent.payment_failed':
                self._handle_payment_failed(event['data']['object'])
            elif event['type'] == 'charge.dispute.created':
                self._handle_dispute_created(event['data']['object'])
            else:
                logger.info(f"Unhandled event type: {event['type']}")
            
            # Mark webhook as processed
            webhook_event.processed = True
            webhook_event.save()
            
        except Exception as e:
            logger.error(f"Error processing webhook {event['id']}: {str(e)}")
            return HttpResponse(status=500)
        
        return HttpResponse(status=200)
    
    def _handle_payment_succeeded(self, payment_intent):
        """Handle successful payment"""
        try:
            with transaction.atomic():
                payment = Payment.objects.get(
                    stripe_payment_intent_id=payment_intent['id']
                )
                
                # Update payment status
                payment.status = 'succeeded'
                payment.completed_at = timezone.now()
                payment.gateway_response = payment_intent
                payment.save()
                
                # Update order status
                order = payment.order
                order.payment_status = 'paid'
                order.status = 'processing'
                order.stripe_payment_intent_id = payment_intent['id']
                order.save()
                
                logger.info(f"Payment succeeded for order {order.order_number}")
                
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for payment_intent {payment_intent['id']}")
        except Exception as e:
            logger.error(f"Error handling payment success: {str(e)}")
    
    def _handle_payment_failed(self, payment_intent):
        """Handle failed payment"""
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            
            payment.status = 'failed'
            payment.gateway_response = payment_intent
            payment.save()
            
            # Update order status
            order = payment.order
            order.payment_status = 'failed'
            order.save()
            
            logger.info(f"Payment failed for order {order.order_number}")
            
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for payment_intent {payment_intent['id']}")
        except Exception as e:
            logger.error(f"Error handling payment failure: {str(e)}")
    
    def _handle_dispute_created(self, charge):
        """Handle dispute/chargeback creation"""
        try:
            # Find payment by charge ID
            payment_intent_id = charge.get('payment_intent')
            if payment_intent_id:
                payment = Payment.objects.get(
                    stripe_payment_intent_id=payment_intent_id
                )
                
                # Update order status
                order = payment.order
                order.status = 'disputed'
                order.save()
                
                logger.warning(f"Dispute created for order {order.order_number}")
                
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for disputed charge {charge['id']}")
        except Exception as e:
            logger.error(f"Error handling dispute: {str(e)}")


class RefundView(LoginRequiredMixin, View):
    """
    Process refund requests (admin only)
    """
    
    def post(self, request, order_id):
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to process refunds.')
            return redirect('orders:order_detail', pk=order_id)
        
        order = get_object_or_404(Order, id=order_id)
        
        try:
            # Get the successful payment
            payment = order.payments.filter(status='succeeded').first()
            
            if not payment:
                messages.error(request, 'No successful payment found for this order.')
                return redirect('orders:order_detail', pk=order_id)
            
            # Create refund in Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.stripe_payment_intent_id,
                reason='requested_by_customer',
            )
            
            # Create refund record
            from .models import Refund
            Refund.objects.create(
                payment=payment,
                order=order,
                user=order.user,
                amount=payment.amount,
                reason='requested_by_customer',
                status='succeeded',
                stripe_refund_id=refund.id,
                processed_by=request.user,
            )
            
            # Update order status
            order.payment_status = 'refunded'
            order.status = 'refunded'
            order.save()
            
            messages.success(request, f'Refund processed successfully for order {order.order_number}.')
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error processing refund: {str(e)}")
            messages.error(request, f'Error processing refund: {str(e)}')
        except Exception as e:
            logger.error(f"Error processing refund: {str(e)}")
            messages.error(request, 'An unexpected error occurred while processing the refund.')
        
        return redirect('orders:order_detail', pk=order_id)
