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
                    response = requests.get(scraped_product.image_url, timeout=10)
                    if response.status_code == 200:
                        temp = tempfile.NamedTemporaryFile(delete=True, suffix='.jpg')
                        temp.write(response.content)
                        temp.flush()
                        image_file = File(temp, name=f"scraped_{scraped_product.external_id}.jpg")
                except Exception as img_exc:
                    logger.warning(f"Could not download image for scraped product: {img_exc}")
            
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
                product.image.save(image_file.name, image_file, save=False)
            product.save()
            
            scraped_product.imported_product = product
            scraped_product.is_processed = True
            scraped_product.save()
            
            return True
        except Exception as e:
            logger.error(f"Error importing product: {e}")
            return False
