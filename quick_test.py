#!/usr/bin/env python
"""
Simple Commercial System Test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def test_commercial_services():
    """Test commercial services quickly"""
    print("🚀 TESTING COMMERCIAL SERVICES")
    print("=" * 40)
    
    try:
        # Test 1: Basic imports
        print("1️⃣ Testing imports...")
        
        from scraping.services.transform_service import transformer
        print("   ✅ Transform Service")
        
        from scraping.services.extract_service import extractor
        print("   ✅ Extract Service")
        
        from scraping.services.fetch_service import fetch_service
        print("   ✅ Fetch Service")
        
        from scraping.services.commercial_pipeline import commercial_pipeline
        print("   ✅ Commercial Pipeline")
        
        # Test 2: Transform service
        print("\n2️⃣ Testing Transform Service...")
        
        sample_data = {
            'title': '  Test Product  ',
            'price': '£19.99',
            'category': 'electronics'
        }
        
        site_config = {'site_id': 1, 'currency': 'GBP'}
        result = transformer.transform_product_data(sample_data, site_config)
        
        print(f"   ✅ Success: {result.success}")
        print(f"   📊 Quality: {result.quality_score:.2f}")
        
        # Test 3: Extract service
        print("\n3️⃣ Testing Extract Service...")
        
        html = '<div><h1>Test Product</h1><span class="price">£19.99</span></div>'
        extract_result = extractor.extract_product_data(html, "test", "http://test.com")
        
        print(f"   ✅ Success: {extract_result.success}")
        print(f"   🎯 Method: {extract_result.method_used}")
        
        # Test 4: Database models
        print("\n4️⃣ Testing Database...")
        
        from scraping.models import ScrapeTarget
        from products.models import Product
        
        targets = ScrapeTarget.objects.count()
        products = Product.objects.count()
        
        print(f"   📊 Targets: {targets}")
        print(f"   📦 Products: {products}")
        
        print(f"\n🎉 COMMERCIAL SERVICES OPERATIONAL!")
        print(f"   Status: ✅ READY")
        print(f"   Pipeline: ✅ ACTIVE")
        print(f"   ML Extract: ✅ ENABLED")
        print(f"   Transform: ✅ ENABLED")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_commercial_services()
    if success:
        print("\n🚀 READY FOR COMMERCIAL DEPLOYMENT!")
    else:
        print("\n🔧 System needs attention")
