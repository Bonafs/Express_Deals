#!/usr/bin/env python
"""
Fix default image file
"""

import requests
import os

def fix_default_image():
    """Create a proper default.jpg file"""
    try:
        # Download a generic product placeholder image
        url = 'https://via.placeholder.com/400x400/f8f9fa/6c757d?text=No+Image'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Ensure media/products directory exists
            os.makedirs('media/products', exist_ok=True)
            
            # Save to media/products/default.jpg
            with open('media/products/default.jpg', 'wb') as f:
                f.write(response.content)
            
            print('✅ Created new default.jpg file')
            print(f'   File size: {len(response.content)} bytes')
            return True
        else:
            print(f'❌ Failed to download placeholder image: {response.status_code}')
            return False
            
    except Exception as e:
        print(f'❌ Error creating default image: {e}')
        return False

if __name__ == "__main__":
    fix_default_image()
