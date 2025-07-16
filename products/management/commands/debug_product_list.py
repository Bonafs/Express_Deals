from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.core.paginator import Paginator


class Command(BaseCommand):
    help = 'Debug the ProductListView pagination and filtering'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Debugging ProductListView..."))

        # Simulate the view's get_queryset method
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        self.stdout.write(f"Total active products: {queryset.count()}")
        
        # Test pagination with paginate_by = 12
        paginator = Paginator(queryset, 12)
        self.stdout.write(f"Number of pages: {paginator.num_pages}")
        self.stdout.write(f"Products per page: 12")
        
        # Check first page
        page1 = paginator.get_page(1)
        self.stdout.write(f"Page 1 - Number of products: {len(page1.object_list)}")
        
        # List first page products
        self.stdout.write("\nProducts on page 1:")
        for i, product in enumerate(page1.object_list, 1):
            self.stdout.write(f"  {i}. {product.name} (ID: {product.id}) - Active: {product.is_active}")
        
        # Check if there's a second page
        if paginator.num_pages > 1:
            page2 = paginator.get_page(2)
            self.stdout.write(f"\nPage 2 - Number of products: {len(page2.object_list)}")
            self.stdout.write("\nProducts on page 2:")
            for i, product in enumerate(page2.object_list, 1):
                self.stdout.write(f"  {i}. {product.name} (ID: {product.id}) - Active: {product.is_active}")
        
        # Check categories
        self.stdout.write(f"\nTotal categories: {Category.objects.count()}")
        for category in Category.objects.all():
            product_count = Product.objects.filter(category=category, is_active=True).count()
            self.stdout.write(f"  {category.name}: {product_count} products")
        
        # Check if any products have missing images
        products_without_images = Product.objects.filter(is_active=True).filter(
            image__isnull=True
        ).count()
        products_with_empty_images = Product.objects.filter(is_active=True).filter(
            image__exact=''
        ).count()
        
        self.stdout.write(f"\nProducts without images: {products_without_images}")
        self.stdout.write(f"Products with empty images: {products_with_empty_images}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Debug completed!")
