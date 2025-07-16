#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

# Quick status check
print("🔍 QUICK STATUS CHECK")
print("=" * 30)

try:
    from products.models import Product
    product_count = Product.objects.count()
    print(f"✅ Products: {product_count}")
except Exception as e:
    print(f"❌ Product Error: {e}")

try:
    from scraping.models import ScrapeJob
    job_count = ScrapeJob.objects.count()
    print(f"✅ Scrape Jobs: {job_count}")
except Exception as e:
    print(f"❌ ScrapeJob Error: {e}")

try:
    from scraping.models import ScrapeTarget
    target_count = ScrapeTarget.objects.filter(status='active').count()
    total_targets = ScrapeTarget.objects.count()
    print(f"✅ Active Targets: {target_count}/{total_targets}")
except Exception as e:
    print(f"❌ ScrapeTarget Error: {e}")

print("✅ Basic Django setup working!")
