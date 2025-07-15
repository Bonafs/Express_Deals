"""
Cloudinary Configuration for Express Deals
===========================================

This module provides additional Cloudinary configuration options
beyond the basic setup in settings.py.
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Initialize Cloudinary with configuration from environment variables
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# Cloudinary Upload Options
CLOUDINARY_UPLOAD_OPTIONS = {
    'quality': 'auto:good',
    'fetch_format': 'auto',
    'crop': 'fill',
    'gravity': 'auto',
    'width': 800,
    'height': 600,
    'secure': True,
}

# Cloudinary Transformation Presets for Product Images
PRODUCT_IMAGE_TRANSFORMATIONS = {
    'thumbnail': {
        'width': 150,
        'height': 150,
        'crop': 'fill',
        'gravity': 'auto',
        'quality': 'auto:good',
        'fetch_format': 'auto'
    },
    'medium': {
        'width': 400,
        'height': 300,
        'crop': 'fill',
        'gravity': 'auto',
        'quality': 'auto:good',
        'fetch_format': 'auto'
    },
    'large': {
        'width': 800,
        'height': 600,
        'crop': 'fill',
        'gravity': 'auto',
        'quality': 'auto:good',
        'fetch_format': 'auto'
    }
}

# Helper functions for image URL generation


def get_product_image_url(image_public_id, transformation='medium'):
    """
    Generate a Cloudinary URL for a product image with transformation.
    
    Args:
        image_public_id (str): The public ID of the image in Cloudinary
        transformation (str): The transformation preset to apply
        
    Returns:
        str: The complete Cloudinary URL for the image
    """
    if not image_public_id:
        return None
        
    transform_options = PRODUCT_IMAGE_TRANSFORMATIONS.get(
        transformation, PRODUCT_IMAGE_TRANSFORMATIONS['medium']
    )
    
    return cloudinary.CloudinaryImage(image_public_id).build_url(
        **transform_options
    )


def upload_product_image(image_file, folder='products'):
    """
    Upload a product image to Cloudinary with optimized settings.
    
    Args:
        image_file: The image file to upload
        folder (str): The Cloudinary folder to organize images
        
    Returns:
        dict: Upload result containing public_id and secure_url
    """
    upload_options = CLOUDINARY_UPLOAD_OPTIONS.copy()
    upload_options['folder'] = folder
    
    try:
        result = cloudinary.uploader.upload(image_file, **upload_options)
        return {
            'success': True,
            'public_id': result.get('public_id'),
            'secure_url': result.get('secure_url'),
            'width': result.get('width'),
            'height': result.get('height')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def delete_product_image(public_id):
    """
    Delete a product image from Cloudinary.
    
    Args:
        public_id (str): The public ID of the image to delete
        
    Returns:
        dict: Deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return {
            'success': result.get('result') == 'ok',
            'result': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
