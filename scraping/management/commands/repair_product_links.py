from django.core.management.base import BaseCommand
from products.models import Product
from scraping.models import ScrapedProduct


class Command(BaseCommand):
    help = (
        'Attempts to re-link products to their original scraped data based '
        'on product name.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "Starting product link repair process..."
        ))

        # Find scraped products that have not been linked to a Product instance
        unlinked_scraped_products = ScrapedProduct.objects.filter(
            imported_product__isnull=True
        )
        total_unlinked = unlinked_scraped_products.count()

        if total_unlinked == 0:
            self.stdout.write(self.style.NOTICE(
                "No unlinked scraped products found. "
                "All scraped data seems to be correctly associated."
            ))
            return

        self.stdout.write(
            f"Found {total_unlinked} scraped products that are not linked to "
            f"a final product."
        )

        relinked_count = 0
        match_not_found_count = 0

        for scraped_product in unlinked_scraped_products:
            self.stdout.write(
                f"\nAttempting to find a product match for scraped item: "
                f"'{scraped_product.title}'"
            )

            # Find a product with the same name (case-insensitive)
            product_match = Product.objects.filter(
                name__iexact=scraped_product.title
            ).first()

            if product_match:
                try:
                    # Link the scraped product to the existing product
                    scraped_product.imported_product = product_match
                    # Mark as processed to avoid re-linking
                    scraped_product.is_processed = True
                    scraped_product.save()

                    relinked_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  [SUCCESS] Linked to Product ID: "
                        f"{product_match.id}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"  [ERROR] Could not link to Product ID "
                        f"{product_match.id}: {e}"
                    ))
            else:
                match_not_found_count += 1
                self.stdout.write(self.style.WARNING(
                    f"  [NOT FOUND] No matching product found in the "
                    f"database for '{scraped_product.title}'."
                ))

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Repair Process Complete!"))
        self.stdout.write(f"Total Scraped Products Checked: {total_unlinked}")
        self.stdout.write(self.style.SUCCESS(
            f"Successfully Re-linked: {relinked_count}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Matching Product Not Found: {match_not_found_count}"
        ))
        self.stdout.write("=" * 50)
