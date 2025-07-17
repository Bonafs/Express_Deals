import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.models import ScrapedProduct
from products.models import Product

print("=== Database Status ===")
print(f"Total ScrapedProducts: {ScrapedProduct.objects.count()}")
print(f"Total Products: {Product.objects.count()}")
print(f"ScrapedProducts with imported_product: {ScrapedProduct.objects.filter(imported_product__isnull=False).count()}")
print(f"ScrapedProducts with image_url: {ScrapedProduct.objects.exclude(image_url='').count()}")
print(f"Products missing images: {Product.objects.filter(image__isnull=True).count() + Product.objects.filter(image='').count()}")

print("\n=== Sample ScrapedProduct ===")
sp = ScrapedProduct.objects.first()
if sp:
    print(f"Title: {sp.title}")
    print(f"Image URL: {sp.image_url}")
    print(f"Imported Product: {sp.imported_product}")
    print(f"Is Processed: {sp.is_processed}")
else:
    print("No ScrapedProducts found")

print("\n=== Sample Product ===")
p = Product.objects.first()
if p:
    print(f"Name: {p.name}")
    print(f"Image: {p.image}")
else:
    print("No Products found")
