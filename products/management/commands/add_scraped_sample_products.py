from django.core.management.base import BaseCommand
from scraping.scrapers import ProductScraper


class Command(BaseCommand):
    help = 'Add live scraped sample products with images to the database.'

    def handle(self, *args, **options):
        # Create ProductScraper instance and import sample products
        scraper = ProductScraper()
        try:
            scraper.import_sample_products()
            self.stdout.write(
                self.style.SUCCESS('Successfully imported sample products')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error importing sample products: {str(e)}'
                )
            )
