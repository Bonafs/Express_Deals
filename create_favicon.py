#!/usr/bin/env python
"""
Create a favicon.ico for Express Deals using a flash/lightning bolt icon
"""
from PIL import Image, ImageDraw
import os

def create_favicon():
    """Create favicon with lightning bolt icon"""
    # Create a 32x32 image with Express Deals brand colors
    img = Image.new('RGBA', (32, 32), (0, 123, 255, 255))  # Express Deals blue
    draw = ImageDraw.Draw(img)
    
    # Draw lightning bolt (flash icon) in white
    lightning_points = [
        (18, 2),   # Top point
        (12, 14),  # Left middle
        (16, 14),  # Center
        (14, 30),  # Bottom point
        (20, 18),  # Right middle
        (16, 18)   # Back to center
    ]
    
    draw.polygon(lightning_points, fill=(255, 255, 255, 255))
    
    # Create multiple sizes for ICO format
    sizes = [(16, 16), (32, 32), (48, 48)]
    images = []
    
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save as ICO file
    favicon_path = 'static/favicon.ico'
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Save the main 32x32 as ICO
    img.save(favicon_path, format='ICO', sizes=[(32, 32)])
    
    print(f"Favicon created: {favicon_path}")
    
    # Also create PNG versions
    img.save('static/favicon-32x32.png', format='PNG')
    resized_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    resized_16.save('static/favicon-16x16.png', format='PNG')
    
    print("Additional PNG favicons created:")
    print("- static/favicon-16x16.png")
    print("- static/favicon-32x32.png")

if __name__ == "__main__":
    create_favicon()
