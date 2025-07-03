#!/usr/bin/env python3
"""
Express Deals Project Verification Script
Checks that all critical files and components are present and ready for deployment.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status."""
    if os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} - NOT FOUND")
        return False

def main():
    """Main verification function."""
    print("🔍 Express Deals Project Verification")
    print("=" * 50)
    
    # Get project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    all_good = True
    
    # Core Django files
    print("\n📁 Core Django Files:")
    all_good &= check_file_exists("manage.py", "Django management script")
    all_good &= check_file_exists("requirements.txt", "Python dependencies")
    all_good &= check_file_exists(".env", "Environment variables")
    all_good &= check_file_exists(".gitignore", "Git ignore file")
    all_good &= check_file_exists("README.md", "Project documentation")
    all_good &= check_file_exists("DEPLOYMENT.md", "Deployment guide")
    
    # Django apps
    print("\n📁 Django Applications:")
    all_good &= check_directory_exists("express_deals", "Main project directory")
    all_good &= check_directory_exists("products", "Products app")
    all_good &= check_directory_exists("orders", "Orders app")
    all_good &= check_directory_exists("payments", "Payments app")
    all_good &= check_directory_exists("accounts", "Accounts app")
    
    # Templates
    print("\n📁 Templates:")
    all_good &= check_file_exists("templates/base.html", "Base template")
    all_good &= check_file_exists("templates/products/product_list.html", "Product list template")
    all_good &= check_file_exists("templates/products/product_detail.html", "Product detail template")
    all_good &= check_file_exists("templates/orders/cart.html", "Shopping cart template")
    all_good &= check_file_exists("templates/orders/checkout.html", "Checkout template")
    all_good &= check_file_exists("templates/payments/payment.html", "Payment template")
    all_good &= check_file_exists("templates/payments/payment_success.html", "Payment success template")
    all_good &= check_file_exists("templates/payments/payment_cancel.html", "Payment cancel template")
    
    # Key Python files
    print("\n📁 Key Python Files:")
    all_good &= check_file_exists("express_deals/settings.py", "Django settings")
    all_good &= check_file_exists("express_deals/urls.py", "Main URL configuration")
    all_good &= check_file_exists("products/models.py", "Product models")
    all_good &= check_file_exists("products/views.py", "Product views")
    all_good &= check_file_exists("orders/models.py", "Order models")
    all_good &= check_file_exists("orders/views.py", "Order views")
    all_good &= check_file_exists("payments/models.py", "Payment models")
    all_good &= check_file_exists("payments/views.py", "Payment views")
    
    # Static files and media
    print("\n📁 Static Files and Media:")
    all_good &= check_directory_exists("static", "Static files directory")
    all_good &= check_directory_exists("media", "Media files directory")
    
    # Git repository
    print("\n📁 Version Control:")
    all_good &= check_directory_exists(".git", "Git repository")
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ALL CHECKS PASSED! Project is ready for deployment.")
        print("\n📋 Next Steps:")
        print("1. Commit and push all changes to GitHub")
        print("2. Set up production environment variables")
        print("3. Deploy to your chosen platform (Heroku, Railway, DigitalOcean, etc.)")
        print("4. Run migrations and create superuser")
        print("5. Configure Stripe webhooks")
        print("6. Add products through admin panel")
        return True
    else:
        print("⚠️  Some files are missing. Please review the above list.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
