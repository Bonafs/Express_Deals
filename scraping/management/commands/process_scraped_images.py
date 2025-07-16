from django.core.management.base import BaseCommand
from django.db.models import Q

from scraping.models import ScrapedProduct
from products.models import Product
from io import BytesIO
import requests
import cloudinary
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError, NotFound
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = (
        'Verifies and processes images for all products. It finds products '
        'missing a valid Cloudinary image, retrieves their original scraped '
        'URL, and uploads the image.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting comprehensive image verification and processing..."
        ))

        # Find all products that are missing a valid Cloudinary image public_id
        products_to_fix = Product.objects.filter(
            Q(image__isnull=True) | Q(image__exact='')
        )
        total_to_fix = products_to_fix.count()

        if total_to_fix == 0:
            self.stdout.write(self.style.NOTICE(
                "No products found needing an image fix. All products seem to have an image reference."
            ))
            self.stdout.write(self.style.WARNING(
                "If images are still not showing, run verify_cloudinary_images to check for broken links."
            ))
            return

        self.stdout.write(
            f"Found {total_to_fix} products that need an image."
        )

        uploaded_count = 0
        checked_count = 0
        not_found_count = 0

        for product in products_to_fix:
            checked_count += 1
            self.stdout.write(
                f"\n({checked_count}/{total_to_fix}) Processing product: {product.name}"
            )

            # Find the corresponding ScrapedProduct to get the image_url
            scraped_product = ScrapedProduct.objects.filter(
                imported_product=product
            ).first()

            if not scraped_product or not scraped_product.image_url:
                self.stdout.write(self.style.WARNING(
                    "  - Status: No corresponding scraped product with an image URL found."
                ))
                not_found_count += 1
                continue

            self.stdout.write(
                f"  - Action: Found image URL. Attempting to download from {scraped_product.image_url}"
            )
            try:
                # Download image from URL
                response = requests.get(scraped_product.image_url, timeout=15)
                response.raise_for_status()

                if 'image' not in response.headers.get('Content-Type', ''):
                    self.stdout.write(self.style.ERROR(
                        "    - Error: URL did not return a valid image."
                    ))
                    continue

                image_content = BytesIO(response.content)

                # Define a more specific public_id
                public_id = f"product_{product.id}_{product.slug}"

                self.stdout.write(
                    f"  - Action: Uploading to Cloudinary with Public ID: {public_id}"
                )

                # Upload image content to Cloudinary
                upload_result = upload(
                    image_content,
                    folder="products",
                    public_id=public_id,
                    overwrite=True
                )

                # Save the public_id to the product's image field
                product.image = upload_result['public_id']
                product.save()

                uploaded_count += 1
                self.stdout.write(self.style.SUCCESS(
                    "    - Success: Image uploaded and product updated."
                ))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(
                    f"    - Error downloading image: {e}"
                ))
            except CloudinaryError as e:
                self.stdout.write(self.style.ERROR(
                    f"    - Error uploading to Cloudinary: {e}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"    - An unexpected error occurred: {e}"
                ))

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Image Processing Complete!"))
        self.stdout.write(f"Total Products Checked: {total_to_fix}")
        self.stdout.write(f"New Images Uploaded: {uploaded_count}")
        self.stdout.write(f"Products without a source URL: {not_found_count}")
        self.stdout.write("=" * 50)
