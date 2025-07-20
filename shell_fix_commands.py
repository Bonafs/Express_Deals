"""
Quick Database Fix - Run this directly in Django shell
Copy and paste this code into heroku run python manage.py shell
"""

# Step 1: Import required modules
from payments.models import Payment
from django.db import transaction
import uuid
from datetime import datetime

# Step 2: Fix duplicate transaction IDs
def fix_transaction_ids_now():
    with transaction.atomic():
        # Find payments with problematic transaction IDs
        problematic = Payment.objects.filter(
            models.Q(transaction_id__isnull=True) | 
            models.Q(transaction_id='')
        )
        
        print(f"Found {problematic.count()} problematic payments")
        
        # Fix each one with a unique ID
        for payment in problematic:
            unique_id = f"TXN_{payment.id}_{int(datetime.now().timestamp())}"
            payment.transaction_id = unique_id
            payment.save()
            print(f"Fixed payment {payment.id}: {unique_id}")
        
        print("All transaction IDs fixed!")

# Step 3: Run the fix
fix_transaction_ids_now()
