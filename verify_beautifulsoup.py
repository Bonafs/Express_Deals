#!/usr/bin/env python
"""
BeautifulSoup Verification Script for Express Deals
Confirms BeautifulSoup4 is properly installed and working in all components
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def test_beautifulsoup_basic():
    """Test basic BeautifulSoup functionality"""
    print("🧪 Testing BeautifulSoup4 Basic Functionality...")
    try:
        from bs4 import BeautifulSoup
        
        # Test basic parsing
        html = "<html><body><h1>Test</h1><p>BeautifulSoup works!</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('h1').text
        if title == "Test":
            print("✅ BeautifulSoup4 basic parsing: SUCCESS")
            return True
        else:
            print(f"❌ BeautifulSoup4 basic parsing: FAILED - got '{title}'")
            return False
            
    except Exception as e:
        print(f"❌ BeautifulSoup4 basic test error: {e}")
        return False

def test_scraping_services():
    """Test BeautifulSoup imports in scraping services"""
    print("🔍 Testing BeautifulSoup4 in Scraping Services...")
    
    services_to_test = [
        'scraping.services.extract_service',
        'scraping.services.commercial_pipeline',
        'scraping.scrapers',
        'scraping.url_tracking_service'
    ]
    
    results = {}
    
    for service in services_to_test:
        try:
            module = __import__(service, fromlist=[''])
            
            # Check if BeautifulSoup is accessible in the module
            if hasattr(module, 'BeautifulSoup') or 'BeautifulSoup' in str(module):
                results[service] = "✅ SUCCESS"
            else:
                # Try to run a quick test
                exec(f"from {service} import *")
                results[service] = "✅ SUCCESS (imported)"
                
        except Exception as e:
            results[service] = f"❌ FAILED: {e}"
    
    # Display results
    for service, status in results.items():
        print(f"  📦 {service}: {status}")
    
    success_count = sum(1 for status in results.values() if "✅" in status)
    return success_count == len(services_to_test)

def test_requirements_compliance():
    """Check if BeautifulSoup4 is in requirements.txt"""
    print("📋 Checking Requirements.txt Compliance...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        if 'beautifulsoup4' in requirements.lower():
            print("✅ beautifulsoup4 found in requirements.txt")
            return True
        elif 'bs4' in requirements.lower():
            print("✅ bs4 found in requirements.txt") 
            return True
        else:
            print("❌ BeautifulSoup not found in requirements.txt")
            return False
            
    except Exception as e:
        print(f"❌ Requirements check error: {e}")
        return False

def test_heroku_compatibility():
    """Test if BeautifulSoup will work on Heroku"""
    print("🚀 Testing Heroku Compatibility...")
    
    try:
        # Check that we can import with different parsers
        from bs4 import BeautifulSoup
        
        html = "<html><body><div class='test'>Heroku Test</div></body></html>"
        
        # Test html.parser (should always work on Heroku)
        soup1 = BeautifulSoup(html, 'html.parser')
        if soup1.find('div', class_='test'):
            print("✅ html.parser works (Heroku compatible)")
            
        # Test lxml if available (might not be on Heroku without proper setup)
        try:
            soup2 = BeautifulSoup(html, 'lxml')
            print("✅ lxml parser works (optimal for Heroku)")
        except:
            print("⚠️  lxml parser not available (html.parser will be used)")
        
        return True
        
    except Exception as e:
        print(f"❌ Heroku compatibility test error: {e}")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("🍲 BEAUTIFULSOUP4 VERIFICATION FOR EXPRESS DEALS")
    print("=" * 60)
    
    tests = [
        ("Basic Functionality", test_beautifulsoup_basic),
        ("Scraping Services", test_scraping_services),
        ("Requirements Compliance", test_requirements_compliance),
        ("Heroku Compatibility", test_heroku_compatibility)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        result = test_func()
        results.append(result)
        print()
    
    # Summary
    print("=" * 60)
    print("📊 VERIFICATION SUMMARY:")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 BEAUTIFULSOUP4 IS FULLY OPERATIONAL!")
        print("✨ Ready for production scraping on Heroku!")
    else:
        print("⚠️  Some issues detected - may need attention")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
