from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Temporary placeholder views
class ProcessPaymentView(View):
    def get(self, request):
        return HttpResponse("Process Payment View - Coming Soon!")

class PaymentSuccessView(View):
    def get(self, request):
        return HttpResponse("Payment Success View - Coming Soon!")

class PaymentCancelView(View):
    def get(self, request):
        return HttpResponse("Payment Cancel View - Coming Soon!")

class StripeWebhookView(View):
    def post(self, request):
        return HttpResponse("Stripe Webhook View - Coming Soon!")
