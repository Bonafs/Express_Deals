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
        'Uploads local product images to Cloudinary and updates the database '
        'references accordingly.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting local image upload to Cloudinary..."
        ))

        # Get the products directory path (same directory as this management command)
        # Go up from management/commands/ to the products app directory
        products_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        if not os.path.exists(products_dir):
            self.stdout.write(self.style.ERROR(
                f"Products directory not found: {products_dir}"
            ))
            return

        # Get all image files in the products directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        
        for file in os.listdir(products_dir):
            file_path = os.path.join(products_dir, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(file)
        
        self.stdout.write(f"Found {len(image_files)} image files in products directory.")
        
        if not image_files:
            self.stdout.write(self.style.WARNING("No image files found to upload."))
            return

        # Get all products that need images
        products_needing_images = Product.objects.filter(
            Q(image__isnull=True) | Q(image__exact='')
        )
        
        self.stdout.write(f"Found {products_needing_images.count()} products needing images.")

        uploaded_count = 0
        matched_count = 0
        
        for product in products_needing_images:
            self.stdout.write(f"\nProcessing product: {product.name}")
            
            # Try to find a matching image file
            # Create possible filename variations based on product name
            product_slug = product.slug if hasattr(product, 'slug') else product.name.lower().replace(' ', '_').replace('&', 'and')
            
            possible_filenames = [
                f"{product_slug}.jpg",
                f"{product_slug}.jpeg",
                f"{product_slug}.png",
                f"{product.name.lower().replace(' ', '_').replace('&', '_')}.jpg",
                f"{product.name.lower().replace(' ', '_').replace('&', 'and')}.jpg",
            ]
            
            matched_file = None
            for filename in possible_filenames:
                if filename in image_files:
                    matched_file = filename
                    break
            
            # Also check for partial matches
            if not matched_file:
                for image_file in image_files:
                    # Remove extension and check if it contains key words from product name
                    file_base = os.path.splitext(image_file)[0].lower()
                    product_words = product.name.lower().split()
                    if len(product_words) >= 2:  # Only match if product has at least 2 words
                        matches = sum(1 for word in product_words if word in file_base)
                        if matches >= 2:  # At least 2 words match
                            matched_file = image_file
                            break
            
            if matched_file:
                matched_count += 1
                file_path = os.path.join(products_dir, matched_file)
                
                try:
                    # Create a public_id based on the product
                    public_id = f"product_{product.id}_{product.name.lower().replace(' ', '_').replace('&', 'and')}"
                    
                    self.stdout.write(f"  - Uploading {matched_file} to Cloudinary...")
                    
                    # Upload to Cloudinary
                    upload_result = upload(
                        file_path,
                        folder="products",
                        public_id=public_id,
                        overwrite=True
                    )
                    
                    # Update the product's image field
                    product.image = upload_result['public_id']
                    product.save()
                    
                    uploaded_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  ✓ Successfully uploaded and linked: {upload_result['public_id']}"
                    ))
                    
                except CloudinaryError as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Cloudinary error uploading {matched_file}: {e}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Unexpected error uploading {matched_file}: {e}"
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"  - No matching image file found for: {product.name}"
                ))

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Local Image Upload Complete!"))
        self.stdout.write(f"Products Processed: {products_needing_images.count()}")
        self.stdout.write(f"Images Matched: {matched_count}")
        self.stdout.write(self.style.SUCCESS(f"Images Successfully Uploaded: {uploaded_count}"))
        self.stdout.write("=" * 50)
        
        if uploaded_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f"\n{uploaded_count} images were successfully uploaded to Cloudinary!"
            ))
            self.stdout.write(self.style.NOTICE(
                "Run 'python manage.py verify_cloudinary_images' to verify the uploads."
            ))
