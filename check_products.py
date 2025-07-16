import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product

print(f"Total Products: {Product.objects.count()}")
print(f"Featured Products: {Product.objects.filter(is_featured=True).count()}")

# Show first 5 products
for product in Product.objects.all()[:5]:
    print(f"  • {product.name} - £{product.price}")
