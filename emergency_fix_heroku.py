#!/usr/bin/env python
"""
🚨 EMERGENCY: Direct Database Fix for Heroku Production
Bypasses Django ORM to directly fix transaction ID constraint issue
"""

# Set up Django environment
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

# Now import Django components
from django.db import connection
import uuid
from datetime import datetime

def emergency_fix_transaction_ids():
    """
    Emergency fix using raw SQL to handle transaction ID duplicates
    """
    print("🚨 EMERGENCY DATABASE FIX IN PROGRESS...")
    
    with connection.cursor() as cursor:
        try:
            # Step 1: Check current state
            cursor.execute("SELECT COUNT(*) FROM payments_payment WHERE transaction_id IS NULL OR transaction_id = '';")
            problem_count = cursor.fetchone()[0]
            
            print(f"🔍 Found {problem_count} payments with problematic transaction IDs")
            
            if problem_count == 0:
                print("✅ No problematic transaction IDs found")
                return True
            
            # Step 2: Fix NULL and empty transaction IDs with unique values
            cursor.execute("""
                UPDATE payments_payment 
                SET transaction_id = 'TXN_' || id || '_' || EXTRACT(EPOCH FROM NOW())::BIGINT 
                WHERE transaction_id IS NULL OR transaction_id = '';
            """)
            
            updated_rows = cursor.rowcount
            print(f"✅ Fixed {updated_rows} transaction IDs")
            
            # Step 3: Verify fix
            cursor.execute("SELECT COUNT(*) FROM payments_payment WHERE transaction_id IS NULL OR transaction_id = '';")
            remaining_problems = cursor.fetchone()[0]
            
            if remaining_problems == 0:
                print("🎉 ALL TRANSACTION IDs FIXED SUCCESSFULLY!")
                return True
            else:
                print(f"⚠️  {remaining_problems} problems still remain")
                return False
                
        except Exception as e:
            print(f"❌ DATABASE FIX ERROR: {e}")
            return False

if __name__ == "__main__":
    print("🚀 HEROKU EMERGENCY DATABASE FIX")
    print("=" * 40)
    
    success = emergency_fix_transaction_ids()
    
    if success:
        print("✅ EMERGENCY FIX SUCCESSFUL")
        print("🔄 You can now retry the deployment")
    else:
        print("❌ EMERGENCY FIX FAILED")
        print("🔧 Manual intervention may be required")
