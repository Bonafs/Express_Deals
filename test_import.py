#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

try:
    from alerts.models import DealCategory, UserSubscription, PriceAlert, AlertNotification
    print("SUCCESS: All alerts models imported successfully!")
    print("Models available:")
    print("- DealCategory")
    print("- UserSubscription") 
    print("- PriceAlert")
    print("- AlertNotification")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()