from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import DemoCard, PaymentMethod
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Create demo credit cards and assign to users'
    
    def handle(self, *args, **options):
        # Create demo credit cards
        demo_cards = [
            {
                'card_type': 'visa',
                'card_number': '4242424242424242',
                'card_holder_name': 'John Doe',
                'expiry_month': '12',
                'expiry_year': '2026',
                'cvv': '123',
                'scenario': 'Success',
                'description': 'Visa card for successful payments'
            },
            {
                'card_type': 'mastercard',
                'card_number': '5555555555554444',
                'card_holder_name': 'Jane Smith',
                'expiry_month': '11',
                'expiry_year': '2025',
                'cvv': '456',
                'scenario': 'Success',
                'description': 'Mastercard for successful payments'
            },
            {
                'card_type': 'amex',
                'card_number': '378282246310005',
                'card_holder_name': 'Bob Johnson',
                'expiry_month': '10',
                'expiry_year': '2027',
                'cvv': '789',
                'scenario': 'Success',
                'description': 'American Express for successful payments'
            },
            {
                'card_type': 'visa',
                'card_number': '4000000000000002',
                'card_holder_name': 'Test Decline',
                'expiry_month': '09',
                'expiry_year': '2026',
                'cvv': '111',
                'scenario': 'Declined',
                'description': 'Visa card that will be declined'
            },
            {
                'card_type': 'visa',
                'card_number': '4000000000009995',
                'card_holder_name': 'Test Insufficient',
                'expiry_month': '08',
                'expiry_year': '2025',
                'cvv': '222',
                'scenario': 'Insufficient Funds',
                'description': 'Visa card with insufficient funds'
            }
        ]
        
        # Create demo cards
        for card_data in demo_cards:
            demo_card, created = DemoCard.objects.get_or_create(
                card_number=card_data['card_number'],
                defaults=card_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created demo card: {demo_card}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Demo card already exists: {demo_card}')
                )
        
        # Assign demo cards to users
        users = User.objects.all()
        demo_cards_qs = DemoCard.objects.filter(scenario='Success')
        
        for i, user in enumerate(users):
            if demo_cards_qs.exists():
                demo_card = demo_cards_qs[i % demo_cards_qs.count()]
                
                # Create payment method for user
                payment_method, created = PaymentMethod.objects.get_or_create(
                    user=user,
                    card_number=f"**** **** **** {demo_card.card_number[-4:]}",
                    defaults={
                        'payment_type': 'credit_card',
                        'card_holder_name': demo_card.card_holder_name,
                        'expiry_month': demo_card.expiry_month,
                        'expiry_year': demo_card.expiry_year,
                        'cvv': demo_card.cvv,
                        'is_demo': True,
                        'is_default': True,
                        'is_active': True,
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Assigned demo card to {user.username}: {demo_card.card_number[-4:]}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Demo card already assigned to {user.username}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Demo credit cards setup completed!')
        )
