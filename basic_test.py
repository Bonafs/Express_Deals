#!/usr/bin/env python
"""
EXPRESS DEALS - SIMPLE TEST
Test the basic setup
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

print("🚀 TESTING EXPRESS DEALS SYSTEM")
print("=" * 40)

try:
    from scraping.models import ScrapeTarget
    print("✅ ScrapeTarget model imported")
    
    # Count targets
    total = ScrapeTarget.objects.count()
    active = ScrapeTarget.objects.filter(status='active').count()
    
    print(f"📊 Total targets: {total}")
    print(f"📊 Active targets: {active}")
    
    if active == 0:
        print("🎯 Creating test target...")
        target = ScrapeTarget.objects.create(
            name="Test Target",
            site_type="custom",
            base_url="https://example.com",
            search_url_template="https://example.com/search?q={query}",
            status="active",
            product_selector=".product",
            title_selector=".title", 
            price_selector=".price",
            image_selector=".image",
            url_selector=".link"
        )
        print(f"✅ Created: {target.name}")
    
    print("\n🎉 SYSTEM TEST SUCCESSFUL!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("🏁 Test complete")
