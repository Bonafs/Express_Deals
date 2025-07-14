import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth import authenticate

print("Authentication Test")
print("-" * 30)

# Test admin
admin = authenticate(username='admin', password='Mobolaji')
print(f"Admin: {'PASS' if admin else 'FAIL'}")

# Test bonafs  
bonafs = authenticate(username='bonafs', password='expressdeals')
print(f"Bonafs: {'PASS' if bonafs else 'FAIL'}")

if admin and bonafs:
    print("All tests PASSED!")
else:
    print("Some tests FAILED!")
