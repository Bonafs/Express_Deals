from django.core.management.base import BaseCommand
from scraping.scrapers import WorldClassProductScraper


class Command(BaseCommand):
    help = 'Add comprehensive sample products with images to the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing products before importing',
        )

    def handle(self, *args, **options):
        # Create WorldClassProductScraper instance and import sample products
        scraper = WorldClassProductScraper()
        try:
            new_count, updated_count, failed_count = scraper.import_sample_products(
                clear_existing=options['clear']
            )
            
            if options['clear']:
                self.stdout.write(
                    self.style.WARNING('Cleared all existing products')
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Product import completed:\n'
                    f'- New products: {new_count}\n'
                    f'- Updated products: {updated_count}\n'
                    f'- Failed imports: {failed_count}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error importing sample products: {str(e)}'
                )
            )
