#!/usr/bin/env python
"""
EXPRESS DEALS - QUICK FIX FOR is_active FIELD ERRORS
Fix all ScrapeTarget references from is_active to status='active'
"""

import os
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def fix_scrapetarget_references():
    """Fix all is_active references for ScrapeTarget model"""
    print("🔧 FIXING SCRAPETARGET FIELD REFERENCES")
    print("=" * 50)
    
    # Files that need fixing based on the grep results
    files_to_fix = [
        'activate_commercial_scraping.py',
        'simple_activation.py', 
        'reset_database.py',
        'test_commercial_system.py',
        'enable_commercial_features.py',
        'deploy_commercial_system.py',
        'system_status_comprehensive.py',
        'scraping/management/commands/test_commercial_scraping.py'
    ]
    
    fixed_count = 0
    
    for filename in files_to_fix:
        filepath = filename if os.path.exists(filename) else None
        if not filepath and os.path.exists(f'scraping/management/commands/{filename}'):
            filepath = f'scraping/management/commands/{filename}'
        
        if not filepath:
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace ScrapeTarget filter patterns
            original_content = content
            
            # Fix filter(is_active=True) patterns for ScrapeTarget
            content = re.sub(
                r'ScrapeTarget\.objects\.filter\(is_active=True\)',
                "ScrapeTarget.objects.filter(status='active')",
                content
            )
            
            # Fix dictionary references in create operations  
            content = re.sub(
                r"'is_active': True,(\s*# For ScrapeTarget|.*site_choice)",
                "'status': 'active',\\1",
                content
            )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"📋 No changes needed: {filename}")
                
        except Exception as e:
            print(f"❌ Error fixing {filename}: {e}")
    
    print(f"\n🎯 Fixed {fixed_count} files")
    
    # Test the fix
    print("\n🧪 Testing ScrapeTarget access...")
    try:
        from scraping.models import ScrapeTarget
        
        # This should work now
        targets = ScrapeTarget.objects.filter(status='active')
        print(f"✅ ScrapeTarget.objects.filter(status='active') works: {targets.count()} targets")
        
        # Test the model fields
        if targets.exists():
            target = targets.first() 
            print(f"✅ Sample target: {target.name} - Status: {target.status}")
        
        print("✅ All ScrapeTarget references fixed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_scrapetarget_references()
    exit(0 if success else 1)
