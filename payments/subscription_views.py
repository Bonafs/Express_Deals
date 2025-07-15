"""
Express Deals - Subscription Management Views
Handle subscription creation, management, and billing
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import stripe
import json
import logging

from .models import SubscriptionPlan, Subscription, StripeCustomer, Payment
from .stripe_service import stripe_service

logger = logging.getLogger(__name__)

@login_required
def subscription_plans(request):
    """Display available subscription plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True)
    user_subscription = None
    
    # Check if user has an active subscription
    try:
        customer = StripeCustomer.objects.get(user=request.user)
        user_subscription = Subscription.objects.filter(
            user=request.user, 
            status__in=['active', 'trialing']
        ).first()
    except StripeCustomer.DoesNotExist:
        pass
    
    context = {
        'plans': plans,
        'user_subscription': user_subscription,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments/subscription_plans.html', context)

@login_required
@require_http_methods(["POST"])
def create_subscription(request):
    """Create a new subscription"""
    try:
        plan_id = request.POST.get('plan_id')
        payment_method_id = request.POST.get('payment_method_id')
        
        if not plan_id:
            messages.error(request, "No subscription plan selected.")
            return redirect('subscription_plans')
        
        plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
        
        # Get or create Stripe customer
        customer = stripe_service.get_or_create_customer(request.user)
        
        # Store customer reference in Django
        stripe_customer, created = StripeCustomer.objects.get_or_create(
            user=request.user,
            defaults={'stripe_customer_id': customer.id}
        )
        
        # Create subscription
        subscription = stripe_service.create_subscription(
            customer=customer,
            price_id=plan.stripe_price_id,
            trial_period_days=plan.trial_period_days,
            metadata={
                'user_id': request.user.id,
                'plan_id': plan.id,
                'django_user': request.user.username
            }
        )
        
        # Store subscription in Django
        django_subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            stripe_subscription_id=subscription.id,
            stripe_customer_id=customer.id,
            status=subscription.status,
            current_period_start=timezone.datetime.fromtimestamp(subscription.current_period_start),
            current_period_end=timezone.datetime.fromtimestamp(subscription.current_period_end),
            trial_end=timezone.datetime.fromtimestamp(subscription.trial_end) if subscription.trial_end else None
        )
        
        # Create payment record
        Payment.objects.create(
            user=request.user,
            amount=plan.price,
            currency=plan.currency,
            payment_type='subscription',
            status='pending',
            description=f'Subscription: {plan.name}',
            stripe_subscription_id=subscription.id,
            subscription=django_subscription,
            metadata={'plan_name': plan.name}
        )
        
        # Return client secret for payment confirmation
        if subscription.latest_invoice and subscription.latest_invoice.payment_intent:
            client_secret = subscription.latest_invoice.payment_intent.client_secret
            return JsonResponse({
                'client_secret': client_secret,
                'subscription_id': subscription.id
            })
        
        messages.success(request, f"Successfully subscribed to {plan.name}!")
        return redirect('subscription_dashboard')
        
    except Exception as e:
        logger.error(f"Subscription creation failed: {e}")
        messages.error(request, "Failed to create subscription. Please try again.")
        return redirect('subscription_plans')

@login_required
def subscription_dashboard(request):
    """User's subscription management dashboard"""
    try:
        customer = StripeCustomer.objects.get(user=request.user)
        subscriptions = Subscription.objects.filter(user=request.user).order_by('-created_at')
        payments = Payment.objects.filter(
            user=request.user, 
            payment_type='subscription'
        ).order_by('-created_at')[:10]
        
        context = {
            'subscriptions': subscriptions,
            'payments': payments,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(request, 'payments/subscription_dashboard.html', context)
        
    except StripeCustomer.DoesNotExist:
        return redirect('subscription_plans')

@login_required
@require_http_methods(["POST"])
def cancel_subscription(request):
    """Cancel a subscription"""
    try:
        subscription_id = request.POST.get('subscription_id')
        at_period_end = request.POST.get('at_period_end', 'true').lower() == 'true'
        
        subscription = get_object_or_404(
            Subscription, 
            id=subscription_id, 
            user=request.user
        )
        
        # Cancel in Stripe
        stripe_subscription = stripe_service.cancel_subscription(
            subscription.stripe_subscription_id,
            at_period_end=at_period_end
        )
        
        # Update Django record
        subscription.cancel_at_period_end = at_period_end
        if not at_period_end:
            subscription.status = 'canceled'
            subscription.canceled_at = timezone.now()
        subscription.save()
        
        if at_period_end:
            messages.success(request, "Subscription will be canceled at the end of the current period.")
        else:
            messages.success(request, "Subscription canceled immediately.")
        
        return redirect('subscription_dashboard')
        
    except Exception as e:
        logger.error(f"Subscription cancellation failed: {e}")
        messages.error(request, "Failed to cancel subscription. Please try again.")
        return redirect('subscription_dashboard')

@login_required
@require_http_methods(["POST"])
def update_subscription(request):
    """Update subscription plan"""
    try:
        subscription_id = request.POST.get('subscription_id')
        new_plan_id = request.POST.get('new_plan_id')
        
        subscription = get_object_or_404(
            Subscription, 
            id=subscription_id, 
            user=request.user
        )
        
        new_plan = get_object_or_404(SubscriptionPlan, id=new_plan_id, is_active=True)
        
        # Update in Stripe
        stripe_subscription = stripe_service.update_subscription(
            subscription.stripe_subscription_id,
            new_price_id=new_plan.stripe_price_id
        )
        
        # Update Django record
        subscription.plan = new_plan
        subscription.save()
        
        messages.success(request, f"Subscription updated to {new_plan.name}!")
        return redirect('subscription_dashboard')
        
    except Exception as e:
        logger.error(f"Subscription update failed: {e}")
        messages.error(request, "Failed to update subscription. Please try again.")
        return redirect('subscription_dashboard')

# ===== MANUAL PAYMENTS =====

@login_required
def manual_payment(request):
    """Create a manual one-time payment"""
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 0))
            description = request.POST.get('description', 'Manual Payment')
            
            if amount <= 0:
                messages.error(request, "Please enter a valid amount.")
                return render(request, 'payments/manual_payment.html')
            
            # Get or create customer
            customer = stripe_service.get_or_create_customer(request.user)
            
            # Create payment intent
            intent = stripe_service.create_payment_intent(
                amount=amount,
                customer=customer,
                description=description,
                metadata={
                    'user_id': request.user.id,
                    'payment_type': 'manual',
                    'django_user': request.user.username
                }
            )
            
            # Create payment record
            Payment.objects.create(
                user=request.user,
                amount=amount,
                currency='GBP',
                payment_type='one_time',
                status='pending',
                description=description,
                stripe_payment_intent_id=intent.id
            )
            
            return JsonResponse({
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            })
            
        except Exception as e:
            logger.error(f"Manual payment creation failed: {e}")
            messages.error(request, "Failed to create payment. Please try again.")
    
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments/manual_payment.html', context)

# ===== RECURRING PAYMENTS (Invoice-based) =====

@login_required
def setup_recurring_payment(request):
    """Set up recurring invoice-based payments"""
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 0))
            frequency = request.POST.get('frequency', 'monthly')
            description = request.POST.get('description', 'Recurring Payment')
            
            if amount <= 0:
                messages.error(request, "Please enter a valid amount.")
                return render(request, 'payments/recurring_payment.html')
            
            # Get or create customer
            customer = stripe_service.get_or_create_customer(request.user)
            
            # Calculate next payment date
            from datetime import datetime, timedelta
            next_payment = datetime.now()
            if frequency == 'weekly':
                next_payment += timedelta(weeks=1)
            elif frequency == 'monthly':
                next_payment += timedelta(days=30)
            elif frequency == 'quarterly':
                next_payment += timedelta(days=90)
            elif frequency == 'yearly':
                next_payment += timedelta(days=365)
            
            # Create recurring payment record
            from .models import RecurringPayment
            recurring_payment = RecurringPayment.objects.create(
                user=request.user,
                amount=amount,
                currency='GBP',
                description=description,
                frequency=frequency,
                next_payment_date=next_payment,
                stripe_customer_id=customer.id
            )
            
            messages.success(request, f"Recurring payment set up successfully! Next payment: {next_payment.strftime('%B %d, %Y')}")
            return redirect('recurring_payments_dashboard')
            
        except Exception as e:
            logger.error(f"Recurring payment setup failed: {e}")
            messages.error(request, "Failed to set up recurring payment. Please try again.")
    
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payments/recurring_payment.html', context)

@login_required
def recurring_payments_dashboard(request):
    """Dashboard for managing recurring payments"""
    from .models import RecurringPayment
    recurring_payments = RecurringPayment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'recurring_payments': recurring_payments
    }
    return render(request, 'payments/recurring_dashboard.html', context)

# ===== WEBHOOK HANDLING =====

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe_service.construct_webhook_event(payload, sig_header)
    except ValueError:
        logger.error("Invalid payload in webhook")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in webhook")
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        handle_successful_payment(event['data']['object'])
    elif event['type'] == 'invoice.payment_failed':
        handle_failed_payment(event['data']['object'])
    elif event['type'] == 'customer.subscription.updated':
        handle_subscription_updated(event['data']['object'])
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    else:
        logger.info(f"Unhandled event type: {event['type']}")
    
    return HttpResponse(status=200)

def handle_successful_payment(invoice):
    """Handle successful payment webhook"""
    try:
        # Update payment record
        if invoice.get('payment_intent'):
            Payment.objects.filter(
                stripe_payment_intent_id=invoice['payment_intent']
            ).update(status='succeeded')
        
        # Update subscription if applicable
        if invoice.get('subscription'):
            Subscription.objects.filter(
                stripe_subscription_id=invoice['subscription']
            ).update(status='active')
            
        logger.info(f"Handled successful payment for invoice {invoice['id']}")
        
    except Exception as e:
        logger.error(f"Error handling successful payment: {e}")

def handle_failed_payment(invoice):
    """Handle failed payment webhook"""
    try:
        # Update payment record
        if invoice.get('payment_intent'):
            Payment.objects.filter(
                stripe_payment_intent_id=invoice['payment_intent']
            ).update(status='failed')
        
        # Update subscription if applicable
        if invoice.get('subscription'):
            Subscription.objects.filter(
                stripe_subscription_id=invoice['subscription']
            ).update(status='past_due')
            
        logger.info(f"Handled failed payment for invoice {invoice['id']}")
        
    except Exception as e:
        logger.error(f"Error handling failed payment: {e}")

def handle_subscription_updated(subscription):
    """Handle subscription updated webhook"""
    try:
        from django.utils import timezone
        
        Subscription.objects.filter(
            stripe_subscription_id=subscription['id']
        ).update(
            status=subscription['status'],
            current_period_start=timezone.datetime.fromtimestamp(subscription['current_period_start']),
            current_period_end=timezone.datetime.fromtimestamp(subscription['current_period_end']),
            cancel_at_period_end=subscription['cancel_at_period_end']
        )
        
        logger.info(f"Updated subscription {subscription['id']}")
        
    except Exception as e:
        logger.error(f"Error handling subscription update: {e}")

def handle_subscription_deleted(subscription):
    """Handle subscription deleted webhook"""
    try:
        from django.utils import timezone
        
        Subscription.objects.filter(
            stripe_subscription_id=subscription['id']
        ).update(
            status='canceled',
            canceled_at=timezone.now()
        )
        
        logger.info(f"Canceled subscription {subscription['id']}")
        
    except Exception as e:
        logger.error(f"Error handling subscription deletion: {e}")
