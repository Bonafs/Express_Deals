from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Temporarily mark some products as non-featured to test pagination'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Temporarily adjusting featured products..."))

        # Get current featured products
        featured_products = Product.objects.filter(is_featured=True)
        self.stdout.write(f"Current featured products: {featured_products.count()}")
        
        # Mark half of them as non-featured to reduce overlap
        products_to_unfeature = featured_products[:8]
        
        for product in products_to_unfeature:
            product.is_featured = False
            product.save()
            self.stdout.write(f"Unmarked as featured: {product.name}")
        
        # Check new counts
        featured_count = Product.objects.filter(is_featured=True).count()
        non_featured_count = Product.objects.filter(is_featured=False).count()
        
        self.stdout.write(f"\nNew counts:")
        self.stdout.write(f"Featured products: {featured_count}")
        self.stdout.write(f"Non-featured products: {non_featured_count}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Adjustment completed!")
        self.stdout.write("Refresh your browser to see the changes.")
        self.stdout.write("Run 'python manage.py restore_featured_products' to revert.")
