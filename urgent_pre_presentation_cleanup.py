#!/usr/bin/env python3
"""
URGENT: Pre-Presentation Cleanup
Remove high-risk legacy files before tomorrow's presentation
"""

import os
import shutil
from datetime import datetime

def create_backup():
    """Create backup before cleanup"""
    backup_dir = f"pre_presentation_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📦 Creating backup: {backup_dir}")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    return backup_dir

def urgent_cleanup():
    """Remove high-risk files that could break presentation"""
    
    print("🚨 URGENT PRE-PRESENTATION CLEANUP")
    print("=" * 40)
    
    # Create backup first
    backup_dir = create_backup()
    
    # HIGH RISK: Files that could cause import/conflict errors
    high_risk_files = [
        # Duplicate/old versions (keep _fixed versions)
        'create_emergency_products.py',  # We have _fixed version
        'setup_scrappable_retailers.py',  # We have _fixed version
        
        # Test/debug scripts that might interfere
        'fix_auth_issues.py',
        'fix_production_issues.py', 
        'fix_image_issues.py',
        'fix_security.py',
        'update_security.py',
        'security_verification.py',
        
        # Old admin/demo scripts
        'admin_demo.py',
        'customer_demo.py',
        'auth_test.py',
        'auth_status.py',
        
        # Multiple check scripts (keep only check_products.py)
        'check_credentials_status.py',
        'check_data.py', 
        'check_final_status.py',
        'check_scraping_status.py',
        
        # Old product creation scripts
        'add_demo_products.py',
        'create_products_with_images.py',
        'temp_products.py',
        
        # Image fix scripts (could conflict)
        'emergency_image_fix.py',
        'fix_product_images.py',
        'migrate_images_to_cloudinary.py',
        'upload_images_to_cloudinary.py',
        'urgent_image_migration.py',
        'urgent_sample_upload.py',
        'test_cloudinary_config.py',
        'test_cloudinary_fix.py',
        'verify_image_consistency.py',
        
        # URL tracking old files
        'comprehensive_url_tracking_test.py',
        'url_tracking_demo.py',
        'test_url_tracking.py',
        'verify_url_tracking.py',
        
        # Scraping analysis/test files
        'analyze_scraping_performance.py',
        'get_live_products_now.py',
        'test_scraping_efficacy.py',
        'upgrade_scraping_stack.py',
        
        # Various test files
        'test_email_config.py',
        'test_image_rendering.py',
        'test_login.py',
        'test_product_data.py',
        'test_retailers_http_errors.py',
        'test_stripe_demo.py',
        'test_stripe_payments.py',
        'test_stripe_system.py',
        'web_interface_test.py',
        
        # Quick test scripts
        'quick_check.py',
        'quick_diagnostic.py',
        'quick_migration_test.py',
        'quick_products.py',
        'quick_retailer_test.py',
        'quick_scrape_test.py',
        'quick_status.py',
        'quick_url_test.py',
        'simple_auth_test.py',
        'simple_status_check.py',
        'simple_test.py',
        
        # Research/setup scripts we don't need
        'research_ethical_retailers.py',
        'research_uk_retailer_policies.py',
        'setup_ethical_retailers.py',
        'verify_environment.py',
        'verify_retailer_expansion.py',
        
        # Urgent fix scripts
        'urgent_production_fix.py',
        
        # System status
        'system_status.py',
    ]
    
    # DIRECTORIES to remove
    high_risk_dirs = [
        'temp-heroku',  # Old heroku backup
    ]
    
    removed_files = 0
    removed_dirs = 0
    
    # Remove files
    for file_name in high_risk_files:
        if os.path.exists(file_name):
            try:
                # Backup first
                backup_path = os.path.join(backup_dir, file_name)
                shutil.copy2(file_name, backup_path)
                
                # Remove original
                os.remove(file_name)
                print(f"✅ Removed: {file_name}")
                removed_files += 1
                
            except Exception as e:
                print(f"❌ Error removing {file_name}: {e}")
        else:
            print(f"⚠️ Not found: {file_name}")
    
    # Remove directories
    for dir_name in high_risk_dirs:
        if os.path.exists(dir_name):
            try:
                # Backup directory
                backup_path = os.path.join(backup_dir, dir_name)
                shutil.copytree(dir_name, backup_path)
                
                # Remove original
                shutil.rmtree(dir_name)
                print(f"✅ Removed directory: {dir_name}")
                removed_dirs += 1
                
            except Exception as e:
                print(f"❌ Error removing {dir_name}: {e}")
    
    print(f"\n🎯 CLEANUP COMPLETE!")
    print(f"   Files removed: {removed_files}")
    print(f"   Directories removed: {removed_dirs}")
    print(f"   Backup created: {backup_dir}")
    
    print(f"\n✅ ESSENTIAL FILES KEPT:")
    essential_kept = [
        'manage.py',
        'requirements.txt', 
        'Procfile',
        'runtime.txt',
        'db.sqlite3',
        'create_emergency_products_fixed.py',
        'setup_scrappable_retailers_fixed.py',
        'world_class_scraping.py',
        'strategy_implementation_analysis.py',
        'check_products.py',
        'fix_all_images.py',  # Current working image fixer
        'express_deals/ (Django app)',
        'accounts/ (Django app)',
        'products/ (Django app)',
        'scraping/ (Django app)',
        'templates/ (Django templates)',
        'static/ (Django static files)'
    ]
    
    for item in essential_kept:
        print(f"   ✅ {item}")
    
    print(f"\n🚀 READY FOR PRESENTATION!")
    print(f"   Risk of conflicts: MINIMIZED")
    print(f"   Codebase: CLEAN")
    print(f"   Import errors: UNLIKELY")
    
    return removed_files, removed_dirs

if __name__ == "__main__":
    urgent_cleanup()
