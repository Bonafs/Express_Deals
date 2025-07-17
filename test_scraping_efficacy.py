#!/usr/bin/env python
"""
Test Web Scraping Efficacy and Efficiency
Check product names, images, and prices from our world-class scraper
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapeTarget, ScrapedProduct, ScrapeJob

def test_scraping_efficacy():
    """Test the quality of scraped data and analyze performance"""
    
    print("🔍 WORLD-CLASS SCRAPING EFFICACY & PERFORMANCE TEST")
    print("=" * 70)
    
    # Overall statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    featured_products = Product.objects.filter(is_featured=True).count()
    products_with_images = Product.objects.exclude(image__isnull=True).exclude(image__exact='').count()
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total Products: {total_products}")
    print(f"   Active Products: {active_products}")
    print(f"   Featured Products: {featured_products}")
    print(f"   Products with Images: {products_with_images}")
    
    # Calculate image success rate (initialize to 0 if no products)
    image_success_rate = (products_with_images / total_products) * 100 if total_products > 0 else 0
    print(f"   Image Success Rate: {image_success_rate:.1f}%")
    
    # Test product quality
    print(f"\n📦 PRODUCT QUALITY TEST:")
    print("-" * 60)
    
    sample_products = Product.objects.all()[:10]
    
    for i, product in enumerate(sample_products, 1):
        # Test product name
        name_quality = "✅" if len(product.name) > 10 else "⚠️"
        
        # Test price
        price_quality = "✅" if product.price and product.price > 0 else "❌"
        
        # Test image
        image_quality = "✅" if product.image else "❌"
        
        print(f"{i:2d}. {product.name[:40]:40} - £{product.price:8.2f}")
        print(f"    Name: {name_quality} | Price: {price_quality} | Image: {image_quality}")
        if product.image:
            print(f"    Image: {product.image}")
        print()
    
    # Test scraping targets
    print(f"\n🎯 SCRAPING TARGETS:")
    print("-" * 60)
    
    targets = ScrapeTarget.objects.all()
    active_targets = targets.filter(status='active')
    
    print(f"   Total Targets: {targets.count()}")
    print(f"   Active Targets: {active_targets.count()}")
    
    for target in active_targets:
        print(f"   • {target.name} ({target.site_type})")
    
    # Test recent scraping jobs
    print(f"\n⚡ RECENT SCRAPING JOBS:")
    print("-" * 60)
    
    recent_jobs = ScrapeJob.objects.all().order_by('-started_at')[:5]
    
    for job in recent_jobs:
        status_icon = "✅" if job.status == 'completed' else "🔄" if job.status == 'running' else "❌"
        print(f"   {status_icon} {job.target.name}: {job.products_imported} products imported")
        if job.started_at:
            print(f"      Started: {job.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test data completeness
    print(f"\n🔬 DATA COMPLETENESS ANALYSIS:")
    print("-" * 60)
    
    # Products with complete data
    complete_products = Product.objects.filter(
        name__isnull=False,
        price__gt=0,
        description__isnull=False
    ).exclude(image__isnull=True).exclude(image__exact='')
    
    print(f"   Products with complete data: {complete_products.count()}")
    
    if total_products > 0:
        completeness_rate = (complete_products.count() / total_products) * 100
        print(f"   Data Completeness Rate: {completeness_rate:.1f}%")
    
    # Price range analysis
    if total_products > 0:
        from django.db.models import Min, Max, Avg
        price_stats = Product.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
        
        print(f"\n💰 PRICE ANALYSIS:")
        print(f"   Minimum Price: £{price_stats['min_price']:.2f}")
        print(f"   Maximum Price: £{price_stats['max_price']:.2f}")
        print(f"   Average Price: £{price_stats['avg_price']:.2f}")
    
    # Quality score
    print(f"\n🏆 OVERALL QUALITY SCORE:")
    print("-" * 60)
    
    quality_factors = []
    
    if total_products >= 60:
        quality_factors.append("✅ Product Count Target (60+)")
    elif total_products >= 20:
        quality_factors.append("⚠️ Partial Product Count")
    else:
        quality_factors.append("❌ Low Product Count")
    
    if image_success_rate >= 80:
        quality_factors.append("✅ Excellent Image Coverage")
    elif image_success_rate >= 50:
        quality_factors.append("⚠️ Good Image Coverage")
    else:
        quality_factors.append("❌ Poor Image Coverage")
    
    active_rate = (active_products / total_products * 100) if total_products > 0 else 0
    if active_rate >= 90:
        quality_factors.append("✅ High Product Activation Rate")
    elif active_rate >= 70:
        quality_factors.append("⚠️ Good Product Activation Rate")
    else:
        quality_factors.append("❌ Low Product Activation Rate")
    
    for factor in quality_factors:
        print(f"   {factor}")
    
    # Final assessment
    excellent_count = len([f for f in quality_factors if f.startswith("✅")])
    
    print(f"\n🎯 FINAL ASSESSMENT:")
    if excellent_count >= 3:
        print("   🌟 EXCELLENT - World-class scraping performance!")
    elif excellent_count >= 2:
        print("   👍 GOOD - Solid scraping performance")
    else:
        print("   🔧 NEEDS IMPROVEMENT - Optimize scraping settings")

if __name__ == '__main__':
    test_scraping_efficacy()
    print("\n" + "=" * 60)
    print("🔍 Scraping efficacy test completed!")
