#!/usr/bin/env python3
"""
Aggressive Live Product Scraping
Get actual products from our 24 scrappable retailers NOW
"""

import os
import sys
import django
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category
from scraping.models import ScrapeTarget, ScrapeJob

def get_live_products_now():
    """Aggressively scrape products from our 24 retailers"""
    
    print("🚀 AGGRESSIVE LIVE PRODUCT SCRAPING")
    print("=" * 50)
    
    # Check current state
    current_products = Product.objects.count()
    targets = ScrapeTarget.objects.filter(status='active')
    
    print(f"📊 Current Products: {current_products}")
    print(f"🎯 Active Targets: {targets.count()}")
    
    if targets.count() == 0:
        print("❌ No active targets! Run setup_scrappable_retailers_fixed.py first")
        return
    
    # User agents for rotation
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    ]
    
    # Simple search queries that usually return results
    search_queries = [
        'laptop',
        'phone',
        'headphones',
        'book',
        'shirt',
        'shoes',
        'chair',
        'table',
        'toy',
        'watch',
    ]
    
    products_scraped = 0
    
    # Try each target
    for target in targets[:5]:  # Limit to first 5 to avoid overwhelming
        print(f"\n🔍 Scraping: {target.name}")
        
        try:
            # Create session
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-GB,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            })
            
            # Try a simple search
            query = random.choice(search_queries)
            search_url = target.search_url_template.replace('{query}', query)
            
            print(f"   🔎 Searching: {search_url}")
            
            response = session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to find products using basic selectors
                product_elements = soup.select('.product, .item, .listing, [class*="product"], [class*="item"]')
                
                print(f"   📦 Found {len(product_elements)} potential products")
                
                for i, element in enumerate(product_elements[:3]):  # Limit to 3 per target
                    try:
                        # Extract product data using multiple selector strategies
                        name = extract_text(element, [
                            'h1, h2, h3, h4, h5, h6',
                            '.title, .name, .product-title, .product-name',
                            '[class*="title"], [class*="name"]',
                            'a'
                        ])
                        
                        price_text = extract_text(element, [
                            '.price, .cost, .amount',
                            '[class*="price"], [class*="cost"]',
                            '.currency, .money'
                        ])
                        
                        image_url = extract_image(element, target.base_url)
                        
                        # Process price
                        price = extract_price(price_text)
                        
                        if name and price and price > 0:
                            # Create product
                            product = Product.objects.create(
                                name=name[:200],  # Limit name length
                                description=f"Live scraped from {target.name}",
                                price=price,
                                category=target.category,
                                stock_status='in_stock',
                                is_active=True,
                                is_featured=True,
                                sku=f"{target.site_type}_{int(time.time())}_{i}",
                                source_url=search_url,
                            )
                            
                            # Try to set image if we found one
                            if image_url:
                                try:
                                    product.image_url = image_url
                                    product.save()
                                except:
                                    pass  # Continue even if image fails
                            
                            products_scraped += 1
                            print(f"   ✅ Added: {name} - £{price}")
                            
                            if products_scraped >= 20:  # Stop after 20 products
                                print("🎯 Reached target of 20 products!")
                                break
                    
                    except Exception as e:
                        print(f"   ⚠️ Error processing product: {str(e)}")
                        continue
                
            else:
                print(f"   ❌ Failed to fetch: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error scraping {target.name}: {str(e)}")
        
        # Break if we have enough products
        if products_scraped >= 20:
            break
            
        # Delay between requests
        time.sleep(random.uniform(1, 3))
    
    # Final report
    final_count = Product.objects.count()
    print(f"\n🎯 SCRAPING COMPLETE!")
    print(f"   Products before: {current_products}")
    print(f"   Products after: {final_count}")
    print(f"   New products: {final_count - current_products}")
    
    # Show sample products
    print(f"\n📦 SAMPLE PRODUCTS:")
    for product in Product.objects.all()[:5]:
        print(f"   • {product.name} - £{product.price} ({product.category.name if product.category else 'No Category'})")
    
    return final_count

def extract_text(element, selectors):
    """Extract text using multiple selector strategies"""
    for selector in selectors:
        try:
            found = element.select_one(selector)
            if found and found.get_text(strip=True):
                return found.get_text(strip=True)
        except:
            continue
    return None

def extract_image(element, base_url):
    """Extract image URL"""
    try:
        img = element.select_one('img')
        if img and img.get('src'):
            src = img.get('src')
            if src.startswith('http'):
                return src
            elif src.startswith('/'):
                return urljoin(base_url, src)
    except:
        pass
    return None

def extract_price(price_text):
    """Extract numeric price from text"""
    if not price_text:
        return 0
    
    import re
    # Find price patterns
    price_match = re.search(r'[\£\$]?(\d+\.?\d*)', price_text.replace(',', ''))
    if price_match:
        try:
            return float(price_match.group(1))
        except:
            pass
    
    # Try finding just numbers
    numbers = re.findall(r'\d+\.?\d*', price_text)
    if numbers:
        try:
            price = float(numbers[0])
            # Reasonable price range
            if 0.01 <= price <= 10000:
                return price
        except:
            pass
    
    return 0

if __name__ == "__main__":
    get_live_products_now()
