#!/usr/bin/env python3
"""
Install Essential Web Scraping Technologies
Based on the comprehensive technology stack for world-class scraping
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def upgrade_scraping_stack():
    """Install/upgrade all essential scraping technologies"""
    
    print("🚀 UPGRADING TO WORLD-CLASS SCRAPING STACK")
    print("=" * 50)
    
    # Essential Technologies from the guide
    essential_packages = [
        # Core scraping libraries
        "requests",
        "beautifulsoup4",
        "scrapy",
        "lxml",
        
        # Browser automation
        "selenium",
        "playwright",
        "undetected-chromedriver",
        
        # Data processing
        "pandas",
        "numpy",
        
        # Proxy and session management
        "requests-html",
        "httpx",
        "aiohttp",
        
        # CAPTCHA solving
        "2captcha-python",
        "anticaptchaofficial",
        
        # Data storage and caching
        "redis",
        "pymongo",
        "psycopg2-binary",
        
        # Additional utilities
        "fake-useragent",
        "cloudscraper",
        "tqdm",
        "schedule",
        
        # Image processing
        "Pillow",
        "opencv-python",
        
        # Text processing
        "nltk",
        "textblob",
        
        # Async support
        "asyncio",
        "aiofiles",
    ]
    
    successful_installs = 0
    
    for package in essential_packages:
        if install_package(package):
            successful_installs += 1
    
    print(f"\n📊 INSTALLATION SUMMARY:")
    print(f"   Successfully installed: {successful_installs}/{len(essential_packages)}")
    print(f"   Success rate: {(successful_installs/len(essential_packages)*100):.1f}%")
    
    # Post-installation setup
    print(f"\n🔧 POST-INSTALLATION SETUP:")
    
    # Install Playwright browsers
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed")
    except:
        print("⚠️ Playwright browser installation failed (run manually: playwright install)")
    
    # Download NLTK data
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
    except:
        print("⚠️ NLTK data download failed")
    
    print(f"\n🌟 WORLD-CLASS SCRAPING STACK READY!")
    
    return successful_installs

if __name__ == "__main__":
    upgrade_scraping_stack()
