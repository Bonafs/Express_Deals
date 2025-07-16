from django.core.management.base import BaseCommand
from products.models import Product
from scraping.models import ScrapeJob
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Test web scraping output quality for names, images, prices'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔍 TESTING SCRAPING EFFICACY & EFFICIENCY"))
        self.stdout.write("=" * 60)
        
        # Overall Statistics
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        
        self.stdout.write(f"📊 OVERALL STATISTICS:")
        self.stdout.write(f"   • Total Products: {total_products}")
        self.stdout.write(f"   • Active Products: {active_products}")
        
        if total_products == 0:
            self.stdout.write(self.style.WARNING("❌ No products found. Scraping may still be running."))
            return
        
        # Test Product Names Quality
        self.stdout.write(f"\n📝 PRODUCT NAME QUALITY ANALYSIS:")
        self.stdout.write("-" * 40)
        
        name_stats = self.analyze_product_names()
        self.stdout.write(f"   • Valid Names: {name_stats['valid_count']}/{total_products}")
        self.stdout.write(f"   • Average Length: {name_stats['avg_length']:.1f} characters")
        self.stdout.write(f"   • Quality Score: {name_stats['quality_score']:.1f}%")
        
        # Test Product Prices Quality
        self.stdout.write(f"\n💰 PRODUCT PRICE QUALITY ANALYSIS:")
        self.stdout.write("-" * 40)
        
        price_stats = self.analyze_product_prices()
        self.stdout.write(f"   • Valid Prices: {price_stats['valid_count']}/{total_products}")
        self.stdout.write(f"   • Price Range: £{price_stats['min_price']:.2f} - £{price_stats['max_price']:.2f}")
        self.stdout.write(f"   • Average Price: £{price_stats['avg_price']:.2f}")
        self.stdout.write(f"   • Quality Score: {price_stats['quality_score']:.1f}%")
        
        # Test Product Images Quality
        self.stdout.write(f"\n🖼️ PRODUCT IMAGE QUALITY ANALYSIS:")
        self.stdout.write("-" * 40)
        
        image_stats = self.analyze_product_images()
        self.stdout.write(f"   • With Images: {image_stats['with_images']}/{total_products}")
        self.stdout.write(f"   • Valid URLs: {image_stats['valid_urls']}")
        self.stdout.write(f"   • Cloudinary Images: {image_stats['cloudinary_count']}")
        self.stdout.write(f"   • Quality Score: {image_stats['quality_score']:.1f}%")
        
        # Recent Scraping Performance
        self.stdout.write(f"\n⚡ SCRAPING PERFORMANCE ANALYSIS:")
        self.stdout.write("-" * 40)
        
        performance_stats = self.analyze_scraping_performance()
        self.stdout.write(f"   • Recent Jobs: {performance_stats['recent_jobs']}")
        self.stdout.write(f"   • Success Rate: {performance_stats['success_rate']:.1f}%")
        self.stdout.write(f"   • Products/Hour: {performance_stats['products_per_hour']:.1f}")
        
        # Sample High-Quality Products
        self.stdout.write(f"\n🌟 SAMPLE HIGH-QUALITY PRODUCTS:")
        self.stdout.write("-" * 40)
        
        self.show_sample_products()
        
        # Overall Quality Assessment
        overall_score = (
            name_stats['quality_score'] + 
            price_stats['quality_score'] + 
            image_stats['quality_score']
        ) / 3
        
        self.stdout.write(f"\n🎯 OVERALL QUALITY ASSESSMENT:")
        self.stdout.write("=" * 40)
        self.stdout.write(f"   📊 Overall Quality Score: {overall_score:.1f}%")
        
        if overall_score >= 80:
            self.stdout.write(self.style.SUCCESS("   ✅ EXCELLENT - World-class scraping quality!"))
        elif overall_score >= 60:
            self.stdout.write(self.style.WARNING("   ⚠️ GOOD - Acceptable quality with room for improvement"))
        else:
            self.stdout.write(self.style.ERROR("   ❌ POOR - Quality needs significant improvement"))
    
    def analyze_product_names(self):
        """Analyze product name quality"""
        products = Product.objects.all()
        valid_names = 0
        total_length = 0
        
        for product in products:
            if product.name and len(product.name.strip()) >= 10:
                valid_names += 1
            if product.name:
                total_length += len(product.name)
        
        avg_length = total_length / max(1, products.count())
        quality_score = (valid_names / max(1, products.count())) * 100
        
        return {
            'valid_count': valid_names,
            'avg_length': avg_length,
            'quality_score': quality_score
        }
    
    def analyze_product_prices(self):
        """Analyze product price quality"""
        products = Product.objects.all()
        valid_prices = products.filter(price__gt=0).count()
        
        prices = [p.price for p in products if p.price and p.price > 0]
        
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) / len(prices) if prices else 0
        
        quality_score = (valid_prices / max(1, products.count())) * 100
        
        return {
            'valid_count': valid_prices,
            'min_price': min_price,
            'max_price': max_price,
            'avg_price': avg_price,
            'quality_score': quality_score
        }
    
    def analyze_product_images(self):
        """Analyze product image quality"""
        products = Product.objects.all()
        with_images = products.exclude(image__isnull=True).exclude(image__exact='').count()
        
        # Count valid image URLs
        valid_urls = 0
        cloudinary_count = 0
        
        for product in products:
            if product.image:
                valid_urls += 1
                if 'cloudinary' in str(product.image):
                    cloudinary_count += 1
        
        quality_score = (with_images / max(1, products.count())) * 100
        
        return {
            'with_images': with_images,
            'valid_urls': valid_urls,
            'cloudinary_count': cloudinary_count,
            'quality_score': quality_score
        }
    
    def analyze_scraping_performance(self):
        """Analyze recent scraping performance"""
        recent_time = timezone.now() - timedelta(hours=24)
        recent_jobs = ScrapeJob.objects.filter(started_at__gte=recent_time)
        
        completed_jobs = recent_jobs.filter(status='completed')
        success_rate = (completed_jobs.count() / max(1, recent_jobs.count())) * 100
        
        # Calculate products per hour
        total_products = sum(job.products_imported for job in recent_jobs)
        products_per_hour = total_products / max(1, 24)  # Last 24 hours
        
        return {
            'recent_jobs': recent_jobs.count(),
            'success_rate': success_rate,
            'products_per_hour': products_per_hour
        }
    
    def show_sample_products(self):
        """Show sample high-quality products"""
        high_quality_products = Product.objects.filter(
            is_active=True,
            price__gt=0
        ).exclude(
            image__isnull=True
        ).exclude(
            image__exact=''
        )[:5]
        
        for i, product in enumerate(high_quality_products, 1):
            self.stdout.write(f"   {i}. {product.name[:45]}...")
            self.stdout.write(f"      💰 Price: £{product.price}")
            self.stdout.write(f"      🖼️ Image: {'✅' if product.image else '❌'}")
            self.stdout.write(f"      📂 Category: {product.category.name if product.category else 'None'}")
            if i < len(high_quality_products):
                self.stdout.write("")
