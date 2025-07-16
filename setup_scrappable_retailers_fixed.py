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
            'search_url_template': 'https://www.overclockers.co.uk/search',
            'category': electronics,
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
            'product_selector': '.product',
            'title_selector': '.description',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.description a',
        },
        {
            'name': 'Box UK',
            'site_type': 'box',
            'base_url': 'https://www.box.co.uk',
            'search_url_template': 'https://www.box.co.uk/search?q={query}',
            'category': electronics,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-title a',
        },
        
        # Fashion (smaller/independent fashion retailers)
        {
            'name': 'Lounge Underwear',
            'site_type': 'lounge',
            'base_url': 'https://loungeunderwear.com',
            'search_url_template': 'https://loungeunderwear.com/search?q={query}',
            'category': fashion,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'In The Style',
            'site_type': 'inthestyle',
            'base_url': 'https://www.inthestyle.com',
            'search_url_template': 'https://www.inthestyle.com/search',
            'category': fashion,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Missguided',
            'site_type': 'missguided',
            'base_url': 'https://www.missguided.co.uk',
            'search_url_template': 'https://www.missguided.co.uk/search?q={query}',
            'category': fashion,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Joules',
            'site_type': 'joules',
            'base_url': 'https://www.joules.com',
            'search_url_template': 'https://www.joules.com/search?q={query}',
            'category': fashion,
            'product_selector': '.product-tile',
            'title_selector': '.product-name',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        
        # Home & Garden (smaller home retailers)
        {
            'name': 'Wayfair UK',
            'site_type': 'wayfair',
            'base_url': 'https://www.wayfair.co.uk',
            'search_url_template': 'https://www.wayfair.co.uk/keyword.php',
            'category': home,
            'product_selector': '.ProductCard',
            'title_selector': '.ProductCard-title',
            'price_selector': '.ProductCard-price',
            'image_selector': '.ProductCard-image img',
            'url_selector': '.ProductCard-title a',
        },
        {
            'name': 'Made.com',
            'site_type': 'made',
            'base_url': 'https://www.made.com',
            'search_url_template': 'https://www.made.com/search?q={query}',
            'category': home,
            'product_selector': '.product-tile',
            'title_selector': '.product-name',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Furniture Village',
            'site_type': 'furniture_village',
            'base_url': 'https://www.furniturevillage.co.uk',
            'search_url_template': 'https://www.furniturevillage.co.uk/search',
            'category': home,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Cox & Cox',
            'site_type': 'cox_cox',
            'base_url': 'https://www.coxandcox.co.uk',
            'search_url_template': 'https://www.coxandcox.co.uk/search?q={query}',
            'category': home,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        
        # Sports & Fitness (smaller sports retailers)
        {
            'name': 'Wiggle',
            'site_type': 'wiggle',
            'base_url': 'https://www.wiggle.co.uk',
            'search_url_template': 'https://www.wiggle.co.uk/search?q={query}',
            'category': sports,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Chain Reaction Cycles',
            'site_type': 'chain_reaction',
            'base_url': 'https://www.chainreactioncycles.com',
            'search_url_template': 'https://www.chainreactioncycles.com/search',
            'category': sports,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'ProBikeKit',
            'site_type': 'probikekit',
            'base_url': 'https://www.probikekit.com',
            'search_url_template': 'https://www.probikekit.com/search.list',
            'category': sports,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Start Fitness',
            'site_type': 'start_fitness',
            'base_url': 'https://www.startfitness.co.uk',
            'search_url_template': 'https://www.startfitness.co.uk/search?q={query}',
            'category': sports,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        
        # Books & Media (smaller book retailers)
        {
            'name': 'Book Depository',
            'site_type': 'book_depository',
            'base_url': 'https://www.bookdepository.com',
            'search_url_template': 'https://www.bookdepository.com/search',
            'category': books,
            'product_selector': '.book-item',
            'title_selector': '.title',
            'price_selector': '.price',
            'image_selector': '.item-img img',
            'url_selector': '.title a',
        },
        {
            'name': 'Blackwells',
            'site_type': 'blackwells',
            'base_url': 'https://blackwells.co.uk',
            'search_url_template': 'https://blackwells.co.uk/bookshop/search',
            'category': books,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Foyles',
            'site_type': 'foyles',
            'base_url': 'https://www.foyles.co.uk',
            'search_url_template': 'https://www.foyles.co.uk/search?q={query}',
            'category': books,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'WHSmith',
            'site_type': 'whsmith',
            'base_url': 'https://www.whsmith.co.uk',
            'search_url_template': 'https://www.whsmith.co.uk/search?q={query}',
            'category': books,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        
        # Toys & Games (smaller toy retailers)
        {
            'name': 'Smyths Toys',
            'site_type': 'smyths',
            'base_url': 'https://www.smythstoys.com',
            'search_url_template': 'https://www.smythstoys.com/search',
            'category': toys,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'The Entertainer',
            'site_type': 'entertainer',
            'base_url': 'https://www.thetoyshop.com',
            'search_url_template': 'https://www.thetoyshop.com/search?q={query}',
            'category': toys,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Toymaster',
            'site_type': 'toymaster',
            'base_url': 'https://www.toymaster.co.uk',
            'search_url_template': 'https://www.toymaster.co.uk/search?q={query}',
            'category': toys,
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        },
        {
            'name': 'Early Learning Centre',
            'site_type': 'elc',
            'base_url': 'https://www.elc.co.uk',
            'search_url_template': 'https://www.elc.co.uk/search?q={query}',
            'category': toys,
            'product_selector': '.product',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link',
        }
    ]
    
    # Create scrappable targets
    for target_data in scrappable_targets:
        target = ScrapeTarget.objects.create(
            name=target_data['name'],
            site_type=target_data['site_type'],
            base_url=target_data['base_url'],
            search_url_template=target_data['search_url_template'],
            status='active',
            category=target_data['category'],
            product_selector=target_data['product_selector'],
            title_selector=target_data['title_selector'],
            price_selector=target_data['price_selector'],
            image_selector=target_data['image_selector'],
            url_selector=target_data['url_selector'],
        )
        print(f"✅ Added: {target.name}")
    
    print("\n🎯 SETUP COMPLETE!")
    print(f"   Total Scrappable Targets: {ScrapeTarget.objects.count()}")
    print(f"   Categories: {Category.objects.count()}")
    
    print("\n📋 TARGET CATEGORIES:")
    for category in Category.objects.all():
        count = ScrapeTarget.objects.filter(category=category).count()
        print(f"   {category.name}: {count} retailers")
    
    print("\n✅ READY TO SCRAPE ACTUAL PRODUCTS!")
    return True

if __name__ == "__main__":
    setup_scrappable_uk_retailers()
