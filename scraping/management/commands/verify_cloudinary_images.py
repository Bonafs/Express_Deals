import cloudinary
import cloudinary.api
from django.core.management.base import BaseCommand
from products.models import Product
from cloudinary.exceptions import NotFound


class Command(BaseCommand):
    help = (
        'Verifies that product images stored in the database exist in '
        'Cloudinary.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting Cloudinary image verification..."
        ))

        products_with_images = Product.objects.exclude(
            image__isnull=True
        ).exclude(image__exact='')
        total_products = products_with_images.count()

        if total_products == 0:
            self.stdout.write(self.style.WARNING(
                "No products with associated images found in the database."
            ))
            return

        self.stdout.write(
            f"Found {total_products} products with image references to verify."
        )

        found_count = 0
        missing_count = 0

        for product in products_with_images:
            # Check if product.image is None or empty
            if not product.image:
                self.stdout.write(self.style.WARNING(
                    f"  [SKIPPED] Product '{product.name}' (ID: {product.id}) "
                    f"has no image reference."
                ))
                continue
                
            # Convert image to string safely
            try:
                image_str = str(product.image)
                if not image_str or image_str == 'None':
                    self.stdout.write(self.style.WARNING(
                        f"  [SKIPPED] Product '{product.name}' (ID: {product.id}) "
                        f"has an empty image reference."
                    ))
                    continue
            except (TypeError, AttributeError):
                self.stdout.write(self.style.WARNING(
                    f"  [SKIPPED] Product '{product.name}' (ID: {product.id}) "
                    f"has an invalid image reference."
                ))
                continue

            # Check if it has public_id attribute for Cloudinary fields
            if hasattr(product.image, 'public_id'):
                public_id = product.image.public_id
            else:
                # If it's a simple string field, use the string value
                public_id = image_str
                
            if not public_id:
                self.stdout.write(self.style.WARNING(
                    f"  [SKIPPED] Product '{product.name}' (ID: {product.id}) "
                    f"has an empty Public ID."
                ))
                continue

            try:
                # This will throw an exception if the resource is not found
                cloudinary.api.resource(public_id)
                self.stdout.write(self.style.SUCCESS(
                    f"  [FOUND]  Product '{product.name}' "
                    f"(ID: {product.id}) -> Public ID: {public_id}"
                ))
                found_count += 1
            except NotFound:
                self.stdout.write(self.style.ERROR(
                    f"  [MISSING] Product '{product.name}' "
                    f"(ID: {product.id}) -> Public ID: {public_id} not found!"
                ))
                missing_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  [ERROR]  An error occurred for Product ID "
                    f"{product.id} with Public ID {public_id}: {e}"
                ))

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Verification Complete!"))
        self.stdout.write(f"Total Products Checked: {total_products}")
        self.stdout.write(self.style.SUCCESS(
            f"Images Found in Cloudinary: {found_count}"
        ))
        self.stdout.write(self.style.ERROR(
            f"Images Missing in Cloudinary: {missing_count}"
        ))
        self.stdout.write("=" * 50)

        if missing_count > 0:
            self.stdout.write(self.style.WARNING(
                "\nTo fix missing images, you can re-run the scraping "
                "process or manually upload the missing images."
            ))
