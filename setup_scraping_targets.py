#!/usr/bin/env python
"""
Express Deals - Setup Scraping Targets
Create sample scraping targets for demonstration
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from scraping.models import ScrapeTarget

def create_sample_scraping_targets():
    """Create sample scraping targets"""
    
    sample_targets = [
        {
            'name': 'Amazon UK Electronics',
            'base_url': 'https://www.amazon.co.uk',
            'search_url_template': 'https://www.amazon.co.uk/s?k={query}&ref=nb_sb_noss',
            'site_type': 'amazon',
            'scrape_frequency_hours': 6,
            'max_pages': 3,
            'product_selector': '[data-component-type="s-search-result"]',
            'title_selector': '[data-cy="title-recipe-H1"]',
            'price_selector': '.a-price-whole',
            'image_selector': '.s-image',
            'url_selector': 'h2 a',
            'status': 'active'
        },
        {
            'name': 'eBay UK Marketplace',
            'base_url': 'https://www.ebay.co.uk',
            'search_url_template': 'https://www.ebay.co.uk/sch/i.html?_nkw={query}',
            'site_type': 'ebay',
            'scrape_frequency_hours': 4,
            'max_pages': 2,
            'product_selector': '.s-item',
            'title_selector': '.s-item__title',
            'price_selector': '.s-item__price',
            'image_selector': '.s-item__image img',
            'url_selector': '.s-item__link',
            'status': 'active'
        },
        {
            'name': 'Currys PC World',
            'base_url': 'https://www.currys.co.uk',
            'search_url_template': 'https://www.currys.co.uk/search?q={query}',
            'site_type': 'custom',
            'scrape_frequency_hours': 8,
            'max_pages': 2,
            'product_selector': '.product-tile',
            'title_selector': '.product-title',
            'price_selector': '.price-current',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
            'status': 'active'
        },
        {
            'name': 'Argos UK',
            'base_url': 'https://www.argos.co.uk',
            'search_url_template': 'https://www.argos.co.uk/search/{query}/',
            'site_type': 'custom',
            'scrape_frequency_hours': 12,
            'max_pages': 2,
            'product_selector': '[data-test="component-product-card"]',
            'title_selector': '[data-test="product-title"]',
            'price_selector': '[data-test="product-price"]',
            'image_selector': '[data-test="product-image"] img',
            'url_selector': '[data-test="product-link"]',
            'status': 'active'
        },
        {
            'name': 'John Lewis & Partners',
            'base_url': 'https://www.johnlewis.com',
            'search_url_template': 'https://www.johnlewis.com/search?search-term={query}',
            'site_type': 'custom',
            'scrape_frequency_hours': 8,
            'max_pages': 2,
            'product_selector': '.product-card',
            'title_selector': '.product-card__title',
            'price_selector': '.product-card__price',
            'image_selector': '.product-card__image img',
            'url_selector': '.product-card__link',
            'status': 'active'
        },
        {
            'name': 'ASDA George',
            'base_url': 'https://groceries.asda.com',
            'search_url_template': 'https://groceries.asda.com/search/{query}',
            'site_type': 'custom',
            'scrape_frequency_hours': 12,
            'max_pages': 2,
            'product_selector': '.product-item',
            'title_selector': '.product-name',
            'price_selector': '.product-price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
            'status': 'active'
        },
        {
            'name': 'Demo UK Retailer',
            'base_url': 'https://example-uk-store.co.uk',
            'search_url_template': 'https://example-uk-store.co.uk/search?q={query}',
            'site_type': 'custom',
            'scrape_frequency_hours': 24,
            'max_pages': 1,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.product-price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
            'status': 'active'
        },
    ]
    
    created_targets = []
    for target_data in sample_targets:
        try:
            target, created = ScrapeTarget.objects.get_or_create(
                name=target_data['name'],
                defaults=target_data
            )
            
            if created:
                print(f"✅ Created scraping target: {target.name}")
                print(f"   🎯 Site: {target.site_type}")
                print(f"   ⏰ Every {target.scrape_frequency_hours} hrs")
                print(f"   📊 Status: {target.status}")
            else:
                print(f"📁 Target already exists: {target.name}")
                
            created_targets.append(target)
            
        except Exception as e:
            print(f"❌ Error creating target {target_data['name']}: {e}")
    
    print("\n🎉 Scraping targets setup complete!")
    print(f"🎯 Total targets: {ScrapeTarget.objects.count()}")
    print(f"✅ Active targets: {ScrapeTarget.objects.filter(status='active').count()}")
    print(f"🧪 Demo targets: {ScrapeTarget.objects.filter(status='demo').count()}")
    
    return created_targets


if __name__ == '__main__':
    create_sample_scraping_targets()
