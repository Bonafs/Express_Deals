#!/usr/bin/env python3
"""
Express Deals: Project Cleanup Analysis
Identify essential vs legacy files for clean production build
"""

import os
import glob
from pathlib import Path

def analyze_workspace():
    """Analyze workspace for essential vs legacy files"""
    
    print("🔍 EXPRESS DEALS WORKSPACE ANALYSIS")
    print("=" * 50)
    
    # Essential Django files (KEEP)
    essential_files = {
        'Core Django': [
            'manage.py',
            'requirements.txt',
            'runtime.txt',
            'Procfile',
            'README.md',
            'LICENSE',
            'db.sqlite3'
        ],
        
        'Django Apps': [
            'express_deals/**/*.py',
            'accounts/**/*.py',
            'products/**/*.py', 
            'orders/**/*.py',
            'payments/**/*.py',
            'scraping/**/*.py',
            'realtime/**/*.py',
            'templates/**/*',
            'static/**/*',
            'staticfiles/**/*',
            'media/**/*'
        ],
        
        'Production Config': [
            'express_deals/settings.py',
            'express_deals/production_settings.py',
            'express_deals/heroku_settings.py',
            'express_deals/urls.py',
            'express_deals/wsgi.py',
            'express_deals/asgi.py'
        ],
        
        'Current Working Scripts': [
            'create_emergency_products_fixed.py',
            'setup_scrappable_retailers_fixed.py',
            'world_class_scraping.py',
            'strategy_implementation_analysis.py',
            'check_products.py'
        ]
    }
    
    # Legacy/Test files (CONSIDER REMOVING)
    legacy_files = {
        'Development Scripts': [
            'fix_*.py',
            'emergency_*.py',
            'test_*.py',
            'demo_*.py',
            'temp_*.py',
            'debug_*.py',
            'check_*.py',  # Except check_products.py
            'admin_demo.py',
            'customer_demo.py',
            'auth_test.py',
            'auth_status.py',
            'system_status.py',
            'url_tracking_*.py',
            'comprehensive_*.py'
        ],
        
        'Duplicate/Old Scripts': [
            'create_emergency_products.py',  # We have _fixed version
            'setup_scrappable_retailers.py',  # We have _fixed version
            'add_demo_products.py',
            'create_products_with_images.py',
            'analyze_scraping_performance.py',
            'get_live_products_now.py',
            'upgrade_scraping_stack.py'
        ],
        
        'Backup/Temp Directories': [
            'temp-heroku/**/*',
            '__pycache__/**/*',
            '*.pyc',
            '.pytest_cache/**/*'
        ],
        
        'Documentation (Maybe Archive)': [
            '*.md',  # Except README.md
            'ADMIN_*.md',
            'AUTHENTICATION_*.md',
            'CUSTOMER_*.md',
            'DEPLOYMENT_*.md',
            'URL_TRACKING_*.md'
        ]
    }
    
    return essential_files, legacy_files

def scan_current_files():
    """Scan current directory for actual files"""
    
    current_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '.venv', 'node_modules', '__pycache__']):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            current_files.append(file_path.replace('.\\', ''))
    
    return current_files

def categorize_files():
    """Categorize all files as KEEP, REMOVE, or REVIEW"""
    
    essential_files, legacy_files = analyze_workspace()
    current_files = scan_current_files()
    
    categorized = {
        'KEEP': [],
        'REMOVE': [],
        'REVIEW': []
    }
    
    # Essential patterns (KEEP)
    essential_patterns = [
        'manage.py', 'requirements.txt', 'runtime.txt', 'Procfile', 'README.md', 'LICENSE',
        'express_deals/', 'accounts/', 'products/', 'orders/', 'payments/', 'scraping/', 'realtime/',
        'templates/', 'static/', 'staticfiles/', 'media/', 'logs/',
        'create_emergency_products_fixed.py',
        'setup_scrappable_retailers_fixed.py', 
        'world_class_scraping.py',
        'strategy_implementation_analysis.py',
        'check_products.py',
        'db.sqlite3'
    ]
    
    # Legacy patterns (REMOVE)
    legacy_patterns = [
        'fix_', 'emergency_', 'test_', 'demo_', 'temp_', 'debug_',
        'admin_demo.py', 'customer_demo.py', 'auth_test.py', 'auth_status.py',
        'url_tracking_', 'comprehensive_', 'analyze_', 'upgrade_',
        'create_emergency_products.py', 'setup_scrappable_retailers.py',
        'get_live_products_now.py', 'add_demo_products.py',
        'temp-heroku/', '__pycache__/', '.pyc'
    ]
    
    for file_path in current_files:
        file_name = os.path.basename(file_path)
        
        # Check if it's essential
        is_essential = any(pattern in file_path for pattern in essential_patterns)
        
        # Check if it's legacy
        is_legacy = any(pattern in file_name for pattern in legacy_patterns)
        
        if is_essential and not is_legacy:
            categorized['KEEP'].append(file_path)
        elif is_legacy and not is_essential:
            categorized['REMOVE'].append(file_path)
        else:
            categorized['REVIEW'].append(file_path)
    
    return categorized

def create_cleanup_recommendations():
    """Create cleanup recommendations"""
    
    categorized = categorize_files()
    
    print("📋 FILE CATEGORIZATION RESULTS")
    print("=" * 40)
    
    print(f"\n✅ ESSENTIAL FILES (KEEP): {len(categorized['KEEP'])}")
    for file_path in sorted(categorized['KEEP'])[:10]:  # Show first 10
        print(f"   ✅ {file_path}")
    if len(categorized['KEEP']) > 10:
        print(f"   ... and {len(categorized['KEEP']) - 10} more essential files")
    
    print(f"\n❌ LEGACY FILES (SAFE TO REMOVE): {len(categorized['REMOVE'])}")
    for file_path in sorted(categorized['REMOVE'])[:15]:  # Show first 15
        print(f"   ❌ {file_path}")
    if len(categorized['REMOVE']) > 15:
        print(f"   ... and {len(categorized['REMOVE']) - 15} more legacy files")
    
    print(f"\n⚠️ REVIEW REQUIRED: {len(categorized['REVIEW'])}")
    for file_path in sorted(categorized['REVIEW'])[:10]:  # Show first 10
        print(f"   ⚠️ {file_path}")
    
    # Risk assessment
    print(f"\n🎯 CLEANUP RECOMMENDATIONS:")
    
    if len(categorized['REMOVE']) > 50:
        print(f"   🚨 HIGH CLEANUP NEEDED: {len(categorized['REMOVE'])} legacy files")
        print(f"   📋 RECOMMENDATION: Clean up before presentation")
        print(f"   ⚠️ RISK: Legacy files may cause import conflicts")
    elif len(categorized['REMOVE']) > 20:
        print(f"   ⚠️ MODERATE CLEANUP NEEDED: {len(categorized['REMOVE'])} legacy files")  
        print(f"   📋 RECOMMENDATION: Clean up high-risk files only")
    else:
        print(f"   ✅ LOW CLEANUP NEEDED: {len(categorized['REMOVE'])} legacy files")
        print(f"   📋 RECOMMENDATION: Clean up after presentation")
    
    # Specific risks
    high_risk_files = [f for f in categorized['REMOVE'] if any(risk in f for risk in [
        'settings', 'urls', 'models', 'views', 'forms', 'admin'
    ])]
    
    if high_risk_files:
        print(f"\n🚨 HIGH RISK FILES (Clean immediately):")
        for file_path in high_risk_files:
            print(f"   🚨 {file_path}")
    
    return categorized

def generate_cleanup_script():
    """Generate a cleanup script"""
    
    categorized = categorize_files()
    
    cleanup_script = '''#!/usr/bin/env python3
"""
Express Deals: Automated Cleanup Script
Remove legacy files safely for production build
"""

import os
import shutil
from pathlib import Path

def backup_before_cleanup():
    """Create backup of files before deletion"""
    backup_dir = "cleanup_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def safe_cleanup():
    """Safely remove legacy files"""
    
    print("🧹 STARTING SAFE CLEANUP")
    print("=" * 30)
    
    # Create backup first
    backup_dir = backup_before_cleanup()
    
    # Files to remove
    files_to_remove = [
'''
    
    for file_path in categorized['REMOVE'][:20]:  # Limit for safety
        cleanup_script += f'        "{file_path}",\n'
    
    cleanup_script += '''    ]
    
    removed_count = 0
    
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                # Backup first
                backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, backup_path)
                
                # Remove original
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
                removed_count += 1
            else:
                print(f"⚠️ Not found: {file_path}")
                
        except Exception as e:
            print(f"❌ Error removing {file_path}: {e}")
    
    print(f"\\n🎯 CLEANUP COMPLETE!")
    print(f"   Removed: {removed_count} files")
    print(f"   Backup created in: {backup_dir}")
    
    return removed_count

if __name__ == "__main__":
    safe_cleanup()
'''
    
    with open('automated_cleanup.py', 'w') as f:
        f.write(cleanup_script)
    
    print(f"\n💾 CLEANUP SCRIPT GENERATED: automated_cleanup.py")

def main():
    """Main analysis function"""
    
    categorized = create_cleanup_recommendations()
    
    print(f"\n🤔 SHOULD YOU CLEAN UP NOW?")
    print("=" * 35)
    
    risk_score = len(categorized['REMOVE'])
    
    if risk_score > 50:
        print("🚨 YES - Clean up NOW before presentation")
        print("   Reasons:")
        print("   • Too many legacy files increase error risk")
        print("   • Import conflicts likely")
        print("   • Cleaner codebase = better presentation")
        
    elif risk_score > 20:
        print("⚠️ PARTIAL - Clean up high-risk files only")
        print("   Reasons:")
        print("   • Moderate risk of conflicts")
        print("   • Focus on files that could break imports")
        print("   • Leave non-critical files for later")
        
    else:
        print("✅ NO - Clean up AFTER presentation")
        print("   Reasons:")
        print("   • Low risk of conflicts")
        print("   • Don't risk breaking working system")
        print("   • Focus on presentation prep instead")
    
    print(f"\n📋 IMMEDIATE ACTION PLAN:")
    print(f"   1. Review high-risk files listed above")
    print(f"   2. Remove only files that could cause import errors")
    print(f"   3. Test the platform after any removals")
    print(f"   4. Keep backups of everything removed")
    
    generate_cleanup_script()
    
    return categorized

if __name__ == "__main__":
    main()
