

from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order
from .models import Payment, Refund, StripeWebhookEvent

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='payuser')
        self.order = Order.objects.create(user=self.user, subtotal=10, tax_amount=1, shipping_cost=2, total=13, shipping_name='Name', shipping_email='a@b.com', shipping_address_line1='Addr', shipping_city='City', shipping_state='State', shipping_postal_code='12345')
        self.payment = Payment.objects.create(order=self.order, user=self.user, amount=13, currency='USD')

    def test_str(self):
        # The __str__ does not include username, just payment id, order number, and status
        expected = f"Payment {self.payment.id} - {self.order.order_number} - {self.payment.status}"
        self.assertEqual(str(self.payment), expected)

class RefundModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='refunduser')
        self.order = Order.objects.create(user=self.user, subtotal=10, tax_amount=1, shipping_cost=2, total=13, shipping_name='Name', shipping_email='a@b.com', shipping_address_line1='Addr', shipping_city='City', shipping_state='State', shipping_postal_code='12345')
        self.payment = Payment.objects.create(order=self.order, user=self.user, amount=13, currency='USD')
        self.refund = Refund.objects.create(payment=self.payment, order=self.order, user=self.user, amount=5, reason='requested_by_customer')

    def test_str(self):
        # The __str__ does not include username, just refund id, order number, and amount
        expected = f"Refund {self.refund.id} - {self.order.order_number} - ${self.refund.amount}"
        self.assertEqual(str(self.refund), expected)

class StripeWebhookEventModelTest(TestCase):
    def test_str(self):
        event = StripeWebhookEvent.objects.create(stripe_event_id='evt_123', event_type='payment_intent.succeeded', data={})
        self.assertIn('evt_123', str(event))
