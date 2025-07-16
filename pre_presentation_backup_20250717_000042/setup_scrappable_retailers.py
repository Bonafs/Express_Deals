#!/usr/bin/env python3
"""
Setup Scrappable UK Retailers
Replace top 24 protected retailers with 24 UK retailers that CAN actually be scraped
Focus on smaller sites, niche retailers, and sites with APIs/feeds
"""

import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.models import ScrapeTarget
from products.models import Category

def setup_scrappable_uk_retailers():
    """Replace protected retailers with actually scrappable UK sites"""
    
    print("🔧 REPLACING PROTECTED RETAILERS WITH SCRAPPABLE ONES")
    print("=" * 60)
    
    # Clear existing targets
    ScrapeTarget.objects.all().delete()
    print("🗑️ Cleared existing protected targets")
    
    # Categories with proper slugs
    electronics, _ = Category.objects.get_or_create(
        name='Electronics', 
        defaults={
            'slug': slugify('Electronics'),
            'description': 'Electronic devices and accessories'
        }
    )
    fashion, _ = Category.objects.get_or_create(
        name='Fashion', 
        defaults={
            'slug': slugify('Fashion'),
            'description': 'Clothing and accessories'
        }
    )
    home, _ = Category.objects.get_or_create(
        name='Home & Garden', 
        defaults={
            'slug': slugify('Home & Garden'),
            'description': 'Home improvement and garden items'
        }
    )
    sports, _ = Category.objects.get_or_create(
        name='Sports & Fitness', 
        defaults={
            'slug': slugify('Sports & Fitness'),
            'description': 'Sports equipment and fitness gear'
        }
    )
    books, _ = Category.objects.get_or_create(
        name='Books & Media', 
        defaults={
            'slug': slugify('Books & Media'),
            'description': 'Books, movies, and media'
        }
    )
    toys, _ = Category.objects.get_or_create(
        name='Toys & Games', 
        defaults={
            'slug': slugify('Toys & Games'),
            'description': 'Children toys and games'
        }
    )
    
    # 24 Actually Scrappable UK Retailers
    scrappable_targets = [
        # Electronics & Tech (smaller/independent retailers)
        {
            'name': 'Ebuyer UK',
            'site_type': 'ebuyer',
            'base_url': 'https://www.ebuyer.com',
            'search_url_template': 'https://www.ebuyer.com/search?q={query}',
            'category': electronics,
            'status': 'active',
            'product_selector': '.grid-item',
            'title_selector': '.item-name',
            'price_selector': '.price-inc',
            'image_selector': '.item-img img',
            'url_selector': '.item-name a',
        },
        {
            'name': 'Overclockers UK',
            'site_type': 'overclockers',
            'base_url': 'https://www.overclockers.co.uk',
            'search_url_template': 'https://www.overclockers.co.uk/search?sSearch={query}',
            'category': electronics,
            'status': 'active',
            'product_selector': '.productItem',
            'title_selector': '.productTitle',
            'price_selector': '.productPrice',
            'image_selector': '.productImage img',
            'url_selector': '.productTitle a',
        },
        {
            'name': 'Scan UK',
            'site_type': 'scan',
            'base_url': 'https://www.scan.co.uk',
            'search_url_template': 'https://www.scan.co.uk/search?q={query}',
            'category': electronics,
            'status': 'active',
            'product_selector': '.product',
            'title_selector': '.description',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.description a',
        },
        {
            'name': 'Novatech',
            'site_type': 'novatech',
            'base_url': 'https://www.novatech.co.uk',
            'search_url': 'https://www.novatech.co.uk/search/{query}',
            'category': electronics,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Box UK',
            'site_type': 'box',
            'base_url': 'https://www.box.co.uk',
            'search_url': 'https://www.box.co.uk/search?search={query}',
            'category': electronics,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Maplin',
            'site_type': 'maplin',
            'base_url': 'https://www.maplin.co.uk',
            'search_url': 'https://www.maplin.co.uk/search?text={query}',
            'category': electronics,
            'is_api_available': False,
            'status': 'active',
        },
        
        # Fashion (independent/smaller retailers)
        {
            'name': 'Boohoo UK',
            'site_type': 'boohoo',
            'base_url': 'https://www.boohoo.com',
            'search_url': 'https://www.boohoo.com/search?query={query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Nasty Gal UK',
            'site_type': 'nastygal',
            'base_url': 'https://www.nastygal.com',
            'search_url': 'https://www.nastygal.com/search?q={query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'PrettyLittleThing',
            'site_type': 'prettylittlething',
            'base_url': 'https://www.prettylittlething.com',
            'search_url': 'https://www.prettylittlething.com/search/{query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Missguided UK',
            'site_type': 'missguided',
            'base_url': 'https://www.missguided.com',
            'search_url': 'https://www.missguided.com/search?query={query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'In The Style',
            'site_type': 'inthestyle',
            'base_url': 'https://www.inthestyle.com',
            'search_url': 'https://www.inthestyle.com/search?type=product&q={query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Topman UK',
            'site_type': 'topman',
            'base_url': 'https://www.topman.com',
            'search_url': 'https://www.topman.com/search?q={query}',
            'category': fashion,
            'is_api_available': False,
            'status': 'active',
        },
        
        # Home & Garden (independent retailers)
        {
            'name': 'Wayfair UK',
            'site_type': 'wayfair',
            'base_url': 'https://www.wayfair.co.uk',
            'search_url': 'https://www.wayfair.co.uk/keyword.php?keyword={query}',
            'category': home,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Made.com',
            'site_type': 'made',
            'base_url': 'https://www.made.com',
            'search_url': 'https://www.made.com/search?q={query}',
            'category': home,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Furniture Village',
            'site_type': 'furniture_village',
            'base_url': 'https://www.furniturevillage.co.uk',
            'search_url': 'https://www.furniturevillage.co.uk/search?q={query}',
            'category': home,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'The White Company',
            'site_type': 'white_company',
            'base_url': 'https://www.thewhitecompany.com',
            'search_url': 'https://www.thewhitecompany.com/search/?q={query}',
            'category': home,
            'is_api_available': False,
            'status': 'active',
        },
        
        # Sports & Fitness
        {
            'name': 'Decathlon UK',
            'site_type': 'decathlon',
            'base_url': 'https://www.decathlon.co.uk',
            'search_url': 'https://www.decathlon.co.uk/search?Ntt={query}',
            'category': sports,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Sports Direct',
            'site_type': 'sports_direct',
            'base_url': 'https://www.sportsdirect.com',
            'search_url': 'https://www.sportsdirect.com/search/{query}',
            'category': sports,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'ProBikeKit',
            'site_type': 'probikekit',
            'base_url': 'https://www.probikekit.com',
            'search_url': 'https://www.probikekit.com/search.list?search={query}',
            'category': sports,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Wiggle UK',
            'site_type': 'wiggle',
            'base_url': 'https://www.wiggle.com',
            'search_url': 'https://www.wiggle.com/search?term={query}',
            'category': sports,
            'is_api_available': False,
            'status': 'active',
        },
        
        # Books & Media
        {
            'name': 'Book Depository',
            'site_type': 'book_depository',
            'base_url': 'https://www.bookdepository.com',
            'search_url': 'https://www.bookdepository.com/search?searchTerm={query}',
            'category': books,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Blackwells',
            'site_type': 'blackwells',
            'base_url': 'https://blackwells.co.uk',
            'search_url': 'https://blackwells.co.uk/bookshop/search/{query}',
            'category': books,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'Foyles',
            'site_type': 'foyles',
            'base_url': 'https://www.foyles.co.uk',
            'search_url': 'https://www.foyles.co.uk/witem/all/{query}',
            'category': books,
            'is_api_available': False,
            'status': 'active',
        },
        
        # Toys & Games
        {
            'name': 'Smyths Toys',
            'site_type': 'smyths',
            'base_url': 'https://www.smythstoys.com',
            'search_url': 'https://www.smythstoys.com/uk/en-gb/search/{query}',
            'category': toys,
            'is_api_available': False,
            'status': 'active',
        },
        {
            'name': 'The Entertainer',
            'site_type': 'entertainer',
            'base_url': 'https://www.thetoyshop.com',
            'search_url': 'https://www.thetoyshop.com/search?q={query}',
            'category': toys,
            'is_api_available': False,
            'status': 'active',
        }
    ]
    
    # Create scrappable targets
    for target_data in scrappable_targets:
        target = ScrapeTarget.objects.create(
            name=target_data['name'],
            site_type=target_data['site_type'],
            base_url=target_data['base_url'],
            search_url=target_data['search_url'],
            status=target_data['status'],
            is_api_available=target_data['is_api_available'],
            category=target_data['category'],
            # Basic selectors that work on most sites
            name_selector='h1, .product-title, .product-name, h2.product-title',
            price_selector='.price, .product-price, .current-price, .sale-price',
            image_selector='img.product-image, .product-img img, .main-image img',
            url_selector='a.product-link, .product-url',
        )
        print(f"✅ Added: {target.name}")
    
    print(f"\n🎯 SETUP COMPLETE!")
    print(f"   Total Scrappable Targets: {ScrapeTarget.objects.count()}")
    print(f"   Categories: {Category.objects.count()}")
    
    print(f"\n📋 TARGET CATEGORIES:")
    for category in Category.objects.all():
        count = ScrapeTarget.objects.filter(category=category).count()
        print(f"   {category.name}: {count} retailers")
    
    return ScrapeTarget.objects.count()

if __name__ == "__main__":
    setup_scrappable_uk_retailers()
