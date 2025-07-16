import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapeJob

print(f"Products: {Product.objects.count()}")
print(f"Jobs: {ScrapeJob.objects.count()}")

# Show latest few products if any
if Product.objects.exists():
    print("\nLatest products:")
    for product in Product.objects.order_by('-id')[:3]:
        print(f"- {product.name} - £{product.price}")
else:
    print("No products yet")

# Show latest jobs
print("\nLatest jobs:")
for job in ScrapeJob.objects.order_by('-started_at')[:3]:
    print(f"- {job.target.name}: {job.status} (Found: {job.products_found})")
