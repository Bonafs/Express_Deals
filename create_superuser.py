#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@expressdeals.com' 
password = 'expressdeals'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Superuser "{username}" created successfully!')
    print(f'📧 Email: {email}')
    print(f'🔑 Password: {password}')
    print(f'🌐 Access admin at: http://127.0.0.1:8000/admin/')
else:
    print(f'ℹ️  Superuser "{username}" already exists!')
    
# Verify creation
total_users = User.objects.count()
superusers = User.objects.filter(is_superuser=True).count()
print(f'\n📊 Database Status:')
print(f'   Total users: {total_users}')
print(f'   Superusers: {superusers}')
