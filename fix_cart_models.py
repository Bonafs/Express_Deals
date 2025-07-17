import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

# First, let's check if the orders_cart table exists
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders_cart';")
table_exists = cursor.fetchone()

if not table_exists:
    print('Creating orders migrations...')
    call_command('makemigrations', 'orders')
    print('Running migrations...')
    call_command('migrate')
    print('✅ Orders models created successfully!')
else:
    print('✅ Orders cart table already exists')

# Check if we have any cart records
cursor.execute("SELECT COUNT(*) FROM orders_cart;")
cart_count = cursor.fetchone()[0]
print(f'Cart records in database: {cart_count}')

print('🎯 Cart models are ready!')
