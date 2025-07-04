#!/usr/bin/env python
"""
Express Deals Project Status Checker
Verifies project completion without requiring terminal output.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

def check_file_structure():
    """Check if all required files and directories exist."""
    required_paths = [
        'express_deals/',
        'products/',
        'orders/',
        'payments/',
        'accounts/',
        'templates/',
        'static/',
        'media/',
        'logs/',
        'manage.py',
        'requirements.txt',
        '.gitignore',
        'README.md',
    ]
    
    print("📁 File Structure Check")
    print("-" * 30)
    
    missing = []
    for path in required_paths:
        full_path = Path(path)
        if full_path.exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path}")
            missing.append(path)
    
    return len(missing) == 0, missing

def check_django_apps():
    """Check if Django apps are properly configured."""
    try:
        django.setup()
        from django.apps import apps
        
        required_apps = ['products', 'orders', 'payments', 'accounts']
        
        print("\n🏗️ Django Apps Check")
        print("-" * 30)
        
        missing = []
        for app_name in required_apps:
            try:
                app = apps.get_app_config(app_name)
                print(f"✅ {app_name} - {app.verbose_name}")
            except:
                print(f"❌ {app_name}")
                missing.append(app_name)
        
        return len(missing) == 0, missing
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False, []

def check_models():
    """Check if models are properly defined."""
    try:
        from products.models import Category, Product, ProductImage, ProductReview
        from orders.models import Cart, CartItem, Order, OrderItem
        from payments.models import Payment
        
        models_info = [
            ('Category', Category),
            ('Product', Product),
            ('ProductImage', ProductImage),
            ('ProductReview', ProductReview),
            ('Cart', Cart),
            ('CartItem', CartItem),
            ('Order', Order),
            ('OrderItem', OrderItem),
            ('Payment', Payment),
        ]
        
        print("\n📊 Models Check")
        print("-" * 30)
        
        for name, model in models_info:
            try:
                field_count = len(model._meta.fields)
                print(f"✅ {name} ({field_count} fields)")
            except Exception as e:
                print(f"❌ {name} - Error: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Models import error: {e}")
        return False

def check_templates():
    """Check if templates exist."""
    template_files = [
        'base.html',
        'products/product_list.html',
        'products/product_detail.html',
        'orders/cart.html',
        'orders/checkout.html',
        'payments/payment.html',
    ]
    
    print("\n🎨 Templates Check")
    print("-" * 30)
    
    missing = []
    for template in template_files:
        template_path = Path('templates') / template
        if template_path.exists():
            size = template_path.stat().st_size
            print(f"✅ {template} ({size} bytes)")
        else:
            print(f"❌ {template}")
            missing.append(template)
    
    return len(missing) == 0, missing

def check_database():
    """Check database status."""
    try:
        from django.db import connection
        
        print("\n🗄️ Database Check")
        print("-" * 30)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"✅ Database connected ({len(tables)} tables)")
                for table in tables[:5]:  # Show first 5 tables
                    print(f"  📋 {table[0]}")
                if len(tables) > 5:
                    print(f"  ... and {len(tables) - 5} more tables")
                return True
            else:
                print("⚠️ Database connected but no tables found")
                return False
                
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_git_status():
    """Check git repository status."""
    print("\n📝 Git Repository Check")
    print("-" * 30)
    
    git_dir = Path('.git')
    if git_dir.exists():
        print("✅ Git repository initialized")
        
        # Check for recent commits
        log_file = git_dir / 'logs' / 'HEAD'
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                print(f"✅ {len(lines)} commits found")
                if lines:
                    last_commit = lines[-1].strip()
                    commit_msg = last_commit.split('\t')[-1] if '\t' in last_commit else 'Unknown'
                    print(f"  📝 Latest: {commit_msg}")
        
        # Check remote
        config_file = git_dir / 'config'
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = f.read()
                if 'github.com' in config:
                    print("✅ GitHub remote configured")
                else:
                    print("⚠️ No GitHub remote found")
        
        return True
    else:
        print("❌ Not a git repository")
        return False

def main():
    """Run all project checks."""
    print("🔍 Express Deals Project Status Report")
    print("=" * 50)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Django Apps", check_django_apps),
        ("Models", check_models),
        ("Templates", check_templates),
        ("Database", check_database),
        ("Git Repository", check_git_status),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if isinstance(result, tuple):
                results[check_name] = result[0]
            else:
                results[check_name] = result
        except Exception as e:
            print(f"\n❌ {check_name} check failed: {e}")
            results[check_name] = False
    
    # Summary
    print("\n🎯 Project Status Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for check_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{check_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n📊 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Project is ready for development!")
        print("💡 Run 'python start_server.py' to start the development server")
    else:
        print("⚠️ Some issues found. Review the details above.")
    
    return passed == total

if __name__ == "__main__":
    main()
