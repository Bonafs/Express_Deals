#!/usr/bin/env python
"""
🚨 URGENT: Fix Transaction ID Duplication on Heroku Production
This script resolves the database constraint error preventing deployment.
"""
import os
import sys
import django
from django.db import transaction, connection
from django.core.management import execute_from_command_line

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

def fix_transaction_ids():
    """Fix duplicate transaction IDs in production database"""
    
    print("🔧 FIXING TRANSACTION ID DUPLICATES ON HEROKU...")
    
    try:
        from payments.models import Payment
        
        with transaction.atomic():
            # Step 1: Find and fix duplicate/empty transaction IDs
            print("📊 Analyzing transaction ID duplicates...")
            
            # Get payments with empty or duplicate transaction IDs
            empty_payments = Payment.objects.filter(transaction_id__isnull=True)
            duplicate_payments = Payment.objects.filter(transaction_id='')
            
            print(f"🔍 Found {empty_payments.count()} payments with NULL transaction_id")
            print(f"🔍 Found {duplicate_payments.count()} payments with empty transaction_id")
            
            # Step 2: Generate unique transaction IDs for problematic records
            import uuid
            from datetime import datetime
            
            fixed_count = 0
            
            # Fix NULL transaction IDs
            for payment in empty_payments:
                unique_id = f"TXN_{payment.id}_{int(datetime.now().timestamp())}"
                payment.transaction_id = unique_id
                payment.save()
                fixed_count += 1
                print(f"✅ Fixed payment {payment.id}: {unique_id}")
            
            # Fix empty transaction IDs  
            for payment in duplicate_payments:
                unique_id = f"TXN_{payment.id}_{uuid.uuid4().hex[:8]}"
                payment.transaction_id = unique_id
                payment.save()
                fixed_count += 1
                print(f"✅ Fixed payment {payment.id}: {unique_id}")
                
            print(f"🎉 SUCCESSFULLY FIXED {fixed_count} TRANSACTION IDS")
            
            # Step 3: Verify no duplicates remain
            all_transaction_ids = Payment.objects.values_list('transaction_id', flat=True)
            unique_count = len(set(all_transaction_ids))
            total_count = all_transaction_ids.count()
            
            if unique_count == total_count:
                print("✅ VERIFICATION PASSED: All transaction IDs are now unique")
                return True
            else:
                print(f"❌ VERIFICATION FAILED: {total_count - unique_count} duplicates still exist")
                return False
                
    except Exception as e:
        print(f"❌ ERROR FIXING TRANSACTION IDS: {e}")
        return False

def create_migration_if_needed():
    """Create migration to handle the unique constraint"""
    print("📝 Creating migration for transaction ID unique constraint...")
    
    migration_content = '''# Generated migration for transaction ID fix
from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('payments', '0001_initial'),
    ]
    
    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True, null=False, blank=False),
        ),
    ]
'''
    
    # Write migration file
    migration_path = 'payments/migrations/0002_fix_transaction_id_unique.py'
    with open(migration_path, 'w') as f:
        f.write(migration_content)
    
    print(f"✅ Created migration: {migration_path}")

if __name__ == "__main__":
    print("🚀 HEROKU PRODUCTION DATABASE FIX")
    print("=" * 50)
    
    # Step 1: Fix the data
    if fix_transaction_ids():
        print("✅ DATA FIX SUCCESSFUL")
    else:
        print("❌ DATA FIX FAILED")
        sys.exit(1)
    
    # Step 2: Create migration
    create_migration_if_needed()
    
    print("🎉 HEROKU TRANSACTION ID FIX COMPLETE")
    print("✨ Ready for successful deployment!")
