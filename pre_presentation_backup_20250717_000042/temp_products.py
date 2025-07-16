#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category

print("Current Products in Database:")
print("=" * 50)

products = Product.objects.all().order_by('id')
for p in products:
    print(f"ID: {p.id}")
    print(f"Name: {p.name}")
    print(f"Price: ${p.price}")
    print(f"Original Price: ${p.original_price or 'None'}")
    print(f"Category: {p.category.name}")
    print(f"Slug: '{p.slug}'")
    print(f"Stock: {p.stock_quantity}")
    print(f"Featured: {p.is_featured}")
    print("-" * 30)

print(f"\nTotal Products: {products.count()}")
print(f"Total Categories: {Category.objects.count()}")
