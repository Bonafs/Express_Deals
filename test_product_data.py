#!/usr/bin/env python3
"""
Test Current Product Count and Data Quality
Check how many products we've scraped and their data completeness
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapeTarget, ScrapeJob, ScrapedProduct

def test_scraped_products():
    """Test current product count and data quality"""
    
    print("🔍 EXPRESS DEALS PRODUCT DATA TEST")
    print("=" * 50)
    
    # Overall counts
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    featured_products = Product.objects.filter(is_featured=True).count()
    
    print(f"\n📊 PRODUCT OVERVIEW:")
    print(f"   Total Products: {total_products}")
    print(f"   Active Products: {active_products}")
    print(f"   Featured Products: {featured_products}")
    
    if total_products == 0:
        print("\n❌ NO PRODUCTS FOUND")
        print("   The scraping may still be in progress or needs to be triggered")
        
        # Check scraping status
        total_targets = ScrapeTarget.objects.count()
        active_targets = ScrapeTarget.objects.filter(status='active').count()
        total_jobs = ScrapeJob.objects.count()
        
        print(f"\n🎯 SCRAPING STATUS:")
        print(f"   Total Targets: {total_targets}")
        print(f"   Active Targets: {active_targets}")
        print(f"   Total Jobs: {total_jobs}")
        
        # Show recent jobs
        recent_jobs = ScrapeJob.objects.order_by('-started_at')[:5]
        print(f"\n📈 RECENT SCRAPING ATTEMPTS:")
        for job in recent_jobs:
            status_icon = "✅" if job.status == 'completed' else "❌" if job.status == 'failed' else "⏳"
            print(f"   {status_icon} {job.target.name}: {job.status} - Found: {job.products_found}, Imported: {job.products_imported}")
        
        return False
    
    # Data quality analysis
    products_with_name = Product.objects.exclude(name__isnull=True).exclude(name__exact='').count()
    products_with_price = Product.objects.exclude(price__isnull=True).filter(price__gt=0).count()
    products_with_image = Product.objects.exclude(image__isnull=True).exclude(image__exact='').count()
    products_with_description = Product.objects.exclude(description__isnull=True).exclude(description__exact='').count()
    
    print(f"\n📋 DATA QUALITY:")
    print(f"   Products with Name: {products_with_name}/{total_products} ({(products_with_name/total_products)*100:.1f}%)")
    print(f"   Products with Price: {products_with_price}/{total_products} ({(products_with_price/total_products)*100:.1f}%)")
    print(f"   Products with Image: {products_with_image}/{total_products} ({(products_with_image/total_products)*100:.1f}%)")
    print(f"   Products with Description: {products_with_description}/{total_products} ({(products_with_description/total_products)*100:.1f}%)")
    
    # Sample products for display
    print(f"\n🛍️ SAMPLE PRODUCTS (for ProductListView):")
    sample_products = Product.objects.filter(is_active=True)[:10]
    
    for i, product in enumerate(sample_products, 1):
        price_display = f"£{product.price}" if product.price else "No price"
        image_status = "✅" if product.image else "❌"
        category_name = product.category.name if product.category else "No Category"
        
        print(f"   {i}. {product.name[:50]}...")
        print(f"      Price: {price_display} | Image: {image_status} | Category: {category_name}")
        if product.image:
            print(f"      Image URL: {product.image}")
        print()
    
    # Category breakdown
    print(f"📁 PRODUCTS BY CATEGORY:")
    from products.models import Category
    for category in Category.objects.all():
        count = Product.objects.filter(category=category, is_active=True).count()
        if count > 0:
            print(f"   {category.name}: {count} products")
    
    # Ready for ProductListView?
    complete_products = Product.objects.filter(
        is_active=True,
        name__isnull=False,
        price__isnull=False,
        price__gt=0
    ).exclude(name__exact='').count()
    
    print(f"\n🎯 READINESS FOR PRODUCTLISTVIEW:")
    print(f"   Complete Products (name + price + active): {complete_products}")
    
    if complete_products >= 12:
        print("   ✅ READY: Enough products for pagination (12+ per page)")
    elif complete_products >= 6:
        print("   ⚠️ PARTIAL: Some products available but may need more")
    else:
        print("   ❌ NOT READY: Need more complete products")
    
    return complete_products > 0

if __name__ == "__main__":
    test_scraped_products()
