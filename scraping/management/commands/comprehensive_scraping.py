from django.core.management.base import BaseCommand
from scraping.models import ScrapeTarget
from scraping.scrapers import ProductScraper
from products.models import Product
import time
import random


class Command(BaseCommand):
    help = 'Comprehensive scraping of all 24 UK retailers to get 60+ products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--target-count',
            type=int,
            default=60,
            help='Target number of products to scrape (default: 60)',
        )
        parser.add_argument(
            '--setup-first',
            action='store_true',
            help='Setup scraping targets before running',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing products before scraping',
        )

    def handle(self, *args, **options):
        target_count = options['target_count']
        
        self.stdout.write(self.style.WARNING("🚀 COMPREHENSIVE UK RETAIL SCRAPING"))
        self.stdout.write(f"Target: {target_count} products from 24 UK retailers")
        
        # Setup targets if requested
        if options['setup_first']:
            self.stdout.write("\n📋 Setting up all UK retail targets...")
            from django.core.management import call_command
            call_command('setup_uk_targets')
            time.sleep(2)
        
        # Clear existing if requested
        if options['clear_existing']:
            existing_count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(f"🗑️ Cleared {existing_count} existing products")
        
        # Comprehensive search strategy for UK market
        uk_search_strategies = {
            'electronics': [
                'iphone 15 uk', 'samsung galaxy s24', 'macbook air',
                'sony headphones', 'nintendo switch', 'xbox series x',
                'playstation 5', 'apple watch', 'ipad pro'
            ],
            'fashion': [
                'nike trainers uk', 'adidas shoes', 'zara dress',
                'next jacket', 'h&m jeans', 'uniqlo shirt',
                'asos boots', 'marks spencer coat'
            ],
            'home_garden': [
                'ikea furniture uk', 'john lewis bedding', 'next home',
                'dunelm curtains', 'the range garden', 'b&q tools',
                'homebase paint', 'wickes kitchen'
            ],
            'sports_fitness': [
                'nike running shoes', 'adidas football boots',
                'jd sports trainers', 'gymshark leggings',
                'under armour uk', 'puma tracksuit'
            ],
            'beauty_health': [
                'boots skincare', 'superdrug makeup', 'l\'oreal uk',
                'nivea products', 'oral b toothbrush'
            ],
            'books_media': [
                'waterstones books', 'hmv vinyl', 'game console',
                'amazon books uk'
            ]
        }
        
        # Get all active targets
        targets = ScrapeTarget.objects.filter(status='active')
        if not targets.exists():
            self.stdout.write(
                self.style.ERROR(
                    "❌ No active targets found. Run with --setup-first"
                )
            )
            return
        
        self.stdout.write(f"Found {targets.count()} active scraping targets")
        
        # Initialize scraper
        scraper = ProductScraper()
        total_scraped = 0
        successful_targets = 0
        failed_targets = 0
        
        # Calculate products per target
        products_per_target = max(3, target_count // targets.count())
        
        self.stdout.write(f"\n🎯 Targeting ~{products_per_target} products per retailer")
        
        for target in targets:
            if total_scraped >= target_count:
                self.stdout.write(f"✅ Target reached: {total_scraped} products")
                break
            
            self.stdout.write(f"\n🛒 Scraping {target.name}...")
            
            # Select appropriate search queries based on target category
            category_name = target.category.name.lower() if target.category else 'electronics'
            
            # Map category to search strategy
            if 'electronics' in category_name or 'tech' in category_name:
                search_queries = uk_search_strategies['electronics']
            elif 'fashion' in category_name or 'clothing' in category_name:
                search_queries = uk_search_strategies['fashion']
            elif 'home' in category_name or 'garden' in category_name:
                search_queries = uk_search_strategies['home_garden']
            elif 'sports' in category_name or 'fitness' in category_name:
                search_queries = uk_search_strategies['sports_fitness']
            else:
                search_queries = uk_search_strategies['electronics']
            
            target_success = False
            
            # Try multiple search queries for this target
            for search_query in random.sample(search_queries, min(3, len(search_queries))):
                try:
                    self.stdout.write(f"   🔍 Searching: '{search_query}'")
                    
                    job = scraper.scrape_target(
                        target=target,
                        search_query=search_query,
                        max_pages=2
                    )
                    
                    if job and job.products_imported > 0:
                        total_scraped += job.products_imported
                        target_success = True
                        self.stdout.write(
                            f"   ✅ Found {job.products_imported} products"
                        )
                        
                        # Stop if we have enough from this target
                        if job.products_imported >= products_per_target:
                            break
                    else:
                        self.stdout.write("   ⚠️ No products found")
                    
                    # Delay between searches
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    self.stdout.write(f"   ❌ Error: {str(e)[:50]}...")
                    continue
            
            if target_success:
                successful_targets += 1
            else:
                failed_targets += 1
            
            # Longer delay between targets
            time.sleep(random.uniform(3, 6))
        
        # Auto-feature products with good images
        self.auto_feature_products()
        
        # Final statistics
        final_count = Product.objects.count()
        featured_count = Product.objects.filter(is_featured=True).count()
        with_images = Product.objects.exclude(image__isnull=True).exclude(image='').count()
        
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("🎉 COMPREHENSIVE SCRAPING COMPLETED!"))
        self.stdout.write("\n📊 Final Statistics:")
        self.stdout.write(f"   • Total products scraped: {total_scraped}")
        self.stdout.write(f"   • Products in database: {final_count}")
        self.stdout.write(f"   • Products with images: {with_images}")
        self.stdout.write(f"   • Featured products: {featured_count}")
        self.stdout.write(f"   • Successful retailers: {successful_targets}")
        self.stdout.write(f"   • Failed retailers: {failed_targets}")
        
        if final_count >= target_count:
            self.stdout.write(f"\n🎯 SUCCESS: Target of {target_count} products achieved!")
        else:
            remaining = target_count - final_count
            self.stdout.write(f"\n📈 Progress: {final_count}/{target_count} products")
            self.stdout.write(f"   Still need: {remaining} more products")
        
        self.stdout.write("\n🌐 Your Express Deals platform now has live UK retail data!")
    
    def auto_feature_products(self):
        """Automatically feature products with good images"""
        self.stdout.write("\n🌟 Auto-featuring products with good images...")
        
        # Reset all featured status
        Product.objects.update(is_featured=False)
        
        # Feature products with images, good names, and reasonable prices
        good_products = Product.objects.filter(
            image__isnull=False
        ).exclude(
            image=''
        ).exclude(
            name__icontains='placeholder'
        ).order_by('-price')[:12]  # Top 12 by price
        
        featured_count = 0
        for product in good_products:
            product.is_featured = True
            product.save()
            featured_count += 1
            self.stdout.write(f"   ⭐ Featured: {product.name[:40]}...")
        
        self.stdout.write(f"✅ Auto-featured {featured_count} products")
