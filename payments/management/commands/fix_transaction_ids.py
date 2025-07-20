from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment
from django.db.models import Q
import uuid
from datetime import datetime


class Command(BaseCommand):
    help = 'Fix duplicate transaction IDs in payments'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing transaction ID duplicates...')
        
        try:
            with transaction.atomic():
                # Find payments with problematic transaction IDs
                problematic = Payment.objects.filter(
                    Q(transaction_id__isnull=True) | 
                    Q(transaction_id='')
                )
                
                count = problematic.count()
                self.stdout.write(f'Found {count} problematic payments')
                
                if count == 0:
                    self.stdout.write(
                        self.style.SUCCESS('No problematic transaction IDs found')
                    )
                    return
                
                # Fix each one with a unique ID
                fixed = 0
                for payment in problematic:
                    timestamp = int(datetime.now().timestamp())
                    unique_id = f"TXN_{payment.id}_{timestamp}_{fixed}"
                    payment.transaction_id = unique_id
                    payment.save()
                    fixed += 1
                    
                    if fixed % 10 == 0:
                        self.stdout.write(f'Fixed {fixed} payments...')
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully fixed {fixed} transaction IDs!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing transaction IDs: {e}')
            )
