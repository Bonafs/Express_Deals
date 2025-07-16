from django.core.management.base import BaseCommand
from scraping.models import ScrapeTarget
from scraping.scrapers import WorldClassProductScraper
from products.models import Product, Category
import time


class Command(BaseCommand):
    help = 'Execute world-class live scraping to get 60+ real UK products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup-targets',
            action='store_true',
            help='Setup UK retail targets before scraping',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing products before live scraping',
        )
        parser.add_argument(
            '--target-count',
            type=int,
            default=60,
            help='Target number of products to scrape (default: 60)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("🚀 WORLD-CLASS LIVE SCRAPING INITIATED")
        )
        self.stdout.write("Targeting 60+ real UK retail products...")
        
        # Setup targets if requested
        if options['setup_targets']:
            self.stdout.write("\n📋 Setting up UK retail targets...")
            from django.core.management import call_command
            call_command('setup_uk_targets')
            time.sleep(2)
        
        # Check scrape targets
        targets = ScrapeTarget.objects.filter(status='active')
        if not targets.exists():
            self.stdout.write(
                self.style.ERROR(
                    "❌ No active scrape targets. Run with --setup-targets"
                )
            )
            return
        
        self.stdout.write(f"Found {targets.count()} active retail targets")
        
        # Clear existing if requested
        if options['clear_existing']:
            existing_count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(f"🗑️ Cleared {existing_count} existing products")
        
        # Initialize world-class scraper
        scraper = WorldClassProductScraper()
        target_count = options['target_count']
        total_scraped = 0
        
        # High-value UK search queries for quality products
        premium_queries = [
            'iphone 15 uk electronics',
            'samsung galaxy s24 smartphone',
            'dyson v15 vacuum cleaner',
            'nike air max trainers uk',
            'adidas originals shoes uk',
            'sony headphones uk',
            'apple macbook pro uk',
            'dell laptop computer',
            'canon camera dslr uk',
            'fitbit smartwatch uk',
            'microsoft surface tablet',
            'beats headphones wireless',
            'lg oled tv uk',
            'samsung 4k monitor',
            'bose speakers bluetooth',
            'gopro action camera',
            'kindle paperwhite ebook',
            'nintendo switch console',
            'playstation controller',
            'xbox series controller'
        ]
        
        self.stdout.write(f"\n🎯 Targeting {target_count} products...")
        self.stdout.write("Using enterprise-grade proxy rotation...")
        
        for i, target in enumerate(targets):
            if total_scraped >= target_count:
                break
                
            progress = f"({i+1}/{targets.count()})"
            target_info = f"\n📦 Scraping {target.name} {progress}..."
            self.stdout.write(target_info)
            
            # Use different queries for variety
            query_index = i % len(premium_queries)
            search_query = premium_queries[query_index]
            
            try:
                # Execute world-class scraping
                job = scraper.scrape_target(
                    target=target,
                    search_query=search_query,
                    max_pages=2  # Reduced for all 24 retailers
                )
                
                if job and job.products_imported > 0:
                    total_scraped += job.products_imported
                    self.stdout.write(
                        f"✅ {target.name}: +{job.products_imported} products"
                    )
                    
                    # Progress update
                    remaining = max(0, target_count - total_scraped)
                    self.stdout.write(
                        f"📈 Progress: {total_scraped}/{target_count} products"
                    )
                    if remaining > 0:
                        self.stdout.write(f"   Still need: {remaining} more")
                    
                else:
                    self.stdout.write(f"⚠️ {target.name}: No products found")
                    
            except Exception as e:
                error_msg = f"❌ {target.name} failed: {str(e)}"
                self.stdout.write(self.style.WARNING(error_msg))
                continue
            
            # Respectful delay between targets (shorter for 24 retailers)
            if i < len(targets) - 1:
                time.sleep(3)
        
        # Final statistics
        final_count = Product.objects.count()
        featured_count = Product.objects.filter(is_featured=True).count()
        active_count = Product.objects.filter(is_active=True).count()
        
        # Auto-feature top products
        if final_count > 0 and featured_count < 8:
            top_products = Product.objects.filter(
                is_active=True
            ).exclude(
                image__isnull=True
            ).exclude(
                image__exact=''
            )[:8]
            
            for product in top_products:
                product.is_featured = True
                product.save()
            
            featured_count = Product.objects.filter(is_featured=True).count()
            self.stdout.write(f"⭐ Auto-featured {len(top_products)} products")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS("🎉 WORLD-CLASS SCRAPING COMPLETED!")
        )
        self.stdout.write("📊 Final Statistics:")
        self.stdout.write(f"   • Total products: {final_count}")
        self.stdout.write(f"   • Active products: {active_count}")
        self.stdout.write(f"   • Featured products: {featured_count}")
        self.stdout.write(f"   • Session scraped: {total_scraped}")
        
        if final_count >= target_count:
            self.stdout.write(
                f"\n🎯 TARGET ACHIEVED! {final_count} products loaded"
            )
        elif final_count > 0:
            self.stdout.write(
                f"\n📈 Progress: {final_count}/{target_count} products"
            )
            self.stdout.write(
                f"   Still need: {target_count - final_count} more"
            )
        
        self.stdout.write(
            "\n🌐 Your Express Deals platform now has live UK retail data!"
        )
