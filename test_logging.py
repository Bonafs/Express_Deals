#!/usr/bin/env python
"""
Test script to verify Django logging configuration is working properly.
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

try:
    # Initialize Django
    django.setup()
    
    import logging
    
    # Get the Django logger
    logger = logging.getLogger('django')
    
    # Test logging
    logger.info("Testing Django logging configuration - this should work without errors!")
    
    print("✅ SUCCESS: Django logging configuration is working correctly!")
    print("✅ No 'ValueError: Unable to configure handler 'file'' error!")
    print(f"✅ Logs directory exists: {project_dir / 'logs'}")
    print(f"✅ Log file path: {project_dir / 'logs' / 'django.log'}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("❌ Django logging configuration has issues.")
    sys.exit(1)
