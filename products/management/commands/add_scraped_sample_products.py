from django.core.management.base import BaseCommand
from products.models import Product, Category
from scraping.scrapers import scrape_sample_products

class Command(BaseCommand):
    help = 'Add live scraped sample products with images to the database.'

    def handle(self, *args, **options):
        # Scrape sample products (implement scrape_sample_products to return a list of dicts)
        scraped_products = scrape_sample_products()
        if not scraped_products:
            self.stdout.write(self.style.ERROR('No products scraped.'))
            return

        for prod in scraped_products:
            category, _ = Category.objects.get_or_create(name=prod['category'], defaults={'slug': prod['category'].lower().replace(' ', '-')})
            product, created = Product.objects.get_or_create(
                name=prod['name'],
                defaults={
                    'slug': prod['slug'],
                    'category': category,
                    'description': prod['description'],
                    'price': prod['price'],
                    'original_price': prod.get('original_price'),
                    'stock_quantity': prod.get('stock_quantity', 10),
                    'is_active': True,
                    'is_featured': prod.get('is_featured', False),
                }
            )
            if created and prod.get('image_url'):
                # Download and save image to trigger Cloudinary upload
                import requests
                from django.core.files.base import ContentFile
                response = requests.get(prod['image_url'])
                if response.status_code == 200:
                    product.image.save(prod['slug'] + '.jpg', ContentFile(response.content), save=True)
            self.stdout.write(self.style.SUCCESS(f"Added/updated product: {product.name}"))
        self.stdout.write(self.style.SUCCESS('Sample products added.'))
