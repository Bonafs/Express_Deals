import cloudinary
import cloudinary.api
from django.core.management.base import BaseCommand
from products.models import Product
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verify that product images exist in Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write("Verifying product images in Cloudinary...")

        # Configure Cloudinary
        try:
            cloudinary.config(
                cloud_name=cloudinary.config().cloud_name,
                api_key=cloudinary.config().api_key,
                api_secret=cloudinary.config().api_secret,
                secure=True
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully connected to Cloudinary cloud: {cloudinary.config().cloud_name}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Cloudinary connection failed: {e}"))
            return

        # Get all products with an image field
        products_with_images = Product.objects.filter(image__isnull=False).exclude(image__exact='')
        total_products = products_with_images.count()
        self.stdout.write(f"Found {total_products} products with image references in the database.")

        found_count = 0
        not_found_count = 0

        for product in products_with_images:
            # Safely handle the image reference
            if not product.image:
                self.stdout.write(self.style.WARNING(
                    f"  [SKIPPED] Product '{product.name}' has no image reference."
                ))
                continue
                
            try:
                public_id = str(product.image)
                if not public_id or public_id == 'None':
                    self.stdout.write(self.style.WARNING(
                        f"  [SKIPPED] Product '{product.name}' has empty image reference."
                    ))
                    continue
            except (TypeError, AttributeError):
                self.stdout.write(self.style.WARNING(
                    f"  [SKIPPED] Product '{product.name}' has invalid image reference."
                ))
                continue
            
            try:
                # Check if the resource exists in Cloudinary
                resource = cloudinary.api.resource(public_id)
                if resource:
                    self.stdout.write(self.style.SUCCESS(f"  [FOUND] Image for '{product.name}' exists in Cloudinary (Public ID: {public_id})"))
                    found_count += 1
                else:
                    # This case might not be hit if resource() throws an exception for not found
                    self.stdout.write(self.style.WARNING(f"  [NOT FOUND] Image for '{product.name}' with Public ID '{public_id}' not found in Cloudinary."))
                    not_found_count += 1
            except cloudinary.api.NotFound:
                self.stdout.write(self.style.WARNING(f"  [NOT FOUND] Image for '{product.name}' with Public ID '{public_id}' not found in Cloudinary."))
                not_found_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [ERROR] An error occurred while checking for '{product.name}' (Public ID: {public_id}): {e}"))
                not_found_count += 1

        self.stdout.write("\n" + "="*50)
        self.stdout.write("Verification Summary:")
        self.stdout.write(self.style.SUCCESS(f"Images found: {found_count}/{total_products}"))
        self.stdout.write(self.style.WARNING(f"Images not found: {not_found_count}/{total_products}"))
        self.stdout.write("="*50 + "\n")

        if not_found_count > 0:
            self.stdout.write(self.style.NOTICE("Consider running 'python manage.py process_scraped_images' to re-upload missing images."))
