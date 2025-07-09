#!/usr/bin/env python
"""
Display current user information (securely)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User

def show_user_info():
    print("👥 Current Users in Database:")
    print("=" * 50)
    
    users = User.objects.all()
    
    if users:
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Name: {user.first_name} {user.last_name}")
            print(f"Staff: {'Yes' if user.is_staff else 'No'}")
            print(f"Superuser: {'Yes' if user.is_superuser else 'No'}")
            print("-" * 30)
        
        print(f"\\nTotal users: {users.count()}")
        print(f"Admins: {User.objects.filter(is_superuser=True).count()}")
        print(f"Staff: {User.objects.filter(is_staff=True).count()}")
        
        print("\\n🔐 Login Information:")
        print("• Check your credentials.py file for passwords")
        print("• Admin panel: http://localhost:8000/admin/")
        print("• Platform: http://localhost:8000/")
        
    else:
        print("No users found. Run setup_secure_credentials.py first.")

if __name__ == '__main__':
    show_user_info()
