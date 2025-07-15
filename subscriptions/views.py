"""
Express Deals - Subscription and Payment Views
Handle recurring payments, manual payments, and subscription management
"""

import json
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import (
    SubscriptionPlan, CustomerSubscription, PaymentIntent, 
    StripeCustomer, PaymentHistory
)

# Set up Stripe with your live test key
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

# ============================================================================
# SUBSCRIPTION VIEWS
# ============================================================================

@login_required
def subscription_plans(request):
    """Display available subscription plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True)
    current_subscription = CustomerSubscription.objects.filter(
        user=request.user, 
        status__in=['active', 'trialing']
    ).first()
    
    context = {
        'plans': plans,
        'current_subscription': current_subscription,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'subscriptions/plans.html', context)

@login_required
@require_POST
def create_subscription(request):
    """Create a new subscription"""
    plan_id = request.POST.get('plan_id')
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    
    # Check if user already has an active subscription
    existing_subscription = CustomerSubscription.objects.filter(
        user=request.user,
        status__in=['active', 'trialing']
    ).first()
    
    if existing_subscription:
        messages.error(request, "You already have an active subscription.")
        return redirect('subscription_plans')
    
    try:
        # Get or create Stripe customer
        stripe_customer = StripeCustomer.get_or_create_stripe_customer(request.user)
        
        # Create Stripe subscription
        subscription = stripe.Subscription.create(
            customer=stripe_customer.stripe_customer_id,
            items=[{'price': plan.stripe_price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
            trial_period_days=plan.trial_period_days if plan.trial_period_days > 0 else None,
        )
        
        # Create local subscription record
        customer_subscription = CustomerSubscription.objects.create(
            user=request.user,
            plan=plan,
            stripe_subscription_id=subscription.id,
            stripe_customer_id=stripe_customer.stripe_customer_id,
            status=subscription.status,
            current_period_start=timezone.datetime.fromtimestamp(
                subscription.current_period_start, tz=timezone.utc
            ),
            current_period_end=timezone.datetime.fromtimestamp(
                subscription.current_period_end, tz=timezone.utc
            ),
        )
        
        if subscription.trial_start and subscription.trial_end:
            customer_subscription.trial_start = timezone.datetime.fromtimestamp(
                subscription.trial_start, tz=timezone.utc
            )
            customer_subscription.trial_end = timezone.datetime.fromtimestamp(
                subscription.trial_end, tz=timezone.utc
            )
            customer_subscription.save()
        
        # Return client secret for payment confirmation
        return JsonResponse({
            'client_secret': subscription.latest_invoice.payment_intent.client_secret,
            'subscription_id': subscription.id,
        })
        
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

@login_required
def subscription_management(request):
    """Manage user's current subscription"""
    subscription = CustomerSubscription.objects.filter(
        user=request.user
    ).order_by('-created_at').first()
    
    payment_history = PaymentHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    context = {
        'subscription': subscription,
        'payment_history': payment_history,
    }
    return render(request, 'subscriptions/management.html', context)

@login_required
@require_POST
def cancel_subscription(request):
    """Cancel user's subscription"""
    subscription = get_object_or_404(
        CustomerSubscription,
        user=request.user,
        status__in=['active', 'trialing']
    )
    
    at_period_end = request.POST.get('at_period_end', 'true') == 'true'
    
    try:
        subscription.cancel_subscription(at_period_end=at_period_end)
        
        if at_period_end:
            messages.success(request, "Subscription will be canceled at the end of the current billing period.")
        else:
            messages.success(request, "Subscription has been canceled immediately.")
            
        return redirect('subscription_management')
    except Exception as e:
        messages.error(request, f"Error canceling subscription: {e}")
        return redirect('subscription_management')

# ============================================================================
# MANUAL PAYMENT VIEWS
# ============================================================================

@login_required
def manual_payment(request):
    """Create a one-time manual payment"""
    return render(request, 'payments/manual_payment.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
@require_POST
def create_payment_intent(request):
    """Create a payment intent for manual payment"""
    try:
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', 0)))
        description = data.get('description', '')
        
        if amount <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        
        # Create payment intent
        payment_intent = PaymentIntent.create_payment_intent(
            user=request.user,
            amount=amount,
            description=description,
            metadata={
                'user_id': str(request.user.id),
                'payment_type': 'manual'
            }
        )
        
        return JsonResponse({
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.stripe_payment_intent_id,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def payment_success(request):
    """Payment success page"""
    payment_intent_id = request.GET.get('payment_intent')
    if payment_intent_id:
        try:
            payment_intent = PaymentIntent.objects.get(
                stripe_payment_intent_id=payment_intent_id,
                user=request.user
            )
            context = {'payment_intent': payment_intent}
        except PaymentIntent.DoesNotExist:
            context = {}
    else:
        context = {}
    
    return render(request, 'payments/success.html', context)

# ============================================================================
# WEBHOOK HANDLERS
# ============================================================================

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_intent_succeeded(payment_intent)
    
    elif event['type'] == 'subscription.created':
        subscription = event['data']['object']
        handle_subscription_created(subscription)
    
    elif event['type'] == 'subscription.updated':
        subscription = event['data']['object']
        handle_subscription_updated(subscription)
    
    elif event['type'] == 'subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deleted(subscription)
    
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_invoice_payment_succeeded(invoice)
    
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_invoice_payment_failed(invoice)
    
    return HttpResponse(status=200)

def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment intent"""
    try:
        pi = PaymentIntent.objects.get(
            stripe_payment_intent_id=payment_intent['id']
        )
        pi.status = 'succeeded'
        pi.save()
        
        # Create payment history record
        PaymentHistory.objects.create(
            user=pi.user,
            stripe_payment_id=payment_intent['id'],
            payment_type='one_time',
            amount=Decimal(str(payment_intent['amount'])) / 100,
            currency=payment_intent['currency'],
            status='succeeded',
            description=pi.description,
            payment_intent=pi
        )
    except PaymentIntent.DoesNotExist:
        pass

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    try:
        sub = CustomerSubscription.objects.get(
            stripe_subscription_id=subscription['id']
        )
        sub.status = subscription['status']
        sub.current_period_start = timezone.datetime.fromtimestamp(
            subscription['current_period_start'], tz=timezone.utc
        )
        sub.current_period_end = timezone.datetime.fromtimestamp(
            subscription['current_period_end'], tz=timezone.utc
        )
        
        if subscription.get('canceled_at'):
            sub.canceled_at = timezone.datetime.fromtimestamp(
                subscription['canceled_at'], tz=timezone.utc
            )
        
        if subscription.get('ended_at'):
            sub.ended_at = timezone.datetime.fromtimestamp(
                subscription['ended_at'], tz=timezone.utc
            )
        
        sub.save()
    except CustomerSubscription.DoesNotExist:
        pass

def handle_subscription_created(subscription):
    """Handle new subscription creation from webhook"""
    # This is typically handled in the create_subscription view
    pass

def handle_subscription_deleted(subscription):
    """Handle subscription deletion"""
    try:
        sub = CustomerSubscription.objects.get(
            stripe_subscription_id=subscription['id']
        )
        sub.status = 'canceled'
        sub.ended_at = timezone.now()
        sub.save()
    except CustomerSubscription.DoesNotExist:
        pass

def handle_invoice_payment_succeeded(invoice):
    """Handle successful invoice payment (recurring subscription)"""
    try:
        subscription_id = invoice.get('subscription')
        if subscription_id:
            sub = CustomerSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            
            # Create payment history record
            PaymentHistory.objects.create(
                user=sub.user,
                stripe_payment_id=invoice['id'],
                payment_type='subscription',
                amount=Decimal(str(invoice['amount_paid'])) / 100,
                currency=invoice['currency'],
                status='succeeded',
                description=f"Subscription payment for {sub.plan.name}",
                subscription=sub
            )
    except CustomerSubscription.DoesNotExist:
        pass

def handle_invoice_payment_failed(invoice):
    """Handle failed invoice payment"""
    try:
        subscription_id = invoice.get('subscription')
        if subscription_id:
            sub = CustomerSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            
            # Create payment history record
            PaymentHistory.objects.create(
                user=sub.user,
                stripe_payment_id=invoice['id'],
                payment_type='subscription',
                amount=Decimal(str(invoice['amount_due'])) / 100,
                currency=invoice['currency'],
                status='failed',
                description=f"Failed subscription payment for {sub.plan.name}",
                subscription=sub
            )
            
            # Optionally send notification to user about failed payment
            # send_payment_failed_notification(sub.user, sub)
    except CustomerSubscription.DoesNotExist:
        pass
