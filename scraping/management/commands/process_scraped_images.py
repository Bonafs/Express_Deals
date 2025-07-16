from django.core.management.base import BaseCommand
from scraping.models import ScrapedProduct
from products.models import Product
from io import BytesIO
import requests
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process existing ScrapedProducts: download their images, upload to Cloudinary, and assign to Product.image.'

    def handle(self, *args, **options):
        self.stdout.write("Starting image processing for scraped products...")
        count = 0
        processed_count = 0
        
        # Filter for products that have been scraped but don't have an image yet
        scraped_products = ScrapedProduct.objects.filter(
            is_processed=True, 
            imported_product__isnull=False, 
            imported_product__image__isnull=True,
            image_url__isnull=False
        ).exclude(image_url__exact='')

        total_products = scraped_products.count()
        self.stdout.write(f"Found {total_products} products needing an image.")

        for scraped in scraped_products:
            product = scraped.imported_product
            processed_count += 1
            self.stdout.write(f"Processing product {processed_count}/{total_products}: {product.name}")

            try:
                # Download image from URL
                response = requests.get(scraped.image_url, timeout=15)
                response.raise_for_status()  # Raise an exception for bad status codes

                if 'image' not in response.headers.get('Content-Type', ''):
                    self.stdout.write(self.style.WARNING(f'URL did not return a valid image for {product.name}: {scraped.image_url}'))
                    continue

                image_content = BytesIO(response.content)
                
                # Upload image content to Cloudinary
                upload_result = upload(
                    image_content,
                    folder="products",
                    public_id=f"product_{product.id}_{scraped.id}",
                    overwrite=True
                )
                
                # Save the public_id to the product's image field
                product.image = upload_result['public_id']
                product.save()
                
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded image for product: {product.name}'))

            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f'Failed to download image for {product.name} from {scraped.image_url}: {e}'))
            except CloudinaryError as e:
                self.stdout.write(self.style.WARNING(f'Failed to upload image to Cloudinary for {product.name}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An unexpected error occurred for {product.name}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully processed and uploaded images for {count} out of {total_products} products.'))
