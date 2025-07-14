"""
Express Deals - Web Scraping Engine
Core scraping functionality for automated product data collection
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal
import re
import logging
from django.conf import settings
from django.utils import timezone
from .models import ScrapeTarget, ScrapeJob, ScrapedProduct
from products.models import Product, Category
from urllib.parse import urljoin, urlparse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)


class BaseScraper:
    """
    Base scraper class with common functionality
    """
    
    def __init__(self, scrape_target):
        self.target = scrape_target
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Configure requests session with headers and settings"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_page(self, url, delay=True):
        """Fetch a page with error handling and rate limiting"""
        if delay:
            time.sleep(random.uniform(1, 3))  # Random delay to be respectful
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_price(self, price_text):
        """Extract price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract number
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            try:
                return Decimal(price_match.group())
            except:
                pass
        return None
    
    def extract_product_data(self, soup, product_element):
        """Extract product data from HTML element"""
        data = {}
        
        try:
            # Title
            title_elem = product_element.select_one(self.target.title_selector)
            data['title'] = title_elem.get_text(strip=True) if title_elem else ''
            
            # Price
            price_elem = product_element.select_one(self.target.price_selector)
            if price_elem:
                data['price'] = self.parse_price(price_elem.get_text(strip=True))
            
            # Image
            img_elem = product_element.select_one(self.target.image_selector)
            if img_elem:
                data['image_url'] = img_elem.get('src') or img_elem.get('data-src') or ''
            
            # URL
            url_elem = product_element.select_one(self.target.url_selector)
            if url_elem:
                data['product_url'] = url_elem.get('href', '')
                if data['product_url'].startswith('/'):
                    data['product_url'] = self.target.base_url + data['product_url']
            
            # Rating (optional)
            if self.target.rating_selector:
                rating_elem = product_element.select_one(self.target.rating_selector)
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        data['rating'] = Decimal(rating_match.group(1))
            
            return data
        
        except Exception as e:
            logger.error(f"Error extracting product data: {e}")
            return {}
    
    def download_image(self, image_url, product_name="product", max_size_mb=5):
        """
        Enhanced image download with comprehensive error handling and validation
        """
        if not image_url:
            logger.warning(f"No image URL provided for {product_name}")
            return None

        try:
            # Clean and validate URL
            image_url = image_url.strip()
            parsed_url = urlparse(image_url)
            
            if not parsed_url.scheme:
                logger.warning(f"Invalid image URL scheme for {product_name}: {image_url}")
                return None

            logger.info(f"Attempting to download image for {product_name}: {image_url}")

            # Download with retries
            for attempt in range(self.max_retries):
                try:
                    response = self.session.get(
                        image_url, 
                        timeout=30,
                        headers={'Referer': image_url}
                    )
                    response.raise_for_status()
                    
                    # Check content type
                    content_type = response.headers.get('content-type', '').lower()
                    if not content_type.startswith('image/'):
                        logger.warning(f"Invalid content type for {product_name}: {content_type}")
                        return None

                    # Check file size
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                        logger.warning(f"Image too large for {product_name}: {content_length} bytes")
                        return None

                    image_content = response.content
                    if len(image_content) > max_size_mb * 1024 * 1024:
                        logger.warning(f"Downloaded image too large for {product_name}: {len(image_content)} bytes")
                        return None

                    # Validate image content
                    try:
                        img = Image.open(BytesIO(image_content))
                        img.verify()
                        
                        # Reset stream for actual processing
                        image_stream = BytesIO(image_content)
                        img = Image.open(image_stream)
                        
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        # Resize if too large
                        max_dimension = 1200
                        if img.width > max_dimension or img.height > max_dimension:
                            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                        
                        # Save processed image
                        output_stream = BytesIO()
                        img.save(output_stream, format='JPEG', quality=85, optimize=True)
                        output_stream.seek(0)
                        
                        # Generate filename
                        file_extension = 'jpg'
                        safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        filename = f"products/{safe_name[:50]}_{int(time.time())}.{file_extension}"
                        
                        logger.info(f"Successfully processed image for {product_name}: {filename}")
                        return ContentFile(output_stream.getvalue(), name=filename)
                        
                    except Exception as img_error:
                        logger.error(f"Image validation failed for {product_name}: {str(img_error)}")
                        return None
                        
                except requests.RequestException as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {product_name}: {str(e)}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                    continue
                    
                break  # Success, exit retry loop
                
        except Exception as e:
            logger.error(f"Unexpected error downloading image for {product_name}: {str(e)}")
            return None

        logger.error(f"Failed to download image for {product_name} after {self.max_retries} attempts")
        return None

    def get_fallback_image(self):
        """
        Get fallback image path for products without images
        """
        return 'media/products/default.jpg'


class SeleniumScraper(BaseScraper):
    """
    Selenium-based scraper for JavaScript-heavy sites
    """
    
    def __init__(self, scrape_target):
        super().__init__(scrape_target)
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            self.driver = None
    
    def get_page_selenium(self, url, wait_for_selector=None):
        """Fetch page using Selenium"""
        if not self.driver:
            return None
        
        try:
            self.driver.get(url)
            
            if wait_for_selector:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
                )
            
            time.sleep(random.uniform(2, 4))
            return self.driver.page_source
        
        except Exception as e:
            logger.error(f"Error fetching {url} with Selenium: {e}")
            return None
    
    def __del__(self):
        if self.driver:
            self.driver.quit()


class ProductScraper:
    """
    Main product scraper that coordinates scraping operations
    """
    
    def __init__(self):
        self.scrapers = {}
        self.products_data = [
            # Electronics Category
            {
                'name': 'Sony PlayStation 5',
                'description': 'Next-generation gaming console with ultra-high speed SSD and ray tracing.',
                'price': 449.99,
                'original_price': 499.99,
                'category': 'Electronics',
                'stock_quantity': 10,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500'
            },
            {
                'name': 'Dyson V15 Detect',
                'description': 'Advanced cordless vacuum with laser dust detection technology.',
                'price': 649.99,
                'original_price': 749.99,
                'category': 'Electronics',
                'stock_quantity': 15,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=500'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Premium smartphone with advanced camera system and S Pen.',
                'price': 1199.99,
                'original_price': 1299.99,
                'category': 'Electronics',
                'stock_quantity': 25,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500'
            },
            {
                'name': 'iPhone 15 Pro Max',
                'description': 'Latest iPhone with titanium design and advanced pro camera system.',
                'price': 1099.99,
                'original_price': 1199.99,
                'category': 'Electronics',
                'stock_quantity': 20,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500'
            },
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
                'price': 149.99,
                'original_price': 199.99,
                'category': 'Electronics',
                'stock_quantity': 25,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'
            },
            {
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with touch controls and USB charging port.',
                'price': 59.99,
                'original_price': 79.99,
                'category': 'Electronics',
                'stock_quantity': 15,
                'is_active': True,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500'
            },
            
            # Clothing Category
            {
                'name': 'Barbour Classic Jacket',
                'description': 'Traditional British waxed cotton jacket, perfect for outdoor activities.',
                'price': 395.00,
                'original_price': 450.00,
                'category': 'Clothing',
                'stock_quantity': 12,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5d?w=500'
            },
            {
                'name': 'Nike Air Max UK Edition',
                'description': 'Limited edition Nike Air Max sneakers with Union Jack design elements.',
                'price': 140.00,
                'original_price': 180.00,
                'category': 'Clothing',
                'stock_quantity': 30,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'
            },
            {
                'name': 'British Designer Wool Coat',
                'description': 'Luxury wool coat from renowned British fashion house, tailored fit.',
                'price': 320.00,
                'original_price': 400.00,
                'category': 'Clothing',
                'stock_quantity': 8,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=500'
            },
            {
                'name': 'Organic Cotton T-Shirt',
                'description': 'Comfortable 100% organic cotton t-shirt available in multiple colors.',
                'price': 19.99,
                'original_price': 29.99,
                'category': 'Clothing',
                'stock_quantity': 50,
                'is_active': True,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'
            },
            
            # Home & Garden Category
            {
                'name': 'Royal Doulton Tea Set',
                'description': 'Elegant bone china tea set featuring classic British patterns.',
                'price': 125.00,
                'original_price': 165.00,
                'category': 'Home & Garden',
                'stock_quantity': 15,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1594398901394-4e34939a4fd0?w=500'
            },
            {
                'name': 'Stainless Steel Water Bottle',
                'description': 'Insulated stainless steel water bottle that keeps drinks cold for 24 hours.',
                'price': 24.99,
                'original_price': 39.99,
                'category': 'Home & Garden',
                'stock_quantity': 30,
                'is_active': True,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=500'
            },
            
            # Sports & Fitness Category
            {
                'name': 'Fitness Resistance Bands Set',
                'description': 'Complete set of resistance bands for home workouts with multiple resistance levels.',
                'price': 34.99,
                'original_price': 49.99,
                'category': 'Sports & Fitness',
                'stock_quantity': 20,
                'is_active': True,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500'
            }
        ]
    
    def download_image(self, image_url, product_name="product"):
        """
        Simple image download for sample products
        """
        import requests
        from django.core.files.base import ContentFile
        
        if not image_url:
            return None
            
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                return None
                
            # Create a Django file object
            image_name = f"{product_name.lower().replace(' ', '_')}.jpg"
            return ContentFile(response.content, name=image_name)
            
        except Exception as e:
            logger.warning(f"Could not download image for {product_name}: {e}")
            return None
    
    def get_fallback_image(self):
        """
        Return path to fallback image
        """
        return 'products/default.jpg'
    
    def get_scraper(self, target):
        """Get appropriate scraper for target"""
        if target.site_type in ['amazon', 'walmart']:
            return SeleniumScraper(target)
        else:
            return BaseScraper(target)
    
    def scrape_target(self, target, search_query='', max_pages=None):
        """
        Scrape products from a target site
        """
        job = ScrapeJob.objects.create(
            target=target,
            search_query=search_query,
            status='running',
            started_at=timezone.now()
        )
        
        try:
            scraper = self.get_scraper(target)
            max_pages = max_pages or target.max_pages
            
            products_found = 0
            products_imported = 0
            
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping page {page} of {target.name}")
                
                # Build search URL
                if search_query:
                    url = target.search_url_template.format(query=search_query, page=page)
                else:
                    url = target.search_url_template.format(page=page)
                
                # Get page content
                if isinstance(scraper, SeleniumScraper):
                    html_content = scraper.get_page_selenium(url, target.product_selector)
                    if not html_content:
                        continue
                    soup = BeautifulSoup(html_content, 'html.parser')
                else:
                    response = scraper.get_page(url)
                    if not response:
                        continue
                    soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract products
                product_elements = soup.select(target.product_selector)
                
                if not product_elements:
                    logger.warning(f"No products found on page {page}")
                    continue
                
                for element in product_elements:
                    product_data = scraper.extract_product_data(soup, element)
                    
                    if self.is_valid_product(product_data, target):
                        scraped_product = self.save_scraped_product(job, product_data)
                        if scraped_product:
                            products_found += 1
                            
                            # Try to import as actual product
                            if self.import_to_catalog(scraped_product):
                                products_imported += 1
                
                job.pages_scraped = page
                job.products_found = products_found
                job.products_imported = products_imported
                job.save()
            
            # Complete job
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.execution_time_seconds = (job.completed_at - job.started_at).total_seconds()
            job.save()
            
            # Update target last scraped time
            target.last_scraped = timezone.now()
            target.save()
            
            logger.info(f"Scraping completed: {products_found} found, {products_imported} imported")
            return job
        
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()
            return job
        
        finally:
            if isinstance(scraper, SeleniumScraper):
                scraper.__del__()
    
    def is_valid_product(self, product_data, target):
        """Validate scraped product data"""
        required_fields = ['title', 'price', 'image_url', 'product_url']
        
        for field in required_fields:
            if not product_data.get(field):
                return False
        
        # Price validation
        price = product_data.get('price')
        if not price:
            return False
        
        if target.min_price and price < target.min_price:
            return False
        
        if target.max_price and price > target.max_price:
            return False
        
        return True
    
    def save_scraped_product(self, job, product_data):
        """Save scraped product to database"""
        try:
            # Create external ID from URL or title
            external_id = product_data.get('product_url', '')[-50:] or product_data.get('title', '')[:50]
            
            scraped_product, created = ScrapedProduct.objects.get_or_create(
                job=job,
                external_id=external_id,
                defaults={
                    'title': product_data.get('title', ''),
                    'price': product_data.get('price', 0),
                    'original_price': product_data.get('original_price'),
                    'image_url': product_data.get('image_url', ''),
                    'product_url': product_data.get('product_url', ''),
                    'description': product_data.get('description', ''),
                    'rating': product_data.get('rating'),
                    'review_count': product_data.get('review_count'),
                    'brand': product_data.get('brand', ''),
                    'availability': product_data.get('availability', ''),
                    'shipping_info': product_data.get('shipping_info', ''),
                }
            )
            
            return scraped_product
        
        except Exception as e:
            logger.error(f"Error saving scraped product: {e}")
            return None
    
    def import_to_catalog(self, scraped_product):
        """Import scraped product to main product catalog"""
        try:
            import tempfile
            import requests
            from django.core.files import File
            # Check if product already exists
            existing = Product.objects.filter(
                name__icontains=scraped_product.title[:30]
            ).first()
            
            if existing:
                # Update price if lower
                if scraped_product.price < existing.price:
                    existing.price = scraped_product.price
                    existing.save()
                    scraped_product.imported_product = existing
                    scraped_product.is_processed = True
                    scraped_product.save()
                    return True
                return False
            
            # Download image from scraped image_url
            image_file = None
            if scraped_product.image_url:
                try:
                    logger.info(f"Attempting to download image for scraped product: {scraped_product.title} from {scraped_product.image_url}")
                    response = requests.get(scraped_product.image_url, timeout=10)
                    logger.info(f"Image download response code: {response.status_code}")
                    content_type = response.headers.get('Content-Type', '')
                    logger.info(f"Image content type: {content_type}")
                    if response.status_code == 200 and 'image' in content_type:
                        temp = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
                        temp.write(response.content)
                        temp.flush()
                        image_file = File(temp, name=f"scraped_{scraped_product.external_id}.jpg")
                        logger.info(f"Image file prepared for product: {scraped_product.title}")
                    else:
                        logger.warning(f"Image URL did not return a valid image: {scraped_product.image_url}")
                except Exception as img_exc:
                    logger.warning(f"Could not download image for scraped product: {img_exc}")
            else:
                logger.info(f"No image URL found for scraped product: {scraped_product.title}")

            # Create new product with image if available
            product = Product(
                name=scraped_product.title[:200],
                description=scraped_product.description or f"Imported from {scraped_product.job.target.name}",
                price=scraped_product.price,
                category=scraped_product.job.target.category,
                is_active=True,
                stock_quantity=100,  # Default stock
            )
            if image_file:
                logger.info(f"Saving image for product: {product.name}")
                product.image.save(image_file.name, image_file, save=False)
            else:
                logger.info(f"No image file to save for product: {product.name}")
            product.save()

            scraped_product.imported_product = product
            scraped_product.is_processed = True
            scraped_product.save()

            logger.info(f"Product imported: {product.name} (ID: {product.id}) | Image: {'Yes' if product.image else 'No'}")
            return True
        except Exception as e:
            logger.error(f"Error importing product: {e}")
            return False

    def import_sample_products(self, clear_existing=False):
        """
        Import comprehensive sample products with enhanced image handling
        """
        from products.models import Product, Category
        
        logger.info("Starting comprehensive sample product import")
        
        if clear_existing:
            logger.info("Clearing existing products...")
            Product.objects.all().delete()
            logger.info("All existing products deleted")
        
        imported_count = 0
        updated_count = 0
        failed_count = 0
        
        for product_data in self.products_data:
            try:
                # Get or create category
                category, created = Category.objects.get_or_create(
                    name=product_data['category']
                )
                if created:
                    logger.info(f"Created new category: {category.name}")

                # Check if product already exists (by name)
                existing_product = Product.objects.filter(
                    name=product_data['name']
                ).first()
                
                if existing_product:
                    # Update existing product
                    existing_product.description = product_data['description']
                    existing_product.price = product_data['price']
                    existing_product.original_price = product_data['original_price']
                    existing_product.category = category
                    existing_product.stock_quantity = product_data['stock_quantity']
                    existing_product.is_active = product_data['is_active']
                    existing_product.is_featured = product_data['is_featured']
                    
                    # Fix empty slug issue
                    if not existing_product.slug:
                        from django.utils.text import slugify
                        base_slug = slugify(product_data['name'])
                        slug = base_slug
                        counter = 1
                        while Product.objects.filter(slug=slug).exclude(id=existing_product.id).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        existing_product.slug = slug
                        logger.info(f"Fixed empty slug for: {product_data['name']} -> {slug}")
                    
                    # Handle image download if no image exists
                    if not existing_product.image and product_data.get('image_url'):
                        logger.info(f"Downloading image for existing product: {product_data['name']}")
                        image_file = self.download_image(
                            product_data['image_url'], 
                            product_data['name']
                        )
                        if image_file:
                            existing_product.image.save(image_file.name, image_file, save=False)
                            logger.info(f"Added image to existing product: {product_data['name']}")
                    
                    existing_product.save()
                    updated_count += 1
                    logger.info(f"Updated existing product: {product_data['name']}")
                    continue

                # Create new product instance
                from django.utils.text import slugify
                
                # Generate unique slug
                base_slug = slugify(product_data['name'])
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                product = Product(
                    name=product_data['name'],
                    slug=slug,
                    description=product_data['description'],
                    price=product_data['price'],
                    original_price=product_data['original_price'],
                    category=category,
                    stock_quantity=product_data['stock_quantity'],
                    is_active=product_data['is_active'],
                    is_featured=product_data['is_featured']
                )

                # Handle image download with fallback
                if product_data.get('image_url'):
                    logger.info(f"Downloading image for: {product_data['name']}")
                    image_file = self.download_image(
                        product_data['image_url'], 
                        product_data['name']
                    )
                    
                    if image_file:
                        product.image.save(image_file.name, image_file, save=False)
                        logger.info(f"Successfully set image for: {product_data['name']}")
                    else:
                        # Use default image as fallback
                        product.image = self.get_fallback_image()
                        logger.warning(f"Using fallback image for: {product_data['name']}")

                # Save product
                product.save()
                imported_count += 1
                logger.info(f"Successfully imported new product: {product_data['name']}")
                
                # Small delay to avoid overwhelming servers
                time.sleep(1)
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to import/update product {product_data['name']}: {str(e)}")
                continue

        logger.info(f"Product import completed. New: {imported_count}, Updated: {updated_count}, Failed: {failed_count}")
        return imported_count, updated_count, failed_count
