from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Restore featured products to show in the sidebar'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Restoring featured products..."))

        # Get products that should be featured (products with good images)
        products_to_feature = [
            'Resistance Band Set by Gymshark',
            'Chilly\'s Series 2 Water Bottle', 
            'Emma Bridgewater Polka Dot Tea Set',
            'Adidas Originals Stan Smith',
            'Sony WH-1000XM5 Headphones',
            'Nike Air Max UK Edition',
        ]
        
        featured_count = 0
        
        for product_name in products_to_feature:
            try:
                product = Product.objects.get(name=product_name)
                product.is_featured = True
                product.save()
                featured_count += 1
                self.stdout.write(f"✅ Marked as featured: {product.name}")
            except Product.DoesNotExist:
                self.stdout.write(f"❌ Product not found: {product_name}")
        
        # Check final counts
        total_featured = Product.objects.filter(is_featured=True).count()
        
        self.stdout.write(f"\nFinal counts:")
        self.stdout.write(f"Products marked as featured: {featured_count}")
        self.stdout.write(f"Total featured products: {total_featured}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Featured products restored!")
        self.stdout.write("Refresh your browser to see the sidebar.")
