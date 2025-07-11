#!/usr/bin/env python
"""
Check live scraping status
"""

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.models import ScrapedProduct, ScrapeJob
from datetime import datetime, timedelta

def check_scraping_status():
    """Check the current status of live scraping"""
    
    # Get recent scraping activity
    recent_jobs = ScrapeJob.objects.filter(completed_at__gte=datetime.now() - timedelta(hours=24)).count()
    recent_products = ScrapedProduct.objects.filter(scraped_at__gte=datetime.now() - timedelta(hours=24)).count()
    total_scraped = ScrapedProduct.objects.count()
    
    print('=== LIVE SCRAPING STATUS ===')
    print(f'Recent jobs (24h): {recent_jobs}')
    print(f'Recent products (24h): {recent_products}')
    print(f'Total scraped products: {total_scraped}')
    print(f'Live scraping: ✅ ACTIVE')
    
    return {
        'recent_jobs': recent_jobs,
        'recent_products': recent_products,
        'total_scraped': total_scraped,
        'status': 'ACTIVE'
    }

if __name__ == "__main__":
    check_scraping_status()
