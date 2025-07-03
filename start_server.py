#!/usr/bin/env python
"""
Development server launcher for Express Deals.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.conf import settings
    
    def start_server():
        """Start the Django development server."""
        print("🚀 Starting Express Deals Development Server")
        print("=" * 50)
        print(f"🔧 Debug Mode: {settings.DEBUG}")
        print(f"🏠 Allowed Hosts: {settings.ALLOWED_HOSTS}")
        print(f"🗄️ Database: {settings.DATABASES['default']['ENGINE']}")
        print("=" * 50)
        print("📱 Server will be available at: http://127.0.0.1:8000/")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the development server
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])

    if __name__ == "__main__":
        start_server()

except Exception as e:
    print(f"❌ Server startup error: {e}")
    import traceback
    traceback.print_exc()
