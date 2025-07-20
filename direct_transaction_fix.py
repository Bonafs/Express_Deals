#!/usr/bin/env python
"""
Direct Transaction ID Fix Script for Heroku
Copy and paste this into: heroku run python manage.py shell --app express-deals
"""

# Direct import and fix
from payments.models import Payment
from django.db import transaction
from django.db.models import Q
from datetime import datetime
import uuid

# Execute the fix
print("🔧 Starting Transaction ID Fix...")

try:
    with transaction.atomic():
        # Find problematic payments
        problematic = Payment.objects.filter(
            Q(transaction_id__isnull=True) | 
            Q(transaction_id='') |
            Q(transaction_id='transaction_test_123')
        )
        
        count = problematic.count()
        print(f"Found {count} payments with problematic transaction IDs")
        
        if count == 0:
            print("✅ No problematic transaction IDs found!")
        else:
            # Fix each payment
            for i, payment in enumerate(problematic):
                timestamp = int(datetime.now().timestamp())
                unique_id = f"TXN_{payment.id}_{timestamp}_{i}"
                payment.transaction_id = unique_id
                payment.save()
                print(f"Fixed payment {payment.id}: {unique_id}")
            
            print(f"✅ Successfully fixed {count} transaction IDs!")
        
        # Verify no duplicates
        all_payments = Payment.objects.all()
        transaction_ids = [p.transaction_id for p in all_payments if p.transaction_id]
        unique_ids = set(transaction_ids)
        
        if len(transaction_ids) == len(unique_ids):
            print("✅ VERIFICATION PASSED: All transaction IDs are unique")
        else:
            print(f"⚠️  Still have {len(transaction_ids) - len(unique_ids)} duplicates")

except Exception as e:
    print(f"❌ Error: {e}")

print("🎉 Transaction ID fix complete!")
