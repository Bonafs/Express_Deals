#!/usr/bin/env python3
"""
Comprehensive retailer validation test for Express Deals URL Tracking Service
Tests all supported retailers and validates the parameter order consistency
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from scraping.url_tracking_service import url_tracking_service


def test_all_retailers():
    """Test validation for all supported retailers"""
    
    test_urls = {
        'Amazon UK': [
            'https://www.amazon.co.uk/dp/B08N5WRWNW',
            'https://amazon.co.uk/gp/product/B08N5WRWNW'
        ],
        'Currys PC World': [
            'https://www.currys.co.uk/products/test-product-123.html',
            'https://currys.co.uk/products/apple-iphone-15-pro.html'
        ],
        'John Lewis': [
            'https://www.johnlewis.com/apple-iphone-15-pro-128gb/p5972568',
            'https://johnlewis.com/samsung-galaxy-s24-ultra/p6123456'
        ],
        'Argos': [
            'https://www.argos.co.uk/product/8349807',
            'https://argos.co.uk/product/1234567'
        ],
        'ASOS': [
            'https://www.asos.com/nike/nike-air-max-90/prd/123456',
            'https://asos.com/adidas/adidas-originals/prd/789012'
        ],
        'Next': [
            'https://www.next.co.uk/style/st123456/789012',
            'https://next.co.uk/g12345'
        ]
    }
    
    print("=" * 80)
    print("EXPRESS DEALS - COMPREHENSIVE RETAILER VALIDATION TEST")
    print("=" * 80)
    
    print(f"\n{'Retailer':<20} | {'URL':<60} | {'Valid':<6} | {'Detected':<20} | Error")
    print("-" * 115)
    
    total_tests = 0
    passed_tests = 0
    
    for retailer, urls in test_urls.items():
        for url in urls:
            total_tests += 1
            try:
                is_valid, detected_retailer, error = url_tracking_service.validate_url(url)
                status = '✅' if is_valid else '❌'
                
                if is_valid and detected_retailer:
                    passed_tests += 1
                
                print(f"{status} {retailer:<17} | {url:<58} | {str(is_valid):<6} | {str(detected_retailer):<20} | {error or 'None'}")
                
            except Exception as e:
                print(f"❌ {retailer:<17} | {url:<58} | ERROR | Exception: {str(e)}")
    
    print("-" * 115)
    print(f"\nTEST RESULTS: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    return passed_tests == total_tests


def test_parameter_order_consistency():
    """Test that all methods use validate_url with correct parameter order"""
    
    print("\n" + "=" * 80)
    print("PARAMETER ORDER CONSISTENCY TEST")
    print("=" * 80)
    
    test_url = "https://www.currys.co.uk/products/test-product.html"
    
    try:
        # Test validate_url directly
        is_valid, retailer_name, error_message = url_tracking_service.validate_url(test_url)
        print(f"✅ validate_url() returns: (is_valid={is_valid}, retailer='{retailer_name}', error='{error_message}')")
        
        # Test methods that use validate_url
        methods_to_test = [
            'get_tracking_effectiveness',
            'check_product_availability',
            'get_url_tracking_info'
        ]
        
        for method_name in methods_to_test:
            try:
                method = getattr(url_tracking_service, method_name)
                result = method(test_url)
                print(f"✅ {method_name}() executed successfully")
            except Exception as e:
                print(f"❌ {method_name}() failed: {str(e)}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Parameter order test failed: {str(e)}")
        return False


def test_future_retailer_compatibility():
    """Test framework for adding new retailers"""
    
    print("\n" + "=" * 80)
    print("FUTURE RETAILER COMPATIBILITY TEST")
    print("=" * 80)
    
    # Test framework for adding new retailers
    new_retailer_config = {
        'test-retailer.co.uk': {
            'name': 'Test Retailer',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.stock',
            'requires_headers': True
        }
    }
    
    # Temporarily add the new retailer
    original_retailers = url_tracking_service.SUPPORTED_RETAILERS.copy()
    url_tracking_service.SUPPORTED_RETAILERS.update(new_retailer_config)
    
    try:
        test_url = "https://www.test-retailer.co.uk/products/test-item"
        is_valid, retailer_name, error = url_tracking_service.validate_url(test_url)
        
        if is_valid and retailer_name == "Test Retailer":
            print("✅ New retailer addition framework works correctly")
            success = True
        else:
            print(f"❌ New retailer addition failed: valid={is_valid}, retailer='{retailer_name}'")
            success = False
            
    except Exception as e:
        print(f"❌ New retailer test failed: {str(e)}")
        success = False
    finally:
        # Restore original retailers
        url_tracking_service.SUPPORTED_RETAILERS = original_retailers
    
    return success


def show_supported_retailers():
    """Display all currently supported retailers"""
    
    print("\n" + "=" * 80)
    print("CURRENTLY SUPPORTED RETAILERS")
    print("=" * 80)
    
    print(f"{'Domain':<25} | {'Retailer Name'}")
    print("-" * 50)
    
    for domain, config in url_tracking_service.SUPPORTED_RETAILERS.items():
        print(f"{domain:<25} | {config['name']}")
    
    print(f"\nTotal: {len(url_tracking_service.SUPPORTED_RETAILERS)} supported retailers")


if __name__ == "__main__":
    print("Starting comprehensive retailer validation tests...\n")
    
    # Run all tests
    test1_passed = test_all_retailers()
    test2_passed = test_parameter_order_consistency()
    test3_passed = test_future_retailer_compatibility()
    
    show_supported_retailers()
    
    # Summary
    print("\n" + "=" * 80)
    print("FINAL TEST SUMMARY")
    print("=" * 80)
    
    tests = [
        ("Retailer URL Validation", test1_passed),
        ("Parameter Order Consistency", test2_passed), 
        ("Future Retailer Compatibility", test3_passed)
    ]
    
    all_passed = all(passed for _, passed in tests)
    
    for test_name, passed in tests:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<30}: {status}")
    
    print("-" * 50)
    overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
    print(f"{'OVERALL RESULT':<30}: {overall_status}")
    print("=" * 80)
    
    sys.exit(0 if all_passed else 1)
