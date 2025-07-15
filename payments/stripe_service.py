#!/usr/bin/env python
"""
Express Deals - Stripe Payment Service
Complete payment management including subscriptions, recurring payments, and manual payments
"""

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import logging

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

class StripePaymentService:
    """Comprehensive Stripe payment service for Express Deals"""
    
    def __init__(self):
        """Initialize Stripe service with API key"""
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
    # ===== CUSTOMER MANAGEMENT =====
    
    def create_customer(self, user, email=None, name=None):
        """Create a Stripe customer for a user"""
        try:
            customer = stripe.Customer.create(
                email=email or user.email,
                name=name or f"{user.first_name} {user.last_name}".strip() or user.username,
                metadata={
                    'user_id': user.id,
                    'django_user': user.username,
                    'created_by': 'express_deals'
                }
            )
            
            logger.info(f"Created Stripe customer {customer.id} for user {user.id}")
            return customer
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise e
    
    def get_or_create_customer(self, user):
        """Get existing customer or create new one"""
        # Check if user already has a customer ID stored
        if hasattr(user, 'stripe_customer_id') and user.stripe_customer_id:
            try:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
                return customer
            except stripe.error.InvalidRequestError:
                # Customer doesn't exist, create new one
                pass
        
        # Search for existing customer by email
        customers = stripe.Customer.list(email=user.email, limit=1)
        if customers.data:
            customer = customers.data[0]
            # Store customer ID for future use
            if hasattr(user, 'stripe_customer_id'):
                user.stripe_customer_id = customer.id
                user.save()
            return customer
        
        # Create new customer
        return self.create_customer(user)
    
    # ===== MANUAL PAYMENTS =====
    
    def create_payment_intent(self, amount, currency='gbp', customer=None, description=None, metadata=None):
        """Create a payment intent for manual payments"""
        try:
            intent_data = {
                'amount': int(amount * 100),  # Convert to cents
                'currency': currency,
                'automatic_payment_methods': {'enabled': True},
                'description': description or 'Express Deals Purchase',
                'metadata': metadata or {}
            }
            
            if customer:
                intent_data['customer'] = customer.id if hasattr(customer, 'id') else customer
            
            intent = stripe.PaymentIntent.create(**intent_data)
            
            logger.info(f"Created payment intent {intent.id} for amount {amount} {currency}")
            return intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create payment intent: {e}")
            raise e
    
    def confirm_payment_intent(self, payment_intent_id, payment_method_id=None):
        """Confirm a payment intent"""
        try:
            confirm_data = {}
            if payment_method_id:
                confirm_data['payment_method'] = payment_method_id
            
            intent = stripe.PaymentIntent.confirm(payment_intent_id, **confirm_data)
            
            logger.info(f"Confirmed payment intent {payment_intent_id}: {intent.status}")
            return intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to confirm payment intent: {e}")
            raise e
    
    # ===== SUBSCRIPTION MANAGEMENT =====
    
    def create_product(self, name, description=None, metadata=None):
        """Create a product for subscriptions"""
        try:
            product = stripe.Product.create(
                name=name,
                description=description,
                metadata=metadata or {}
            )
            
            logger.info(f"Created product {product.id}: {name}")
            return product
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create product: {e}")
            raise e
    
    def create_price(self, product_id, amount, currency='gbp', interval='month', interval_count=1):
        """Create a recurring price for subscriptions"""
        try:
            price = stripe.Price.create(
                product=product_id,
                unit_amount=int(amount * 100),  # Convert to cents
                currency=currency,
                recurring={
                    'interval': interval,
                    'interval_count': interval_count
                }
            )
            
            logger.info(f"Created price {price.id} for product {product_id}: {amount} {currency}/{interval}")
            return price
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create price: {e}")
            raise e
    
    def create_subscription(self, customer, price_id, trial_period_days=None, metadata=None):
        """Create a subscription for a customer"""
        try:
            subscription_data = {
                'customer': customer.id if hasattr(customer, 'id') else customer,
                'items': [{'price': price_id}],
                'payment_behavior': 'default_incomplete',
                'payment_settings': {'save_default_payment_method': 'on_subscription'},
                'expand': ['latest_invoice.payment_intent'],
                'metadata': metadata or {}
            }
            
            if trial_period_days:
                subscription_data['trial_period_days'] = trial_period_days
            
            subscription = stripe.Subscription.create(**subscription_data)
            
            logger.info(f"Created subscription {subscription.id} for customer {customer.id if hasattr(customer, 'id') else customer}")
            return subscription
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create subscription: {e}")
            raise e
    
    def cancel_subscription(self, subscription_id, at_period_end=True):
        """Cancel a subscription"""
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)
            
            logger.info(f"Cancelled subscription {subscription_id}")
            return subscription
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise e
    
    def update_subscription(self, subscription_id, new_price_id=None, metadata=None):
        """Update a subscription"""
        try:
            update_data = {}
            
            if new_price_id:
                # Get current subscription to modify items
                subscription = stripe.Subscription.retrieve(subscription_id)
                update_data['items'] = [{
                    'id': subscription['items']['data'][0].id,
                    'price': new_price_id,
                }]
            
            if metadata:
                update_data['metadata'] = metadata
            
            subscription = stripe.Subscription.modify(subscription_id, **update_data)
            
            logger.info(f"Updated subscription {subscription_id}")
            return subscription
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update subscription: {e}")
            raise e
    
    # ===== RECURRING PAYMENTS (Invoice-based) =====
    
    def create_invoice_item(self, customer, amount, currency='gbp', description=None, metadata=None):
        """Create an invoice item for recurring billing"""
        try:
            invoice_item = stripe.InvoiceItem.create(
                customer=customer.id if hasattr(customer, 'id') else customer,
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                description=description or 'Express Deals Service',
                metadata=metadata or {}
            )
            
            logger.info(f"Created invoice item {invoice_item.id} for customer {customer.id if hasattr(customer, 'id') else customer}")
            return invoice_item
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create invoice item: {e}")
            raise e
    
    def create_invoice(self, customer, auto_advance=True, collection_method='charge_automatically'):
        """Create and send an invoice"""
        try:
            invoice = stripe.Invoice.create(
                customer=customer.id if hasattr(customer, 'id') else customer,
                auto_advance=auto_advance,
                collection_method=collection_method
            )
            
            # Finalize the invoice
            if auto_advance:
                invoice = stripe.Invoice.finalize_invoice(invoice.id)
            
            logger.info(f"Created invoice {invoice.id} for customer {customer.id if hasattr(customer, 'id') else customer}")
            return invoice
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create invoice: {e}")
            raise e
    
    # ===== PAYMENT METHODS =====
    
    def create_setup_intent(self, customer, usage='off_session'):
        """Create a setup intent for saving payment methods"""
        try:
            setup_intent = stripe.SetupIntent.create(
                customer=customer.id if hasattr(customer, 'id') else customer,
                usage=usage,
                payment_method_types=['card']
            )
            
            logger.info(f"Created setup intent {setup_intent.id} for customer {customer.id if hasattr(customer, 'id') else customer}")
            return setup_intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create setup intent: {e}")
            raise e
    
    def get_customer_payment_methods(self, customer, type='card'):
        """Get all payment methods for a customer"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer.id if hasattr(customer, 'id') else customer,
                type=type
            )
            
            return payment_methods.data
            
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get payment methods: {e}")
            raise e
    
    # ===== WEBHOOK HANDLING =====
    
    def construct_webhook_event(self, payload, sig_header):
        """Construct and verify webhook event"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError:
            # Invalid payload
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            raise stripe.error.SignatureVerificationError("Invalid signature")
    
    # ===== UTILITY METHODS =====
    
    def format_amount(self, amount_cents, currency='gbp'):
        """Format amount from cents to currency string"""
        amount = amount_cents / 100
        currency_symbols = {
            'gbp': '£',
            'usd': '$',
            'eur': '€'
        }
        symbol = currency_symbols.get(currency.lower(), currency.upper())
        return f"{symbol}{amount:.2f}"
    
    def get_subscription_status(self, subscription_id):
        """Get detailed subscription status"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'trial_end': subscription.trial_end,
                'amount': subscription.items.data[0].price.unit_amount,
                'currency': subscription.items.data[0].price.currency,
                'interval': subscription.items.data[0].price.recurring.interval
            }
        except stripe.error.StripeError as e:
            logger.error(f"Failed to get subscription status: {e}")
            raise e

# Create a global instance
stripe_service = StripePaymentService()
