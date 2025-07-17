import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapeTarget

print(f"Products: {Product.objects.count()}")
print(f"Targets: {ScrapeTarget.objects.count()}")
print("✅ Django working!")
