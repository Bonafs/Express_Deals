"""
Express Deals - URL Tracking Service
Comprehensive service for checking product availability and tracking effectiveness
"""

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import re

logger = logging.getLogger(__name__)


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
        }
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def validate_url(self, url):
        """
        Validate if URL is from a supported retailer
        Returns: (is_valid, retailer_name, error_message)
        """
        try:
            if not url or not isinstance(url, str):
                return False, None, "URL is required"
            
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                return False, None, "URL must start with http:// or https://"
            
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Remove www. prefix for comparison
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Check against supported retailers
            for supported_domain, retailer_info in self.SUPPORTED_RETAILERS.items():
                if domain == supported_domain or domain.endswith('.' + supported_domain):
                    return True, retailer_info['name'], None
            
            # Not a supported retailer
            supported_sites = list(self.SUPPORTED_RETAILERS.keys())
            return False, None, f"URL must be from a supported retailer: {', '.join(supported_sites)}"
            
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False, None, f"Invalid URL format: {str(e)}"
    
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
            is_valid, retailer_name, error = self.validate_url(url)
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
            
            # Make request to check availability
            session = requests.Session()
            session.headers.update(self.headers)
            
            response = session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
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
                'error': None
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
            status_code = e.response.status_code if e.response else 'Unknown'
            error_messages = {
                404: 'Product not found (404) - URL may be invalid or product removed',
                403: 'Access forbidden (403) - site may be blocking automated access',
                429: 'Too many requests (429) - rate limited by website',
                500: 'Server error (500) - website experiencing issues',
            }
            error_msg = error_messages.get(status_code, f'HTTP error {status_code}')
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
    
    def get_tracking_effectiveness_score(self, url):
        """
        Calculate tracking effectiveness score (0-100)
        Based on supported features and reliability
        """
        try:
            is_valid, retailer_name, error = self.validate_url(url)
            if not is_valid:
                return 0, error
            
            # Base score for supported retailer
            score = 60
            
            # Check if we can extract product data
            availability = self.check_product_availability(url)
            
            if availability['available']:
                score += 20  # Site is accessible
                
                if availability['title']:
                    score += 10  # Can extract title
                
                if availability['price']:
                    score += 10  # Can extract price
            
            return min(score, 100), None
            
        except Exception as e:
            logger.error(f"Tracking effectiveness error: {e}")
            return 0, str(e)
    
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
            is_valid, retailer_name, validation_msg = self.validate_url(url)
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
                result['factors'].append(f"❌ Product not accessible: {availability.get('error', 'Unknown error')}")
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
        try:
            from .models import PriceAlert
            
            # Validate URL
            is_valid, retailer_name, validation_message = self.validate_url(url)
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
            
            is_valid, retailer, message = self.validate_url(url)
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
