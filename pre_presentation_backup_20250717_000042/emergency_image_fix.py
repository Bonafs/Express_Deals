#!/usr/bin/env python
"""
CRITICAL FIX: Upload default.jpg to Cloudinary with exact path that's being requested
"""

import os
import sys
import django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

import cloudinary.uploader
from PIL import Image, ImageDraw, ImageFont
import io

def create_default_image():
    """Create a professional default image."""
    # Create image
    img = Image.new('RGB', (400, 400), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        try:
            font_large = ImageFont.truetype("Arial", 24)
            font_small = ImageFont.truetype("Arial", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Add text
    text1 = "EXPRESS DEALS"
    text2 = "Image Coming Soon"
    
    # Calculate text positions
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    
    pos1 = ((400 - w1) // 2, 170)
    pos2 = ((400 - w2) // 2, 210)
    
    # Draw text and border
    draw.text(pos1, text1, fill='#0066cc', font=font_large)
    draw.text(pos2, text2, fill='#666666', font=font_small)
    draw.rectangle([20, 20, 380, 380], outline='#ddd', width=2)
    
    return img

def upload_default_variants():
    """Upload all possible default image variants."""
    print("🚨 CRITICAL: Uploading default image variants...")
    
    img = create_default_image()
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=90)
    img_bytes.seek(0)
    
    # Upload multiple variants to cover all possible URLs
    variants = [
        "products/default",
        "products/default.jpg", 
        "default",
        "default.jpg"
    ]
    
    for variant in variants:
        try:
            result = cloudinary.uploader.upload(
                img_bytes.getvalue(),
                public_id=variant,
                overwrite=True,
                resource_type="image"
            )
            print(f"✅ Uploaded: {variant} -> {result['secure_url']}")
            img_bytes.seek(0)  # Reset for next upload
        except Exception as e:
            print(f"❌ Failed to upload {variant}: {e}")
    
    return True

if __name__ == "__main__":
    print("🚨 EMERGENCY DEFAULT IMAGE FIX")
    print("=" * 50)
    upload_default_variants()
    print("=" * 50)
    print("✅ Default images uploaded! Deploy immediately!")
