#!/usr/bin/env python
"""
Start Django server for demonstration
"""
import subprocess
import sys
import time

print("🚀 Starting Express Deals Platform...")
print("📝 Server will start at: http://localhost:8000")
print("⚙️ Admin panel at: http://localhost:8000/admin/")
print("\n🔑 Admin credentials:")
print("   Username: admin")
print("   Password: admin123")
print("\n📦 Features ready:")
print("   ✅ GBP pricing on all products")
print("   ✅ User registration with success messages")
print("   ✅ User login system")
print("   ✅ Shopping cart functionality")
print("   ✅ Admin panel")
print("\n⏰ Starting server...")

try:
    # Start the Django development server
    subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'], check=True)
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("💡 Try running: python manage.py runserver 8000")
