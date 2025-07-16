#!/usr/bin/env python3
"""
Quick Test Scraper - Get some sample products immediately
"""

import os
import django
import requests
from bs4 import BeautifulSoup
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category
from scraping.models import ScrapeTarget
import cloudinary.uploader

def quick_scrape_test():
    """Quick scrape test to get immediate products"""
    
    print("🚀 QUICK SCRAPE TEST")
    print("=" * 30)
    
    # Get a few targets to test
    targets = ScrapeTarget.objects.filter(status='active')[:3]
    
    if not targets.exists():
        print("❌ No active targets found")
        return
    
    # Simple scraping without all the enterprise features
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    products_created = 0
    
    for target in targets:
        print(f"\n🎯 Testing: {target.name}")
        
        try:
            # Simple search for common products
            search_queries = ['laptop', 'phone', 'book', 'toy']
            
            for query in search_queries[:2]:  # Test 2 queries per target
                print(f"   Searching: {query}")
                
                # Build search URL
                search_url = target.search_url_template.replace('{query}', query)
                
                # Simple request
                response = session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try to find products using basic selectors
                    product_elements = soup.select('div[class*="product"], .product-item, .product, [class*="item"]')[:2]
                    
                    for element in product_elements:
                        try:
                            # Extract basic data
                            title_elem = element.select_one('h2, h3, .title, [class*="title"], [class*="name"]')
                            price_elem = element.select_one('.price, [class*="price"], .cost')
                            
                            if title_elem and price_elem:
                                title = title_elem.get_text().strip()
                                price_text = price_elem.get_text().strip()
                                
                                # Extract price number
                                import re
                                price_match = re.search(r'[\d.]+', price_text.replace(',', ''))
                                price = float(price_match.group()) if price_match else 9.99
                                
                                # Create product
                                product = Product.objects.create(
                                    name=title[:200],  # Limit name length
                                    price=price,
                                    description=f"Product from {target.name}",
                                    category=target.category,
                                    stock_quantity=10,
                                    is_active=True,
                                    is_featured=products_created < 5  # First 5 are featured
                                )
                                
                                print(f"      ✅ Created: {product.name} - £{product.price}")
                                products_created += 1
                                
                                if products_created >= 15:  # Stop at 15 products
                                    break
                                    
                        except Exception as e:
                            print(f"      ⚠️ Error processing element: {e}")
                            continue
                    
                else:
                    print(f"   ❌ Failed to fetch: {response.status_code}")
                
                if products_created >= 15:
                    break
                    
                time.sleep(1)  # Be respectful
                
        except Exception as e:
            print(f"   ❌ Error with {target.name}: {e}")
            continue
        
        if products_created >= 15:
            break
    
    print(f"\n🎯 QUICK SCRAPE COMPLETE!")
    print(f"   Products Created: {products_created}")
    print(f"   Total Products: {Product.objects.count()}")
    
    # Show sample products
    if products_created > 0:
        print(f"\n📦 SAMPLE PRODUCTS:")
        for product in Product.objects.order_by('-id')[:5]:
            print(f"   • {product.name} - £{product.price}")
    
    return products_created

if __name__ == "__main__":
    quick_scrape_test()
