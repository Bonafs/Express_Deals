"""
Test Commercial Scraping System
"""

from django.core.management.base import BaseCommand
from scraping.services.commercial_pipeline import commercial_pipeline
from scraping.models import ScrapeTarget
import asyncio
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test the commercial scraping pipeline'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--target-id',
            type=int,
            help='ID of scrape target to test',
            default=None
        )
        parser.add_argument(
            '--demo',
            action='store_true',
            help='Run demo test with sample data'
        )
    
    def handle(self, *args, **options):
        """Execute commercial scraping test"""
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting Commercial Scraping System Test')
        )
        
        if options['demo']:
            self.run_demo_test()
        elif options['target_id']:
            self.run_target_test(options['target_id'])
        else:
            self.list_available_targets()
    
    def run_demo_test(self):
        """Run demo test with sample data"""
        
        self.stdout.write('📊 Running Demo Test...')
        
        # Test individual services
        self.test_fetch_service()
        self.test_extract_service()
        self.test_transform_service()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Demo test completed successfully!')
        )
    
    def test_fetch_service(self):
        """Test fetch service"""
        try:
            from scraping.services.fetch_service import fetch_service
            metrics = fetch_service.get_performance_metrics()
            
            self.stdout.write(f"🌐 Fetch Service Status:")
            self.stdout.write(f"   - Success Rate: {metrics.get('success_rate', 0):.2%}")
            self.stdout.write(f"   - Total Requests: {metrics.get('total_requests', 0)}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Fetch Service Error: {e}")
            )
    
    def test_extract_service(self):
        """Test extract service with sample HTML"""
        try:
            from scraping.services.extract_service import extractor
            
            # Sample HTML for testing
            sample_html = """
            <html>
                <body>
                    <h1 class="product-title">Test Product</h1>
                    <span class="price">£19.99</span>
                    <img src="test.jpg" alt="Product image">
                </body>
            </html>
            """
            
            result = extractor.extract_product_data(sample_html, "demo", "http://test.com")
            
            self.stdout.write(f"🧠 Extract Service Status:")
            self.stdout.write(f"   - Success: {result.success}")
            self.stdout.write(f"   - Confidence: {result.confidence:.2f}")
            self.stdout.write(f"   - Method: {result.method_used}")
            
            if result.data:
                self.stdout.write(f"   - Extracted Data: {result.data}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Extract Service Error: {e}")
            )
    
    def test_transform_service(self):
        """Test transform service with sample data"""
        try:
            from scraping.services.transform_service import transformer
            
            # Sample raw data
            raw_data = {
                'title': '  Test Product  ',
                'price': '£19.99',
                'category': 'electronics',
                'images': ['http://test.com/image.jpg']
            }
            
            site_config = {
                'site_id': 1,
                'currency': 'GBP',
                'base_url': 'http://test.com'
            }
            
            result = transformer.transform_product_data(raw_data, site_config)
            
            self.stdout.write(f"🔄 Transform Service Status:")
            self.stdout.write(f"   - Success: {result.success}")
            self.stdout.write(f"   - Quality Score: {result.quality_score:.2f}")
            self.stdout.write(f"   - Transformations: {len(result.transformations_applied or [])}")
            
            if result.data:
                self.stdout.write(f"   - Transformed Data: {result.data}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Transform Service Error: {e}")
            )
    
    def run_target_test(self, target_id):
        """Run test with specific target"""
        
        try:
            target = ScrapeTarget.objects.get(id=target_id)
            
            self.stdout.write(f"🎯 Testing Target: {target.name}")
            
            # Run async pipeline
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                commercial_pipeline.execute_scraping_job(target, max_pages=1)
            )
            
            self.stdout.write(f"📈 Pipeline Results:")
            self.stdout.write(f"   - Success: {result.get('success', False)}")
            self.stdout.write(f"   - Job ID: {result.get('job_id', 'N/A')}")
            self.stdout.write(f"   - URLs Processed: {result.get('urls_processed', 0)}")
            self.stdout.write(f"   - Products Loaded: {result.get('products_loaded', 0)}")
            self.stdout.write(f"   - Execution Time: {result.get('execution_time', 0):.2f}s")
            
            if result.get('error'):
                self.stdout.write(
                    self.style.ERROR(f"❌ Error: {result['error']}")
                )
            
        except ScrapeTarget.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"❌ Target {target_id} not found")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Pipeline Error: {e}")
            )
    
    def list_available_targets(self):
        """List available scrape targets"""
        
        targets = ScrapeTarget.objects.filter(status='active')
        
        self.stdout.write("📋 Available Scrape Targets:")
        
        if not targets.exists():
            self.stdout.write("   No active targets found.")
            self.stdout.write("\n💡 Usage:")
            self.stdout.write("   python manage.py test_commercial_scraping --demo")
            return
        
        for target in targets:
            self.stdout.write(f"   {target.id}: {target.name} ({target.base_url})")
        
        self.stdout.write("\n💡 Usage:")
        self.stdout.write("   python manage.py test_commercial_scraping --target-id <ID>")
        self.stdout.write("   python manage.py test_commercial_scraping --demo")
