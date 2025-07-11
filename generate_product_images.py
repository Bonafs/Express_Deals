#!/usr/bin/env python
"""
Product Image Generator for Express Deals
Creates attractive placeholder images for products without real images
"""

import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
import random
import colorsys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from django.core.files.base import ContentFile
import io


def generate_gradient_background(width, height, color_theme):
    """Generate a gradient background based on color theme"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Color themes for different categories
    color_schemes = {
        'electronics': [(65, 105, 225), (0, 191, 255)],  # Blue gradient
        'clothing': [(255, 182, 193), (255, 105, 180)],   # Pink gradient
        'home': [(144, 238, 144), (34, 139, 34)],         # Green gradient
        'beauty': [(221, 160, 221), (186, 85, 211)],      # Purple gradient
        'sports': [(255, 140, 0), (255, 69, 0)],          # Orange gradient
        'books': [(205, 133, 63), (139, 69, 19)],         # Brown gradient
        'toys': [(255, 255, 0), (255, 215, 0)],           # Yellow gradient
        'food': [(255, 99, 71), (220, 20, 60)],           # Red gradient
        'automotive': [(128, 128, 128), (64, 64, 64)],    # Gray gradient
        'default': [(173, 216, 230), (135, 206, 235)]     # Light blue gradient
    }
    
    colors = color_schemes.get(color_theme, color_schemes['default'])
    start_color = colors[0]
    end_color = colors[1]
    
    # Create gradient
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def add_product_icon(img, category_name):
    """Add a category-appropriate icon to the image"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Icon symbols for different categories
    icons = {
        'electronics': '🔌',
        'clothing': '👕',
        'home': '🏠',
        'beauty': '💄',
        'sports': '⚽',
        'books': '📚',
        'toys': '🧸',
        'food': '🍎',
        'automotive': '🚗',
        'default': '📦'
    }
    
    # Get category key
    category_key = 'default'
    for key in icons.keys():
        if key in category_name.lower():
            category_key = key
            break
    
    # Try to use a font that supports emojis (fallback to text)
    try:
        # For Windows, try Segoe UI Emoji
        font_size = min(width, height) // 4
        font = ImageFont.truetype("seguiemj.ttf", font_size)
        icon = icons[category_key]
    except:
        # Fallback to simple text
        font_size = min(width, height) // 6
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Text alternatives for icons
        text_icons = {
            'electronics': 'TECH',
            'clothing': 'STYLE',
            'home': 'HOME',
            'beauty': 'BEAUTY',
            'sports': 'SPORT',
            'books': 'BOOKS',
            'toys': 'TOYS',
            'food': 'FOOD',
            'automotive': 'AUTO',
            'default': 'PRODUCT'
        }
        icon = text_icons[category_key]
    
    # Get text/icon dimensions and center it
    bbox = draw.textbbox((0, 0), icon, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Add shadow
    draw.text((x + 2, y + 2), icon, fill=(0, 0, 0, 100), font=font)
    # Add main text
    draw.text((x, y), icon, fill=(255, 255, 255, 230), font=font)
    
    return img


def create_product_placeholder(product_name, category_name, width=400, height=400):
    """Create an attractive placeholder image for a product"""
    
    # Determine color theme from category
    color_theme = 'default'
    category_lower = category_name.lower() if category_name else ''
    
    themes = ['electronics', 'clothing', 'home', 'beauty', 'sports', 'books', 'toys', 'food', 'automotive']
    for theme in themes:
        if theme in category_lower:
            color_theme = theme
            break
    
    # Generate base gradient
    img = generate_gradient_background(width, height, color_theme)
    
    # Add category icon
    img = add_product_icon(img, category_name or 'default')
    
    # Add subtle pattern overlay
    draw = ImageDraw.Draw(img)
    
    # Add some geometric patterns for visual interest
    overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Add subtle circles
    for i in range(3):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(20, 60)
        overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=(255, 255, 255, 15))
    
    # Composite the overlay
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    return img


def update_products_with_placeholders():
    """Update products that don't have images with generated placeholders"""
    print("=== Creating Placeholder Images for Products ===")
    
    # Get products that need images
    products_needing_images = Product.objects.filter(
        image__in=['', 'products/default.jpg']
    ) | Product.objects.filter(image__isnull=True)
    
    print(f"Found {products_needing_images.count()} products needing placeholder images")
    
    updated_count = 0
    
    for product in products_needing_images:
        print(f"Creating placeholder for: {product.name}")
        
        try:
            # Create placeholder image
            category_name = product.category.name if product.category else 'Product'
            img = create_product_placeholder(product.name, category_name)
            
            # Save to BytesIO
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)
            
            # Create filename
            clean_name = "".join(c for c in product.name if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_name = clean_name.replace(' ', '_')[:30]
            filename = f"placeholder_{product.id}_{clean_name}.jpg"
            
            # Save to product
            content = ContentFile(img_io.getvalue(), name=filename)
            product.image.save(filename, content, save=True)
            
            updated_count += 1
            print(f"  ✓ Created placeholder image: {filename}")
            
        except Exception as e:
            print(f"  ✗ Error creating placeholder for {product.name}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Created {updated_count} placeholder images")


def main():
    """Main function"""
    print("Express Deals - Product Image Generator\n")
    update_products_with_placeholders()
    print("\n=== Image Generation Complete ===")


if __name__ == "__main__":
    main()
