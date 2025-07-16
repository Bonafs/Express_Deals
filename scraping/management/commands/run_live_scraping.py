from django.core.management.base import BaseCommand
from scraping.models import ScrapeTarget
from scraping.scrapers import ProductScraper
from products.models import Product
import time


class Command(BaseCommand):
    help = 'Run live web scraping to replace demo data with real UK products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup-targets',
            action='store_true',
            help='Set up scraping targets for UK retailers before scraping',
        )
        parser.add_argument(
            '--clear-demo',
            action='store_true',
            help='Clear existing demo products before scraping',
        )
        parser.add_argument(
            '--max-products',
            type=int,
            default=30,
            help='Maximum number of products to scrape (default: 30)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🚀 STARTING LIVE WEB SCRAPING"))
        self.stdout.write("Replacing demo data with real UK products...")
        
        # Setup targets if requested
        if options['setup_targets']:
            self.stdout.write("\n📋 Setting up UK retail scraping targets...")
            from django.core.management import call_command
            call_command('setup_uk_targets')
            time.sleep(2)
        
        # Check if we have scrape targets
        targets = ScrapeTarget.objects.filter(status='active')
        if not targets.exists():
            self.stdout.write(
                self.style.ERROR(
                    "❌ No active scrape targets found. "
                    "Run with --setup-targets first."
                )
            )
            return
        
        self.stdout.write(f"Found {targets.count()} active scraping targets")
        
        # Clear demo products if requested
        if options['clear_demo']:
            self.stdout.write("\n🗑️ Clearing existing demo products...")
            demo_count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(f"Deleted {demo_count} demo products")
        
        # Initialize scraper
        scraper = ProductScraper()
        total_scraped = 0
        max_products = options['max_products']
        
        # Search queries for UK products
        uk_search_queries = [
            'iphone uk',
            'samsung galaxy uk',
            'dyson vacuum uk',
            'nike trainers uk',
            'adidas shoes uk',
            'marks spencer uk',
            'next clothing uk',
            'john lewis home uk'
        ]
        
        msg = f"\n🔍 Starting scraping with max {max_products} products..."
        self.stdout.write(msg)
        
        # Limit to first 3 targets to avoid overwhelming
        for i, target in enumerate(targets[:3]):
            if total_scraped >= max_products:
                break
                
            self.stdout.write(f"\n📦 Scraping from {target.name}...")
            
            # Use different search queries for variety
            search_query = uk_search_queries[i % len(uk_search_queries)]
            
            try:
                # Run scraping for this target
                job = scraper.scrape_target(
                    target=target,
                    search_query=search_query,
                    max_pages=2  # Limit pages to avoid too much data
                )
                
                if job and job.products_imported > 0:
                    total_scraped += job.products_imported
                    msg = f"✅ {target.name}: {job.products_imported} imported"
                    self.stdout.write(msg)
                else:
                    self.stdout.write(
                        f"⚠️ {target.name}: No products imported"
                    )
                    
            except Exception as e:
                error_msg = f"❌ Error scraping {target.name}: {str(e)}"
                self.stdout.write(self.style.ERROR(error_msg))
                continue
            
            # Small delay between targets
            time.sleep(3)
        
        # Final status
        final_count = Product.objects.count()
        featured_count = Product.objects.filter(is_featured=True).count()
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("🎉 LIVE SCRAPING COMPLETED!"))
        self.stdout.write("📊 Final Statistics:")
        self.stdout.write(f"   • Total products in database: {final_count}")
        self.stdout.write(f"   • Featured products: {featured_count}")
        self.stdout.write(f"   • Products scraped: {total_scraped}")
        
        if final_count > 0:
            self.stdout.write("\n🌐 Your website now has REAL product data!")
            self.stdout.write("   Check your website to see live UK products")
        else:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️ No products were successfully scraped."
                )
            )
            self.stdout.write("   This could be due to:")
            self.stdout.write("   • Anti-bot protection on target sites")
            self.stdout.write("   • Network connectivity issues")
            self.stdout.write("   • Outdated CSS selectors")
            self.stdout.write("   • Rate limiting")
