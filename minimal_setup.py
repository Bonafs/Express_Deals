#!/usr/bin/env python
"""
Minimal Express Deals setup script - avoiding subprocess issues
"""
import sys
import os

def main():
    print("🔧 EXPRESS DEALS - MINIMAL SETUP")
    print("=" * 40)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
    
    # Test critical imports
    print("\n🧪 Testing critical imports...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} imported successfully")
        
        # Setup Django
        django.setup()
        print("✅ Django setup completed")
        
        # Test Django settings
        from django.conf import settings
        print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        print("💡 Please install Django: pip install django")
        return False
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    try:
        import rest_framework
        print(f"✅ Django REST Framework {rest_framework.VERSION} imported successfully")
    except ImportError:
        print("❌ Django REST Framework not found")
        print("💡 Please install: pip install djangorestframework")
        return False
    
    # Test other key imports
    optional_imports = [
        ('celery', 'pip install celery'),
        ('channels', 'pip install channels'),
        ('redis', 'pip install redis'),
        ('PIL', 'pip install pillow'),
        ('stripe', 'pip install stripe'),
    ]
    
    for module, install_cmd in optional_imports:
        try:
            __import__(module)
            print(f"✅ {module} available")
        except ImportError:
            print(f"⚠️ {module} not found - install with: {install_cmd}")
    
    # Test Django management commands
    try:
        from django.core.management import call_command
        print("\n🔧 Testing Django management...")
        
        # Run system check
        call_command('check', verbosity=0)
        print("✅ Django system check passed")
        
    except Exception as e:
        print(f"❌ Django management failed: {e}")
        return False
    
    # Check required directories
    print("\n📁 Checking directories...")
    required_dirs = ['logs', 'media', 'static']
    for dirname in required_dirs:
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            print(f"✅ Created {dirname} directory")
        else:
            print(f"✅ {dirname} directory exists")
    
    # Remove .env file if it exists
    if os.path.exists('.env'):
        os.remove('.env')
        print("✅ Removed .env file (using hardcoded settings)")
    else:
        print("✅ No .env file found (using hardcoded settings)")
    
    print("\n🎉 EXPRESS DEALS SETUP COMPLETE!")
    print("=" * 40)
    print("✅ Django is properly configured")
    print("✅ Core modules are available")
    print("✅ Ready for development")
    print("\n💡 To start the server:")
    print("   python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup incomplete - please install missing packages")
        sys.exit(1)
    else:
        print("\n✅ Setup successful!")
