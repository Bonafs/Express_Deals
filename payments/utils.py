"""
Express Deals - Transaction ID Generator
Ensures unique transaction IDs for payments
"""

import uuid
import time
from datetime import datetime
from django.utils import timezone


def generate_unique_transaction_id(prefix='TXN'):
    """
    Generate a unique transaction ID
    Format: PREFIX-YYYYMMDD-HHMMSS-UUID4
    Example: TXN-20250718-143021-a1b2c3d4
    """
    timestamp = timezone.now()
    date_part = timestamp.strftime('%Y%m%d')
    time_part = timestamp.strftime('%H%M%S')
    uuid_part = str(uuid.uuid4())[:8]
    
    return f"{prefix}-{date_part}-{time_part}-{uuid_part}"


def generate_payment_transaction_id():
    """Generate transaction ID specifically for payments"""
    return generate_unique_transaction_id('PAY')


def generate_subscription_transaction_id():
    """Generate transaction ID for subscriptions"""
    return generate_unique_transaction_id('SUB')


def generate_refund_transaction_id():
    """Generate transaction ID for refunds"""
    return generate_unique_transaction_id('REF')
