import os
from django.core.management.base import BaseCommand
from django.db.models import Q
from products.models import Product
import cloudinary
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = (
        'Maps existing product image references to local files and uploads '
        'them to Cloudinary with the correct public_id.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting product image mapping and upload..."
        ))

        # Get the products directory path
        products_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Get all image files in the products directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = {}
        
        for file in os.listdir(products_dir):
            file_path = os.path.join(products_dir, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
                # Store without extension for easier matching
                base_name = os.path.splitext(file)[0]
                image_files[base_name] = file
        
        self.stdout.write(f"Found {len(image_files)} image files in products directory.")
        
        # Get all products with image references
        products_with_images = Product.objects.exclude(image__isnull=True).exclude(image__exact='')
        
        self.stdout.write(f"Found {products_with_images.count()} products with image references.")

        uploaded_count = 0
        
        # Define mapping between image filenames and products
        filename_mappings = {
            'resistance_band_set_by_gymshark': 'fitness_resistance_bands_set',
            'chillys_series_2_water_bottle': 'chillys_series_2_water_bottle',
            'emma_bridgewater_polka_dot_tea_set': 'emma_bridgewater_polka_dot_tea_set',
            'organic_cotton_t-shirt': 'organic_cotton_t-shirt',
            'marks__spencer_wool_overcoat': 'marks__spencer_wool_overcoat',
            'adidas_originals_stan_smith': 'adidas_originals_stan_smith',
            'led_desk_lamp': 'led_desk_lamp',
            'sony_wh-1000xm5_headphones': 'sony_wh-1000xm5_headphones',
            'fitness_resistance_bands_set': 'fitness_resistance_bands_set',
            'stainless_steel_water_bottle': 'stainless_steel_water_bottle',
            'wireless_bluetooth_headphones': 'wireless_bluetooth_headphones',
            'british_designer_wool_coat': 'british_designer_wool_coat',
            'nike_air_max_uk_edition': 'nike_air_max_uk_edition',
        }
        
        for product in products_with_images:
            self.stdout.write(f"\nProcessing product: {product.name}")
            
            # Safely handle the image reference
            if not product.image:
                self.stdout.write(self.style.WARNING(
                    "  - Product has no image reference, skipping."
                ))
                continue
                
            try:
                image_ref = str(product.image)
                self.stdout.write(f"  Current image reference: {image_ref}")
            except (TypeError, AttributeError):
                self.stdout.write(self.style.WARNING(
                    "  - Product has invalid image reference, skipping."
                ))
                continue
            
            # Extract the expected filename from the product image reference
            public_id_parts = image_ref.split('/')
            expected_filename = public_id_parts[-1] if public_id_parts else image_ref
            
            # Try direct match first
            local_file = None
            if expected_filename in image_files:
                local_file = image_files[expected_filename]
            elif expected_filename in filename_mappings and filename_mappings[expected_filename] in image_files:
                local_file = image_files[filename_mappings[expected_filename]]
            
            if local_file:
                file_path = os.path.join(products_dir, local_file)
                
                try:
                    self.stdout.write(f"  - Uploading {local_file} to Cloudinary...")
                    
                    # Upload to Cloudinary with the exact public_id from the product
                    upload_result = upload(
                        file_path,
                        public_id=image_ref,
                        overwrite=True
                    )
                    
                    uploaded_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✓ Successfully uploaded: {upload_result['public_id']}"
                    ))
                    
                except CloudinaryError as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Cloudinary error uploading {local_file}: {e}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Unexpected error uploading {local_file}: {e}"
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"  - No matching local file found for: {expected_filename}"
                ))
                # List available files for debugging
                similar_files = [f for f in image_files.keys() if any(word in f.lower() for word in expected_filename.lower().split('_'))]
                if similar_files:
                    self.stdout.write(f"    Similar files available: {', '.join(similar_files[:3])}")

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Product Image Upload Complete!"))
        self.stdout.write(f"Products Processed: {products_with_images.count()}")
        self.stdout.write(self.style.SUCCESS(f"Images Successfully Uploaded: {uploaded_count}"))
        self.stdout.write("=" * 50)
        
        if uploaded_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f"\n{uploaded_count} images were successfully uploaded to Cloudinary!"
            ))
            self.stdout.write(self.style.NOTICE(
                "Run 'python manage.py verify_cloudinary_images' to verify the uploads."
            ))
