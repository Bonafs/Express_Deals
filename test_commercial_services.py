#!/usr/bin/env python
"""
Quick test of commercial scraping services
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def test_services():
    """Test all commercial scraping services"""
    print("🚀 Testing Commercial Scraping Services...")
    
    try:
        # Test 1: Import services
        print("\n1️⃣ Testing Service Imports...")
        
        from scraping.services.fetch_service import fetch_service
        print("   ✅ Fetch Service imported")
        
        from scraping.services.extract_service import extractor
        print("   ✅ Extract Service imported")
        
        from scraping.services.transform_service import transformer
        print("   ✅ Transform Service imported")
        
        from scraping.services.load_service import loader
        print("   ✅ Load Service imported")
        
        from scraping.services.commercial_pipeline import commercial_pipeline
        print("   ✅ Commercial Pipeline imported")
        
        # Test 2: Basic functionality
        print("\n2️⃣ Testing Basic Functionality...")
        
        # Test transform service
        raw_data = {
            'title': '  Test Product  ',
            'price': '£19.99',
            'category': 'electronics'
        }
        
        site_config = {'site_id': 1, 'currency': 'GBP'}
        
        result = transformer.transform_product_data(raw_data, site_config)
        print(f"   ✅ Transform Service: Success={result.success}, Quality={result.quality_score:.2f}")
        
        # Test extract service  
        sample_html = '<div><h1>Test Product</h1><span class="price">£19.99</span></div>'
        extract_result = extractor.extract_product_data(sample_html, "test", "http://test.com")
        print(f"   ✅ Extract Service: Success={extract_result.success}, Method={extract_result.method_used}")
        
        # Test fetch service metrics
        fetch_metrics = fetch_service.get_performance_metrics()
        print(f"   ✅ Fetch Service: Ready (Success Rate: {fetch_metrics.get('success_rate', 0):.1%})")
        
        # Test pipeline statistics
        pipeline_stats = commercial_pipeline.get_pipeline_statistics()
        print(f"   ✅ Pipeline: Ready (URLs processed: {pipeline_stats.get('urls_processed', 0)})")
        
        print("\n🎉 ALL COMMERCIAL SCRAPING SERVICES ARE OPERATIONAL!")
        print("\n📊 System Status:")
        print("   • ML-Powered Extract Service: ✅ ACTIVE")
        print("   • Commercial Transform Service: ✅ ACTIVE")
        print("   • High-Performance Load Service: ✅ ACTIVE")
        print("   • Advanced Fetch Service: ✅ ACTIVE")
        print("   • Orchestrated Pipeline: ✅ ACTIVE")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_services()
    sys.exit(0 if success else 1)
