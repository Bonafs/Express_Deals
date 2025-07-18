"""
Express Deals - Commercial Scraping Pipeline
Orchestrated ETL pipeline using all commercial services
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from django.utils import timezone
from .models import ScrapeTarget, ScrapeJob
from .services.fetch_service import fetch_service
from .services.extract_service import extractor
from .services.transform_service import transformer
from .services.load_service import loader

logger = logging.getLogger(__name__)


class CommercialScrapingPipeline:
    """Complete ETL pipeline for commercial-grade scraping"""
    
    def __init__(self):
        self.pipeline_stats = {
            'urls_processed': 0,
            'successful_extractions': 0,
            'successful_transforms': 0,
            'successful_loads': 0,
            'pipeline_errors': 0
        }
    
    async def execute_scraping_job(self, scrape_target: ScrapeTarget, max_pages: int = 5) -> Dict:
        """Execute complete scraping job using commercial pipeline"""
        
        # Create job record
        job = ScrapeJob.objects.create(
            target=scrape_target,
            status='running',
            started_at=timezone.now()
        )
        
        try:
            logger.info(f"Starting commercial scraping job for {scrape_target.name}")
            
            # Phase 1: Generate URLs to scrape
            urls_to_scrape = await self._generate_scraping_urls(scrape_target, max_pages)
            
            # Phase 2: Execute ETL Pipeline
            pipeline_results = await self._execute_etl_pipeline(urls_to_scrape, scrape_target, job.id)
            
            # Phase 3: Update job status
            job.status = 'completed' if pipeline_results['success'] else 'failed'
            job.completed_at = timezone.now()
            job.products_imported = pipeline_results.get('products_loaded', 0)
            job.errors_count = pipeline_results.get('total_errors', 0)
            job.save()
            
            return {
                'success': pipeline_results['success'],
                'job_id': job.id,
                'urls_processed': len(urls_to_scrape),
                'products_loaded': pipeline_results.get('products_loaded', 0),
                'total_errors': pipeline_results.get('total_errors', 0),
                'execution_time': (timezone.now() - job.started_at).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Commercial scraping job failed: {e}")
            job.status = 'failed'
            job.completed_at = timezone.now()
            job.save()
            
            return {
                'success': False,
                'job_id': job.id,
                'error': str(e)
            }
    
    async def _generate_scraping_urls(self, target: ScrapeTarget, max_pages: int) -> List[str]:
        """Generate URLs to scrape based on target configuration"""
        
        urls = []
        
        if target.target_type == 'category':
            # Generate category page URLs
            for page in range(1, max_pages + 1):
                if '?' in target.base_url:
                    url = f"{target.base_url}&page={page}"
                else:
                    url = f"{target.base_url}?page={page}"
                urls.append(url)
        
        elif target.target_type == 'search':
            # Generate search result URLs
            search_terms = target.search_terms.split(',') if target.search_terms else ['deals']
            
            for term in search_terms[:3]:  # Limit to 3 search terms
                for page in range(1, min(max_pages, 3) + 1):  # Limit pages for search
                    if '?' in target.base_url:
                        url = f"{target.base_url}&q={term.strip()}&page={page}"
                    else:
                        url = f"{target.base_url}?q={term.strip()}&page={page}"
                    urls.append(url)
        
        elif target.target_type == 'product_list':
            # Direct product list URL
            urls.append(target.base_url)
        
        else:
            # Fallback to base URL
            urls.append(target.base_url)
        
        logger.info(f"Generated {len(urls)} URLs for {target.name}")
        return urls
    
    async def _execute_etl_pipeline(self, urls: List[str], target: ScrapeTarget, job_id: int) -> Dict:
        """Execute the complete ETL pipeline"""
        
        extracted_data = []
        transformed_data = []
        total_errors = 0
        
        # Site configuration
        site_config = {
            'site_id': target.id,
            'base_url': target.base_url,
            'currency': 'GBP',
            'target_geo': 'UK',
            'category_mapping': self._get_site_category_mapping(target.name)
        }
        
        # Process URLs in batches
        batch_size = 5
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            
            # Process batch concurrently
            batch_tasks = [
                self._process_single_url(url, target, site_config)
                for url in batch_urls
            ]
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"URL processing failed: {result}")
                    total_errors += 1
                    continue
                
                if result and result.get('extracted_products'):
                    extracted_data.extend(result['extracted_products'])
                
                if result and result.get('errors'):
                    total_errors += result['errors']
        
        # Transform all extracted data
        for raw_product in extracted_data:
            try:
                transform_result = transformer.transform_product_data(raw_product, site_config)
                
                if transform_result.success and transform_result.quality_score >= 0.6:
                    transformed_data.append(transform_result.data)
                else:
                    total_errors += 1
                    logger.warning(f"Transform failed: {transform_result.validation_errors}")
                    
            except Exception as e:
                logger.error(f"Transform error: {e}")
                total_errors += 1
        
        # Load transformed data
        products_loaded = 0
        if transformed_data:
            try:
                load_result = await loader.bulk_load_products(transformed_data, job_id)
                products_loaded = load_result.get('loaded', 0)
                total_errors += load_result.get('failed', 0)
                
            except Exception as e:
                logger.error(f"Load error: {e}")
                total_errors += len(transformed_data)
        
        return {
            'success': products_loaded > 0,
            'extracted_count': len(extracted_data),
            'transformed_count': len(transformed_data),
            'products_loaded': products_loaded,
            'total_errors': total_errors
        }
    
    async def _process_single_url(self, url: str, target: ScrapeTarget, site_config: Dict) -> Dict:
        """Process a single URL through the pipeline"""
        
        try:
            # FETCH: Get page content
            fetch_result = await fetch_service.fetch_with_intelligence(url, {
                'base_delay': 3.0,
                'anti_bot_level': 'medium',
                'target_geo': 'UK'
            })
            
            if not fetch_result.success:
                return {'errors': 1, 'extracted_products': []}
            
            # EXTRACT: Parse product data
            extract_result = extractor.extract_product_data(
                fetch_result.content, 
                str(target.id), 
                url
            )
            
            if not extract_result.success:
                return {'errors': 1, 'extracted_products': []}
            
            # Find multiple products on the page
            products = self._find_multiple_products(fetch_result.content, url)
            
            # Add extraction metadata
            for product in products:
                product.update({
                    'source_url': url,
                    'scraped_at': datetime.now().isoformat(),
                    'extraction_confidence': extract_result.confidence,
                    'extraction_method': extract_result.method_used
                })
            
            return {
                'errors': 0,
                'extracted_products': products
            }
            
        except Exception as e:
            logger.error(f"URL processing failed for {url}: {e}")
            return {'errors': 1, 'extracted_products': []}
    
    def _find_multiple_products(self, html: str, url: str) -> List[Dict]:
        """Find multiple products on a page (for category/search pages)"""
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        # Common product container selectors
        product_selectors = [
            '.product-item',
            '.product-card',
            '[data-testid*="product"]',
            '.item',
            '.product',
            '.result'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements and len(elements) > 1:  # Multiple products found
                product_elements = elements[:20]  # Limit to 20 products
                break
        
        if not product_elements:
            # Single product page - extract one product
            single_product = self._extract_single_product(soup, url)
            if single_product:
                products.append(single_product)
        else:
            # Multiple products page
            for elem in product_elements:
                product = self._extract_product_from_element(elem, url)
                if product:
                    products.append(product)
        
        return products
    
    def _extract_single_product(self, soup: BeautifulSoup, url: str) -> Optional[Dict]:
        """Extract single product from product detail page"""
        
        # Basic extraction logic
        product = {}
        
        # Extract title
        title_selectors = ['h1', '.product-title', '[data-testid*="title"]', '.title']
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                product['title'] = elem.get_text(strip=True)
                break
        
        # Extract price
        price_selectors = ['.price', '.product-price', '[data-testid*="price"]', '[class*="price"]']
        for selector in price_selectors:
            elem = soup.select_one(selector)
            if elem:
                price_text = elem.get_text(strip=True)
                price = self._extract_price_value(price_text)
                if price:
                    product['price'] = price
                    break
        
        # Extract image
        img_elem = soup.select_one('img[src*="product"], img[data-src*="product"], .product-image img')
        if img_elem:
            product['images'] = [img_elem.get('src') or img_elem.get('data-src')]
        
        return product if product.get('title') and product.get('price') else None
    
    def _extract_product_from_element(self, elem, url: str) -> Optional[Dict]:
        """Extract product data from individual product element"""
        
        product = {}
        
        # Extract title
        title_elem = elem.select_one('h1, h2, h3, .title, [data-testid*="title"], a')
        if title_elem:
            product['title'] = title_elem.get_text(strip=True)
        
        # Extract price
        price_elem = elem.select_one('.price, [data-testid*="price"], [class*="price"]')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price = self._extract_price_value(price_text)
            if price:
                product['price'] = price
        
        # Extract image
        img_elem = elem.select_one('img')
        if img_elem:
            product['images'] = [img_elem.get('src') or img_elem.get('data-src')]
        
        # Extract link
        link_elem = elem.select_one('a[href]')
        if link_elem:
            href = link_elem.get('href')
            if href:
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    product['product_url'] = urljoin(url, href)
                else:
                    product['product_url'] = href
        
        return product if product.get('title') and product.get('price') else None
    
    def _extract_price_value(self, price_text: str) -> Optional[float]:
        """Extract numeric price value from text"""
        
        if not price_text:
            return None
        
        # Remove common noise
        cleaned = re.sub(r'[^\d£$.,\s]', '', price_text)
        
        # Find price patterns
        patterns = [
            r'£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*£',
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned)
            if match:
                try:
                    price_str = match.group(1).replace(',', '')
                    return float(price_str)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _get_site_category_mapping(self, site_name: str) -> Dict:
        """Get site-specific category mappings"""
        
        mappings = {
            'Amazon': {
                'electronics': 'Electronics',
                'books': 'Books',
                'clothing': 'Clothing',
                'home': 'Home & Garden'
            },
            'John Lewis': {
                'tech': 'Electronics',
                'fashion': 'Clothing',
                'home-garden': 'Home & Garden'
            },
            'Argos': {
                'technology': 'Electronics',
                'sports-leisure': 'Sports',
                'home-furniture': 'Home & Garden'
            }
        }
        
        return mappings.get(site_name, {})
    
    def get_pipeline_statistics(self) -> Dict:
        """Get pipeline performance statistics"""
        return {
            'urls_processed': self.pipeline_stats['urls_processed'],
            'successful_extractions': self.pipeline_stats['successful_extractions'],
            'successful_transforms': self.pipeline_stats['successful_transforms'],
            'successful_loads': self.pipeline_stats['successful_loads'],
            'pipeline_errors': self.pipeline_stats['pipeline_errors']
        }


# Global pipeline instance
commercial_pipeline = CommercialScrapingPipeline()
