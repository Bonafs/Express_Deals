"""
Express Deals - URL Tracking Service
Comprehensive service for checking product availability and tracking effectiveness
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from datetime import timedelta
from typing import Tuple, Optional, Dict, Any  # Add type hints
import re
from decimal import Decimal

logger = logging.getLogger(__name__)

class ValidationResult:
    """
    Structured result for URL validation to prevent parameter order confusion
    """
    def __init__(self, is_valid: bool, retailer_name: Optional[str] = None, error_message: Optional[str] = None):
        self.is_valid = is_valid
        self.retailer_name = retailer_name
        self.error_message = error_message
    
    def as_tuple(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """Return as tuple for backward compatibility"""
        return (self.is_valid, self.retailer_name, self.error_message)
    
    def __iter__(self):
        """Allow tuple unpacking"""
        yield self.is_valid
        yield self.retailer_name
        yield self.error_message


class URLTrackingService:
    """Service for URL tracking validation and availability checking"""
    
    SUPPORTED_RETAILERS = {
        'amazon.co.uk': {
            'name': 'Amazon UK',
            'price_selector': '.a-price-whole',
            'title_selector': '#productTitle',
            'availability_selector': '#availability span',
            'requires_headers': True
        },
        'currys.co.uk': {
            'name': 'Currys PC World',
            'price_selector': '.price, .current-price, [data-qa="price"], .sr-only + span',
            'title_selector': 'h1, [data-qa="product-name"], .sr-only + span',
            'availability_selector': '.stock-status, [data-qa="stock"], .availability',
            'requires_headers': True
        },
        'johnlewis.com': {
            'name': 'John Lewis',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.availability',
            'requires_headers': True
        },
        'argos.co.uk': {
            'name': 'Argos',
            'price_selector': '.price-current',
            'title_selector': 'h1',
            'availability_selector': '.stock-checker',
            'requires_headers': True
        },
        'asos.com': {
            'name': 'ASOS',
            'price_selector': '.current-price',
            'title_selector': 'h1',
            'availability_selector': '.product-stock',
            'requires_headers': True
        },
        'next.co.uk': {
            'name': 'Next',
            'price_selector': '.Price',
            'title_selector': 'h1',
            'availability_selector': '.StockMessage',
            'requires_headers': True
        },
        
        # TOP 20 UK RETAILERS - New additions for enhanced market coverage
        'tesco.com': {
            'name': 'Tesco',
            'price_selector': '.price-per-sellable-unit, .value',
            'title_selector': 'h1, .product-title',
            'availability_selector': '.availability, .stock-level',
            'requires_headers': True
        },
        'ebay.co.uk': {
            'name': 'eBay UK',
            'price_selector': '.notranslate',
            'title_selector': 'h1#x-title-label-lbl',
            'availability_selector': '.u-flL.condText',
            'requires_headers': True
        },
        'boots.com': {
            'name': 'Boots',
            'price_selector': '.pd-price, .price',
            'title_selector': 'h1, .pdp-product-name',
            'availability_selector': '.stock-level-indicator',
            'requires_headers': True
        },
        'marksandspencer.com': {
            'name': 'Marks & Spencer',
            'price_selector': '.price-current',
            'title_selector': 'h1',
            'availability_selector': '.availability-message',
            'requires_headers': True
        },
        'very.co.uk': {
            'name': 'Very',
            'price_selector': '.product-price',
            'title_selector': 'h1',
            'availability_selector': '.product-stock',
            'requires_headers': True
        },
        'asda.com': {
            'name': 'ASDA',
            'price_selector': '.co-product__price',
            'title_selector': 'h1',
            'availability_selector': '.pdp-product-availability',
            'requires_headers': True
        },
        'ao.com': {
            'name': 'AO.com',
            'price_selector': '.price-now',
            'title_selector': 'h1',
            'availability_selector': '.delivery-options',
            'requires_headers': True
        },
        'screwfix.com': {
            'name': 'Screwfix',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.availability',
            'requires_headers': True
        },
        'wickes.co.uk': {
            'name': 'Wickes',
            'price_selector': '.price-current',
            'title_selector': 'h1',
            'availability_selector': '.stock-message',
            'requires_headers': True
        },
        'dunelm.com': {
            'name': 'Dunelm',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.stock-level',
            'requires_headers': True
        },
        'diy.com': {
            'name': 'B&Q',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.stock-availability',
            'requires_headers': True
        },
        'homebase.co.uk': {
            'name': 'Homebase',
            'price_selector': '.price-now',
            'title_selector': 'h1',
            'availability_selector': '.availability-status',
            'requires_headers': True
        },
        'matalan.co.uk': {
            'name': 'Matalan',
            'price_selector': '.price-current',
            'title_selector': 'h1',
            'availability_selector': '.stock-level',
            'requires_headers': True
        },
        'zalando.co.uk': {
            'name': 'Zalando UK',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.availability',
            'requires_headers': True
        },
        'sportsdirect.com': {
            'name': 'Sports Direct',
            'price_selector': '.price, .CurrentPrice',
            'title_selector': 'h1',
            'availability_selector': '.stockMessage',
            'requires_headers': True
        },
        'jdsports.co.uk': {
            'name': 'JD Sports',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.stock-message',
            'requires_headers': True
        },
        'wayfair.co.uk': {
            'name': 'Wayfair UK',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.delivery-message',
            'requires_headers': True
        },
        'hmv.com': {
            'name': 'HMV',
            'price_selector': '.price',
            'title_selector': 'h1',
            'availability_selector': '.stock-level',
            'requires_headers': True
        }
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def validate_url(self, url) -> ValidationResult:
        """
        Validate if URL is from a supported retailer
        Returns: ValidationResult(is_valid, retailer_name, error_message)
        """
        try:
            if not url or not isinstance(url, str):
                return ValidationResult(False, None, "URL is required")
            
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                return ValidationResult(False, None, 
                                      "URL must start with http:// or https://")
            
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Remove www. prefix for comparison
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Check against supported retailers
            for supported_domain, retailer_info in self.SUPPORTED_RETAILERS.items():
                if domain == supported_domain or domain.endswith('.' + supported_domain):
                    return ValidationResult(True, retailer_info['name'], None)
            
            # Not a supported retailer
            supported_sites = list(self.SUPPORTED_RETAILERS.keys())
            error_msg = f"URL must be from a supported retailer: {', '.join(supported_sites)}"
            return ValidationResult(False, None, error_msg)
            
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return ValidationResult(False, None, f"Invalid URL format: {str(e)}")
    
    def check_product_availability(self, url, timeout=10):
        """
        Check if product URL is accessible and contains valid product data
        Returns: {
            'available': bool,
            'title': str,
            'price': Decimal,
            'currency': str,
            'stock_status': str,
            'retailer': str,
            'error': str
        }
        """
        try:
            # Validate URL first
            validation_result = self.validate_url(url)
            is_valid, retailer_name, error = validation_result.as_tuple()
            if not is_valid:
                return {
                    'available': False,
                    'title': None,
                    'price': None,
                    'currency': 'GBP',
                    'stock_status': 'Unknown',
                    'retailer': None,
                    'error': error
                }
            
            # Get retailer configuration
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            
            retailer_config = None
            for supported_domain, config in self.SUPPORTED_RETAILERS.items():
                if domain == supported_domain or domain.endswith('.' + supported_domain):
                    retailer_config = config
                    break
            
            if not retailer_config:
                return {
                    'available': False,
                    'title': None,
                    'price': None,
                    'currency': 'GBP',
                    'stock_status': 'Unknown',
                    'retailer': retailer_name,
                    'error': 'Retailer configuration not found'
                }
            
            # Make request to check availability with retry logic
            session = requests.Session()
            session.headers.update(self.headers)
            
            max_retries = 2
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    start_time = time.time()
                    response = session.get(url, timeout=timeout, allow_redirects=True)
                    response_time = time.time() - start_time
                    response.raise_for_status()
                    
                    # Success - break out of retry loop
                    break
                    
                except requests.exceptions.HTTPError as e:
                    last_error = e
                    if e.response and e.response.status_code in [429, 503, 502]:
                        # Rate limited or server error - retry with delay
                        if attempt < max_retries:
                            wait_time = (attempt + 1) * 2  # 2s, 4s delays
                            logger.warning(f"HTTP {e.response.status_code} for {url}, retrying in {wait_time}s")
                            time.sleep(wait_time)
                            continue
                    # Other HTTP errors or max retries reached
                    raise e
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    last_error = e
                    if attempt < max_retries:
                        wait_time = (attempt + 1) * 1  # 1s, 2s delays
                        logger.warning(f"Request failed for {url}, retrying in {wait_time}s: {str(e)}")
                        time.sleep(wait_time)
                        continue
                    # Max retries reached
                    raise e
            
            # Parse the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product information
            result = {
                'available': True,
                'title': self._extract_title(soup, retailer_config),
                'price': self._extract_price(soup, retailer_config),
                'currency': 'GBP',
                'stock_status': self._extract_stock_status(soup, retailer_config),
                'retailer': retailer_name,
                'error': None,
                'response_time': response_time
            }
            
            # Validate that we found at least a title
            if not result['title']:
                result['available'] = False
                result['error'] = 'Could not extract product title - page may not be a valid product page'
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                'available': False,
                'title': None,
                'price': None,
                'currency': 'GBP',
                'stock_status': 'Unknown',
                'retailer': retailer_name,
                'error': 'Request timeout - site may be slow or unreachable'
            }
        except requests.exceptions.ConnectionError:
            return {
                'available': False,
                'title': None,
                'price': None,
                'currency': 'GBP',
                'stock_status': 'Unknown',
                'retailer': retailer_name,
                'error': 'Connection error - unable to reach the website'
            }
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors with proper status code extraction
            if e.response is not None:
                status_code = e.response.status_code
                error_messages = {
                    404: 'Product not found (404) - URL may be invalid or product removed',
                    403: 'Access forbidden (403) - site may be blocking automated access',
                    429: 'Too many requests (429) - rate limited by website',
                    500: 'Server error (500) - website experiencing issues',
                    502: 'Bad gateway (502) - website server error',
                    503: 'Service unavailable (503) - website temporarily down',
                    504: 'Gateway timeout (504) - website server timeout',
                }
                error_msg = error_messages.get(status_code, f'HTTP error {status_code}')
            else:
                # No response object available
                error_msg = f'HTTP error: {str(e)}'
            
            return {
                'available': False,
                'title': None,
                'price': None,
                'currency': 'GBP',
                'stock_status': 'Unknown',
                'retailer': retailer_name,
                'error': error_msg
            }
        except Exception as e:
            logger.error(f"Product availability check error for {url}: {e}")
            return {
                'available': False,
                'title': None,
                'price': None,
                'currency': 'GBP',
                'stock_status': 'Unknown',
                'retailer': retailer_name,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _extract_title(self, soup, retailer_config):
        """Extract product title from page"""
        try:
            title_selector = retailer_config.get('title_selector')
            if title_selector:
                title_elem = soup.select_one(title_selector)
                if title_elem:
                    return title_elem.get_text(strip=True)
            
            # Fallback selectors
            fallback_selectors = ['h1', 'title', '.product-title', '.product-name']
            for selector in fallback_selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    if text and len(text) > 5:  # Reasonable title length
                        return text
            
            return None
        except Exception as e:
            logger.error(f"Title extraction error: {e}")
            return None
    
    def _extract_price(self, soup, retailer_config):
        """Extract product price from page"""
        try:
            price_selector = retailer_config.get('price_selector')
            if price_selector:
                price_elem = soup.select_one(price_selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    return self._parse_price(price_text)
            
            # Fallback price selectors
            fallback_selectors = ['.price', '.current-price', '.product-price', '[data-price]']
            for selector in fallback_selectors:
                elem = soup.select_one(selector)
                if elem:
                    price_text = elem.get_text(strip=True)
                    price = self._parse_price(price_text)
                    if price:
                        return price
            
            return None
        except Exception as e:
            logger.error(f"Price extraction error: {e}")
            return None
    
    def _extract_stock_status(self, soup, retailer_config):
        """Extract stock status from page"""
        try:
            stock_selector = retailer_config.get('availability_selector')
            if stock_selector:
                stock_elem = soup.select_one(stock_selector)
                if stock_elem:
                    return stock_elem.get_text(strip=True)
            
            return 'Unknown'
        except Exception as e:
            logger.error(f"Stock status extraction error: {e}")
            return 'Unknown'
    
    def _parse_price(self, price_text):
        """Parse price from text"""
        try:
            if not price_text:
                return None
            
            # Remove currency symbols and extra text
            cleaned = re.sub(r'[£$€,\s]', '', price_text)
            
            # Find decimal number
            price_match = re.search(r'\d+\.?\d*', cleaned)
            if price_match:
                return Decimal(price_match.group())
            
            return None
        except Exception as e:
            logger.error(f"Price parsing error: {e}")
            return None
    
    def get_tracking_effectiveness(self, url: str) -> dict:
        """
        Assess how effectively we can track a URL
        
        Returns:
            {
                'score': int (0-100),
                'factors': List[str], 
                'recommendations': List[str],
                'can_track': bool
            }
        """
        result = {
            'score': 0,
            'factors': [],
            'recommendations': [],
            'can_track': False
        }
        
        try:
            # URL validation (20 points)
            validation_result = self.validate_url(url)
            is_valid, retailer_name, validation_msg = validation_result.as_tuple()
            if is_valid:
                result['score'] += 20
                result['factors'].append(f"✅ Supported retailer: {retailer_name}")
                result['can_track'] = True
            else:
                result['factors'].append("❌ Unsupported retailer")
                result['recommendations'].append("Use a supported retailer URL")
                return result
            
            # Availability check (30 points)
            availability = self.check_product_availability(url)
            if availability['available']:
                result['score'] += 30
                result['factors'].append("✅ Product page accessible")
                
                # Response time factor (15 points)
                if availability.get('response_time', 0) < 3.0:
                    result['score'] += 15
                    result['factors'].append("✅ Fast response time")
                else:
                    result['factors'].append("⚠️ Slow response time")
                    result['recommendations'].append("Page loads slowly - may affect tracking frequency")
                
                # Price extraction (20 points)
                if availability.get('price'):
                    result['score'] += 20
                    result['factors'].append("✅ Price successfully extracted")
                else:
                    result['factors'].append("⚠️ Price extraction uncertain")
                    result['recommendations'].append("Price tracking may be limited")
                
                # Title extraction (10 points)
                if availability.get('title'):
                    result['score'] += 10
                    result['factors'].append("✅ Product title extracted")
                else:
                    result['factors'].append("⚠️ Product title not found")
                
                # URL structure analysis (5 points)
                if any(indicator in url.lower() for indicator in ['/dp/', '/product/', '/p/', 'product-']):
                    result['score'] += 5
                    result['factors'].append("✅ Valid product URL structure")
                else:
                    result['factors'].append("⚠️ Uncertain URL structure")
                    result['recommendations'].append("Ensure URL points to a specific product page")
                    
            else:
                result['can_track'] = False
                error_msg = availability.get('error', 'Unknown error')
                result['factors'].append(f"❌ Product not accessible: {error_msg}")
                
                # Add specific recommendations based on error type
                if 'timeout' in error_msg.lower():
                    result['recommendations'].append("❌ Poor tracking potential")
                    result['recommendations'].append("Website is too slow for reliable tracking")
                elif 'connection error' in error_msg.lower():
                    result['recommendations'].append("❌ Poor tracking potential") 
                    result['recommendations'].append("Check if the website is accessible from your network")
                elif '403' in error_msg or 'forbidden' in error_msg.lower():
                    result['recommendations'].append("❌ Poor tracking potential")
                    result['recommendations'].append("Website blocks automated access - tracking not possible")
                elif '404' in error_msg or 'not found' in error_msg.lower():
                    result['recommendations'].append("❌ Poor tracking potential")
                    result['recommendations'].append("Product page not found - check if URL is correct")
                elif '429' in error_msg or 'rate limit' in error_msg.lower():
                    result['recommendations'].append("❌ Poor tracking potential") 
                    result['recommendations'].append("Website rate limiting detected - try again later")
                else:
                    result['recommendations'].append("❌ Poor tracking potential")
                    result['recommendations'].append("Check if the product URL is correct and accessible")
                result['recommendations'].append("Check if the product URL is correct and accessible")
        
        except Exception as e:
            logger.error(f"Tracking effectiveness check error: {e}")
            result['factors'].append(f"❌ Error during analysis: {str(e)}")
        
        # Add general recommendations based on score
        if result['score'] >= 80:
            result['recommendations'].insert(0, "✅ Excellent tracking potential!")
        elif result['score'] >= 60:
            result['recommendations'].insert(0, "✅ Good tracking potential")
        elif result['score'] >= 40:
            result['recommendations'].insert(0, "⚠️ Limited tracking potential")
        else:
            result['recommendations'].insert(0, "❌ Poor tracking potential")
        
        return result

    def create_alert_for_url(self, user, url: str, alert_data: dict) -> tuple:
        """
        Create a price alert for an external URL with comprehensive error handling
        
        Args:
            user: User creating the alert
            url: Product URL to track
            alert_data: Alert configuration
        
        Returns:
            (success: bool, message: str, alert_object: PriceAlert or None)
        """
        from django.utils import timezone
        from django.core.exceptions import ValidationError
        
        try:
            from .models import PriceAlert
            
            # Validate URL
            validation_result = self.validate_url(url)
            is_valid, retailer_name, validation_message = validation_result.as_tuple()
            if not is_valid:
                return False, validation_message, None
            
            # Check product availability
            availability = self.check_product_availability(url)
            if not availability['available']:
                error_msg = f"Product not trackable: {availability.get('error', 'Unknown error')}"
                return False, error_msg, None
            
            # Create alert
            alert = PriceAlert(
                user=user,
                product_url=url,
                alert_type=alert_data.get('alert_type', 'below'),
                target_price=alert_data.get('target_price'),
                percentage_threshold=alert_data.get('percentage_threshold'),
                email_enabled=alert_data.get('email_enabled', True),
                sms_enabled=alert_data.get('sms_enabled', False),
                push_enabled=alert_data.get('push_enabled', True),
                status='active'
            )
            
            # Set onset price if we extracted it
            if availability.get('price'):
                try:
                    price_str = re.sub(r'[£$,]', '', availability['price'])
                    alert.onset_price = Decimal(price_str)
                    alert.current_price = Decimal(price_str)
                    alert.last_price_update = timezone.now()
                except (ValueError, TypeError):
                    pass  # Continue without price if extraction fails
            
            alert.full_clean()  # Validate model
            alert.save()
            
            success_msg = f"Alert created successfully for {retailer_name}! "
            if availability.get('title'):
                success_msg += f"Product: {availability['title'][:50]}..."
            
            return True, success_msg, alert
            
        except ValidationError as e:
            return False, f"Validation error: {e}", None
        except Exception as e:
            logger.error(f"Alert creation error: {e}")
            return False, f"Failed to create alert: {str(e)}", None
        
    def get_tracking_effectiveness_score(self, url):
        """
        Get a simple effectiveness score for admin display
        
        Returns:
            (score: int, error: str or None)
        """
        try:
            effectiveness = self.get_tracking_effectiveness(url)
            return effectiveness['score'], None
        except Exception as e:
            logger.error(f"Error getting tracking effectiveness score: {e}")
            return 0, str(e)
    
    def get_url_tracking_info(self, url: str) -> dict:
        """
        Get comprehensive URL tracking information for admin display
        
        Returns:
            {
                'effectiveness': dict,
                'availability': dict,
                'validation': dict
            }
        """
        try:
            result = {
                'effectiveness': self.get_tracking_effectiveness(url),
                'availability': self.check_product_availability(url),
                'validation': {}
            }
            
            validation_result = self.validate_url(url)
            is_valid, retailer, message = validation_result.as_tuple()
            result['validation'] = {
                'is_valid': is_valid,
                'message': message,
                'retailer': retailer
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting URL tracking info: {e}")
            return {
                'error': str(e),
                'effectiveness': {'score': 0, 'factors': [], 'recommendations': []},
                'availability': {'available': False, 'error': str(e)},
                'validation': {'is_valid': False, 'message': str(e), 'retailer': None}
            }
# Global instance
url_tracking_service = URLTrackingService()
