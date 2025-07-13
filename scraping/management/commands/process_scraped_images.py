from django.core.management.base import BaseCommand
from scraping.models import ScrapedProduct
from products.models import Product
from django.core.files import File
import tempfile
import requests

class Command(BaseCommand):
    help = 'Process existing ScrapedProducts: download their images, upload to Cloudinary, and assign to Product.image.'

    def handle(self, *args, **options):
        count = 0
        for scraped in ScrapedProduct.objects.filter(is_processed=True, imported_product__isnull=False):
            product = scraped.imported_product
            if not product.image and scraped.image_url:
                try:
                    response = requests.get(scraped.image_url, timeout=10)
                    if response.status_code == 200:
                        temp = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
                        temp.write(response.content)
                        temp.flush()
                        product.image.save(f'scraped_{scraped.external_id}.jpg', File(temp), save=True)
                        count += 1
                        self.stdout.write(self.style.SUCCESS(f'Uploaded image for product: {product.name}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Failed for {product.name}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Processed {count} products.'))
