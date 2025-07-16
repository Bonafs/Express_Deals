"""
Express Deals - World-Class Web Scraping Engine
Enterprise-grade scraping with advanced anti-detection, proxy rotation, and error optimization
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
from selenium.webdriver.common.action_chains import ActionChains
from decimal import Decimal
import re
import logging
from django.conf import settings
from django.utils import timezone
from .models import ScrapeTarget, ScrapeJob, ScrapedProduct
from .proxy_manager import proxy_manager
from .performance_optimizer import scraping_optimizer
from products.models import Product, Category
from urllib.parse import urljoin, urlparse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException
)
from io import BytesIO
from PIL import Image
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import cloudscraper

logger = logging.getLogger(__name__)


class WorldClassBaseScraper:
    """
    World-class base scraper with enterprise-grade features:
    - Intelligent proxy rotation
    - Advanced anti-detection
    - Cloudflare bypass
    - Rate limiting compliance
    - Performance monitoring
    """
    
    def __init__(self, scrape_target):
        self.target = scrape_target
        self.session = None
        self.current_proxy = None
        self.request_count = 0
        self.success_count = 0
        self.ua = UserAgent()
        self.setup_session()
    
    def setup_session(self):
        """Configure advanced session with anti-detection measures"""
        # Use cloudscraper for Cloudflare bypass
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        # Get proxy from manager
        self.current_proxy = proxy_manager.get_proxy(target_country='UK')
        
        if self.current_proxy:
            self.session.proxies.update(self.current_proxy.dict)
            logger.info(f"Using proxy: {self.current_proxy.host}:{self.current_proxy.port}")
        
        # Advanced headers for stealth
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
    
    def get_page(self, url, delay=True, max_retries=3):
        """Enhanced page fetching with intelligent retry logic and error optimization"""
        # Get optimized settings based on error history
        domain = urlparse(url).netloc
        settings = scraping_optimizer.get_optimized_request_settings(domain)
        
        # Use optimized settings
        max_retries = settings['max_retries']
        timeout = settings['timeout']
        base_delay = settings['delay']
        
        if delay:
            # Use optimized delay
            delay_time = base_delay + random.uniform(0, 1)
            time.sleep(delay_time)
        
        for attempt in range(max_retries):
            start_time = time.time()
            
            try:
                # Rotate user agent occasionally
                if random.random() < 0.3:
                    self.session.headers['User-Agent'] = self.ua.random
                
                # Use premium proxy if recommended
                if settings['use_premium_proxy']:
                    self.current_proxy = proxy_manager.get_proxy(target_country='UK')
                    if self.current_proxy:
                        self.session.proxies.update(self.current_proxy.dict)
                
                response = self.session.get(url, timeout=timeout)
                response_time = time.time() - start_time
                
                self.request_count += 1
                
                if response.status_code == 200:
                    self.success_count += 1
                    
                    # Record successful proxy usage
                    if self.current_proxy:
                        proxy_manager.record_proxy_usage(
                            self.current_proxy, True, response_time
                        )
                    
                    logger.debug(f"Successfully fetched {url} in {response_time:.2f}s")
                    return response
                
                elif response.status_code in [403, 429, 503]:
                    # Record error for analysis
                    scraping_optimizer.record_error(
                        error_type='http_blocking',
                        target_url=url,
                        proxy_used=self.current_proxy.url if self.current_proxy else None,
                        http_status=response.status_code,
                        error_message=f"HTTP {response.status_code} blocking",
                        retry_count=attempt
                    )
                    
                    logger.warning(f"Blocked response {response.status_code} for {url}")
                    self._handle_blocking()
                    
                elif response.status_code == 404:
                    logger.warning(f"Page not found: {url}")
                    return None
                    
                else:
                    # Record unexpected status
                    scraping_optimizer.record_error(
                        error_type='http_error',
                        target_url=url,
                        proxy_used=self.current_proxy.url if self.current_proxy else None,
                        http_status=response.status_code,
                        error_message=f"HTTP {response.status_code}",
                        retry_count=attempt
                    )
                    logger.warning(f"Unexpected status {response.status_code} for {url}")
                
            except requests.exceptions.ProxyError:
                # Record proxy error
                scraping_optimizer.record_error(
                    error_type='proxy_error',
                    target_url=url,
                    proxy_used=self.current_proxy.url if self.current_proxy else None,
                    error_message="Proxy connection failed",
                    retry_count=attempt
                )
                logger.warning(f"Proxy error on attempt {attempt + 1}")
                self._handle_proxy_failure()
                
            except requests.exceptions.Timeout:
                # Record timeout error
                scraping_optimizer.record_error(
                    error_type='timeout',
                    target_url=url,
                    proxy_used=self.current_proxy.url if self.current_proxy else None,
                    error_message=f"Timeout after {timeout}s",
                    retry_count=attempt
                )
                logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
                
            except requests.exceptions.RequestException as e:
                # Record general request error
                scraping_optimizer.record_error(
                    error_type='request_error',
                    target_url=url,
                    proxy_used=self.current_proxy.url if self.current_proxy else None,
                    error_message=str(e),
                    retry_count=attempt
                )
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
            
            # Record failed proxy usage
            if self.current_proxy:
                proxy_manager.record_proxy_usage(self.current_proxy, False)
            
            # Progressive delay on retries with optimization
            if attempt < max_retries - 1:
                retry_delay = (attempt + 1) * base_delay + random.uniform(1, 3)
                time.sleep(retry_delay)
        
        # Record final failure
        scraping_optimizer.record_error(
            error_type='total_failure',
            target_url=url,
            proxy_used=self.current_proxy.url if self.current_proxy else None,
            error_message=f"Failed after {max_retries} attempts",
            retry_count=max_retries
        )
        
        logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None
    
    def _handle_blocking(self):
        """Handle when current proxy/session is blocked"""
        logger.info("Handling blocking - switching proxy and session")
        
        # Switch to new proxy
        old_proxy = self.current_proxy
        self.current_proxy = proxy_manager.get_proxy(target_country='UK')
        
        if self.current_proxy and self.current_proxy != old_proxy:
            self.session.proxies.update(self.current_proxy.dict)
            self.session.headers['User-Agent'] = self.ua.random
            logger.info(f"Switched to new proxy: {self.current_proxy.host}")
        else:
            # No proxies available - wait longer
            logger.warning("No alternative proxy available - waiting...")
            time.sleep(60)
    
    def _handle_proxy_failure(self):
        """Handle proxy connection failure"""
        if self.current_proxy:
            logger.warning(f"Proxy {self.current_proxy.host} failed - switching")
            proxy_manager.record_proxy_usage(self.current_proxy, False)
        
        # Get new proxy
        self.current_proxy = proxy_manager.get_proxy(target_country='UK')
        if self.current_proxy:
            self.session.proxies.update(self.current_proxy.dict)
    
    def get_success_rate(self) -> float:
        """Calculate scraping success rate"""
        if self.request_count == 0:
            return 0.0
        return (self.success_count / self.request_count) * 100
    
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
                image_src = img_elem.get('src') or img_elem.get('data-src')
                if image_src:
                    data['image_url'] = urljoin(self.target.base_url, image_src)
            else:
                # Fallback to Open Graph image
                og_image = soup.select_one("meta[property='og:image']")
                if og_image and og_image.get('content'):
                    data['image_url'] = urljoin(self.target.base_url, og_image['content'])

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


class WorldClassSeleniumScraper(WorldClassBaseScraper):
    """
    Advanced Selenium scraper with undetected Chrome and stealth features
    """
    
    def __init__(self, scrape_target):
        super().__init__(scrape_target)
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup undetected Chrome driver with stealth configuration"""
        options = uc.ChromeOptions()
        
        # Stealth options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Faster loading
        options.add_argument('--user-agent=' + self.ua.random)
        
        # Window size randomization
        window_sizes = ['1366,768', '1920,1080', '1440,900', '1536,864']
        options.add_argument(f'--window-size={random.choice(window_sizes)}')
        
        # Proxy configuration
        if self.current_proxy:
            proxy_arg = f'--proxy-server={self.current_proxy.url}'
            options.add_argument(proxy_arg)
        
        # Additional stealth measures
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            # Use undetected Chrome driver
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Execute script to remove webdriver property
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            
            logger.info("Undetected Chrome driver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            self.driver = None
    
    def get_page_selenium(self, url, wait_for_selector=None, max_retries=3):
        """Get page using Selenium with enhanced stealth"""
        if not self.driver:
            self.setup_driver()
        
        if not self.driver:
            return None
        
        for attempt in range(max_retries):
            try:
                # Human-like navigation
                self.driver.get(url)
                
                # Random scroll to simulate human behavior
                self._simulate_human_behavior()
                
                # Wait for specific selector if provided
                if wait_for_selector:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
                    )
                
                # Additional wait for dynamic content
                time.sleep(random.uniform(2, 4))
                
                return self.driver.page_source
                
            except TimeoutException:
                logger.warning(f"Timeout loading {url} on attempt {attempt + 1}")
                
            except WebDriverException as e:
                logger.error(f"WebDriver error on attempt {attempt + 1}: {e}")
                
                # Try to recover driver
                if "chrome not reachable" in str(e).lower():
                    self._recover_driver()
            
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
        
        return None
    
    def _simulate_human_behavior(self):
        """Simulate human-like browsing behavior"""
        try:
            # Random scroll
            scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            for _ in range(random.randint(1, 3)):
                scroll_to = random.randint(0, scroll_height)
                self.driver.execute_script(f"window.scrollTo(0, {scroll_to});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Occasional mouse movement
            if random.random() < 0.3:
                action = ActionChains(self.driver)
                action.move_by_offset(
                    random.randint(-100, 100), 
                    random.randint(-100, 100)
                ).perform()
            
        except Exception as e:
            logger.debug(f"Human behavior simulation failed: {e}")
    
    def _recover_driver(self):
        """Attempt to recover failed driver"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        
        time.sleep(5)
        self.setup_driver()
    
    def close(self):
        """Clean up driver resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def __del__(self):
        if self.driver:
            self.driver.quit()


class WorldClassProductScraper:
    """
    World-class product scraper with enterprise-grade features:
    - Multi-retailer support for 24+ UK stores
    - Intelligent scraper selection
    - Advanced anti-detection
    - Performance monitoring
    - Automatic failover
    """
    
    def __init__(self):
        self.scrapers = {}
        self.active_retailers = [
            'amazon_uk', 'currys', 'john_lewis', 'argos', 'tesco',
            'asda', 'sainsburys', 'marks_spencer', 'next', 'boots',
            'asos', 'very', 'ao', 'game', 'jd_sports'
        ]
        self.performance_stats = {}
        self.setup_scrapers()
    
    def setup_scrapers(self):
        """Initialize scrapers for different site types"""
        self.scrapers = {
            'requests': WorldClassBaseScraper,
            'selenium': WorldClassSeleniumScraper,
            'cloudflare': WorldClassSeleniumScraper  # Use Selenium for Cloudflare sites
        }
    
    def get_scraper(self, target):
        """Select appropriate scraper for target site"""
        # Sites that typically require JavaScript/Selenium
        selenium_sites = ['currys', 'very', 'ao', 'game', 'jd_sports']
        
        # Sites with Cloudflare protection
        cloudflare_sites = ['asos', 'next']
        
        if target.site_type in cloudflare_sites:
            return self.scrapers['cloudflare'](target)
        elif target.site_type in selenium_sites:
            return self.scrapers['selenium'](target)
        else:
            return self.scrapers['requests'](target)
    
    def scrape_target(self, target, search_query='', max_pages=None):
        """
        Scrape products from a target site using world-class techniques
        """
        logger.info(f"Starting world-class scraping for {target.name}")
        
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
                
                # Get page content with appropriate scraper
                if isinstance(scraper, WorldClassSeleniumScraper):
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
                
                # Respect rate limits
                time.sleep(random.uniform(2, 5))
            
            # Complete job
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            logger.info(f"Scraping completed: {products_found} found, {products_imported} imported")
            return job
            
        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()
            logger.error(f"Scraping failed: {e}")
            return job
        
        finally:
            # Cleanup selenium driver if used
            if isinstance(scraper, WorldClassSeleniumScraper):
                scraper.cleanup()
    
    def is_valid_product(self, product_data, target):
        """Validate scraped product data"""
        required_fields = ['title', 'price', 'image_url']
        
        for field in required_fields:
            if not product_data.get(field):
                return False
        
        # Price validation
        if target.min_price and product_data['price'] < target.min_price:
            return False
        if target.max_price and product_data['price'] > target.max_price:
            return False
        
        return True
    
    def save_scraped_product(self, job, product_data):
        """Save scraped product to database"""
        try:
            scraped_product = ScrapedProduct.objects.create(
                job=job,
                external_id=product_data.get('external_id', ''),
                title=product_data['title'],
                price=product_data['price'],
                original_price=product_data.get('original_price'),
                image_url=product_data['image_url'],
                product_url=product_data.get('product_url', ''),
                description=product_data.get('description', ''),
                rating=product_data.get('rating'),
                brand=product_data.get('brand', ''),
                availability=product_data.get('availability', 'In Stock')
            )
            return scraped_product
        except Exception as e:
            logger.error(f"Failed to save scraped product: {e}")
            return None
    
    def import_to_catalog(self, scraped_product):
        """Import scraped product to main product catalog"""
        try:
            from products.models import Product, Category
            from django.utils.text import slugify
            
            # Get or create category
            category, _ = Category.objects.get_or_create(
                name=scraped_product.job.target.category.name if scraped_product.job.target.category else 'General'
            )
            
            # Generate unique slug
            base_slug = slugify(scraped_product.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Check if product already exists
            existing_product = Product.objects.filter(
                name=scraped_product.title
            ).first()
            
            if existing_product:
                # Update existing product
                existing_product.price = scraped_product.price
                existing_product.original_price = scraped_product.original_price
                existing_product.description = scraped_product.description or existing_product.description
                existing_product.save()
                
                scraped_product.imported_product = existing_product
                scraped_product.is_processed = True
                scraped_product.save()
                
                logger.info(f"Updated existing product: {existing_product.name}")
                return True
            
            # Create new product
            product = Product.objects.create(
                name=scraped_product.title,
                slug=slug,
                description=scraped_product.description or f"Quality product from {scraped_product.job.target.name}",
                price=scraped_product.price,
                original_price=scraped_product.original_price,
                category=category,
                stock_quantity=random.randint(5, 50),
                is_active=True,
                is_featured=False  # Will be set manually for featured products
            )
            
            # Download and upload image
            if scraped_product.image_url:
                try:
                    image_content = self._download_product_image(scraped_product.image_url)
                    if image_content:
                        upload_result = upload(
                            image_content,
                            folder="products",
                            public_id=f"product_{product.id}_{slugify(product.name)}"
                        )
                        product.image = upload_result['public_id']
                        product.save()
                        logger.info(f"Successfully uploaded image for: {product.name}")
                except Exception as e:
                    logger.warning(f"Failed to upload image for {product.name}: {e}")
            
            scraped_product.imported_product = product
            scraped_product.is_processed = True
            scraped_product.save()
            
            logger.info(f"Created new product: {product.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import product to catalog: {e}")
            return False
    
    def _download_product_image(self, image_url):
        """Download product image with proxy support"""
        try:
            # Use proxy manager for image download
            proxy = proxy_manager.get_proxy(target_country='UK')
            proxies = proxy.dict if proxy else None
            
            response = requests.get(
                image_url,
                proxies=proxies,
                timeout=30,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                # Validate image
                image_content = BytesIO(response.content)
                img = Image.open(image_content)
                img.verify()
                
                # Reset stream
                image_content = BytesIO(response.content)
                return image_content
                
        except Exception as e:
            logger.warning(f"Failed to download image {image_url}: {e}")
        
        return None
    
    def get_performance_stats(self):
        """Get scraping performance statistics"""
        stats = {
            'total_retailers': len(self.active_retailers),
            'proxy_stats': proxy_manager.get_proxy_stats(),
            'scraper_performance': self.performance_stats
        }
        return stats


# Backward compatibility alias
ProductScraper = WorldClassProductScraper
