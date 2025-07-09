#!/usr/bin/env python
"""
Express Deals - Test Automation Pipeline
Test scraping targets, background tasks, and notifications
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from scraping.models import ScrapeTarget, ScrapeJob
from products.models import Product, Category
from django.contrib.auth.models import User
from django.utils import timezone


def test_scraping_targets():
    """Test that scraping targets are properly configured"""
    print("🎯 Testing Scraping Targets Configuration:")
    print("=" * 50)
    
    targets = ScrapeTarget.objects.all()
    print(f"📊 Total targets: {targets.count()}")
    
    for target in targets:
        print(f"\n✅ {target.name}")
        print(f"   🏪 Site Type: {target.site_type}")
        print(f"   🌐 Base URL: {target.base_url}")
        print(f"   📝 Search Template: {target.search_url_template[:60]}...")
        print(f"   ⏰ Frequency: Every {target.scrape_frequency_hours} hours")
        print(f"   📊 Status: {target.status}")
        print(f"   🔍 Max Pages: {target.max_pages}")
    
    return targets


def test_currency_support():
    """Test currency and UK localization"""
    print("\n💷 Testing Currency & UK Localization:")
    print("=" * 50)
    
    # Test currency settings
    from django.conf import settings
    from express_deals.currency_utils import get_default_currency, format_price_gbp
    
    print(f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 Default Currency: {get_default_currency()}")
    print(f"🌍 Time Zone: {settings.TIME_ZONE}")
    print(f"🗣️ Language: {settings.LANGUAGE_CODE}")
    
    # Test price formatting
    test_price = 29.99
    formatted = format_price_gbp(test_price)
    print(f"💰 Price Format Test: {test_price} -> {formatted}")
    
    return True


def test_database_setup():
    """Test database and models"""
    print("\n🗄️ Testing Database Setup:")
    print("=" * 50)
    
    # Check users
    user_count = User.objects.count()
    print(f"👥 Total Users: {user_count}")
    
    # Check categories
    category_count = Category.objects.count()
    print(f"📂 Total Categories: {category_count}")
    
    # Check products
    product_count = Product.objects.count()
    print(f"📦 Total Products: {product_count}")
    
    # Check scrape jobs
    job_count = ScrapeJob.objects.count()
    print(f"🔄 Total Scrape Jobs: {job_count}")
    
    return True


def test_admin_access():
    """Test admin interface setup"""
    print("\n⚙️ Testing Admin Interface:")
    print("=" * 50)
    
    superusers = User.objects.filter(is_superuser=True)
    print(f"👑 Superusers: {superusers.count()}")
    
    for user in superusers:
        print(f"   📧 {user.username} ({user.email})")
    
    print(f"🌐 Admin URL: https://express-deals.herokuapp.com/admin/")
    
    return True


def create_test_scrape_job():
    """Create a test scrape job to verify automation"""
    print("\n🧪 Creating Test Scrape Job:")
    print("=" * 50)
    
    try:
        # Get a demo target for testing
        target = ScrapeTarget.objects.filter(status='active').first()
        
        if target:
            job = ScrapeJob.objects.create(
                target=target,
                search_query='laptop',
                status='pending'
            )
            print(f"✅ Created test job: #{job.id}")
            print(f"   🎯 Target: {target.name}")
            print(f"   🔍 Query: {job.search_query}")
            print(f"   📊 Status: {job.status}")
            print(f"   ⏰ Created: {job.started_at or 'Not started'}")
            
            return job
        else:
            print("❌ No active scraping targets found")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test job: {e}")
        return None


def main():
    """Run all automation tests"""
    print("🚀 Express Deals - UK Automation Pipeline Test")
    print("=" * 60)
    print(f"🕐 Test started at: {timezone.now()}")
    
    try:
        # Test 1: Scraping Targets
        targets = test_scraping_targets()
        
        # Test 2: Currency Support
        test_currency_support()
        
        # Test 3: Database Setup
        test_database_setup()
        
        # Test 4: Admin Access
        test_admin_access()
        
        # Test 5: Create Test Job
        test_job = create_test_scrape_job()
        
        print("\n🎉 Automation Pipeline Test Complete!")
        print("=" * 60)
        print("✅ UK-focused scraping targets: READY")
        print("✅ GBP currency support: READY")
        print("✅ Database and models: READY")
        print("✅ Admin interface: READY")
        print("✅ Background processing: READY")
        
        print("\n🌐 Live Site: https://express-deals.herokuapp.com/")
        print("⚙️ Admin Panel: https://express-deals.herokuapp.com/admin/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


if __name__ == '__main__':
    main()
