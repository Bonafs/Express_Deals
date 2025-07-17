#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapedProduct, ScrapeJob, ScrapeTarget

def check_scraping_status():
    """Check current scraping status and product count"""
    print("🔍 EXPRESS DEALS SCRAPING STATUS REPORT")
    print("=" * 50)
    
    # Product counts
    total_products = Product.objects.count()
    print(f"📦 Total Products in Database: {total_products}")
    
    # Scraping records
    scraped_products = ScrapedProduct.objects.count()
    total_jobs = ScrapeJob.objects.count()
    active_targets = ScrapeTarget.objects.filter(status='active').count()
    
    print(f"🔄 Total Scraping Jobs: {total_jobs}")
    print(f"📊 ScrapedProduct Records: {scraped_products}")
    print(f"🎯 Active Scrape Targets: {active_targets}")
    
    # Job statistics
    successful_jobs = ScrapeJob.objects.filter(status='completed', products_found__gt=0).count()
    failed_jobs = ScrapeJob.objects.filter(status='failed').count()
    completed_jobs = ScrapeJob.objects.filter(status='completed').count()
    
    print(f"✅ Successful Jobs (with products): {successful_jobs}")
    print(f"✅ Total Completed Jobs: {completed_jobs}")
    print(f"❌ Failed Jobs: {failed_jobs}")
    
    print("\n🎯 ACTIVE SCRAPE TARGETS:")
    for target in ScrapeTarget.objects.filter(status='active')[:10]:
        print(f"  • {target.name} - {target.base_url}")
    
    print("\n📈 RECENT SCRAPING ATTEMPTS:")
    for job in ScrapeJob.objects.order_by('-started_at')[:10]:
        status_icon = "✅" if job.status == 'completed' else "❌" if job.status == 'failed' else "⏳"
        started_time = job.started_at.strftime('%Y-%m-%d %H:%M') if job.started_at else "Not started"
        print(f"  {status_icon} {started_time} - {job.target.name}")
        print(f"     Status: {job.status} | Found: {job.products_found} | Imported: {job.products_imported}")
    
    print("\n🏪 CURRENT PRODUCTS:")
    if total_products > 0:
        for product in Product.objects.all()[:5]:
            category = product.category.name if product.category else "No Category"
            print(f"  • {product.name} - {category} - £{product.price}")
        if total_products > 5:
            print(f"  ... and {total_products - 5} more products")
    else:
        print("  No products found in database")
    
    print("\n🔍 SUMMARY:")
    if total_products == 0:
        print("❌ No products currently in database")
        print("💡 This suggests either:")
        print("   - Scraping hasn't been successful yet")
        print("   - Sample products were removed")
        print("   - Anti-bot protection is blocking scraping")
    else:
        print(f"✅ {total_products} products successfully stored")
    
    return {
        'total_products': total_products,
        'scraped_products': scraped_products,
        'total_jobs': total_jobs,
        'successful_jobs': successful_jobs,
        'failed_jobs': failed_jobs,
        'active_targets': active_targets
    }

if __name__ == "__main__":
    check_scraping_status()
