"""
Express Deals - Transform Service
Advanced data processing and validation
"""

import re
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional, Dict, List
import logging
from django.core.cache import cache
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class TransformResult:
    """Result of data transformation"""
    success: bool
    data: Dict = None
    quality_score: float = 0.0
    validation_errors: List[str] = None
    transformations_applied: List[str] = None


class CommercialDataTransformer:
    """Enterprise-grade data transformation and validation"""
    
    def __init__(self):
        self.price_patterns = self._compile_price_patterns()
        self.validation_rules = self._load_validation_rules()
        self.normalization_maps = self._load_normalization_maps()
        
    def _compile_price_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for price normalization"""
        return [
            re.compile(r'£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
            re.compile(r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*£', re.IGNORECASE),
            re.compile(r'GBP\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
            re.compile(r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
        ]
    
    def _load_validation_rules(self) -> Dict:
        """Load data validation rules"""
        return {
            'price': {
                'min_value': 0.01,
                'max_value': 50000.0,
                'required': True
            },
            'title': {
                'min_length': 3,
                'max_length': 500,
                'required': True
            },
            'category': {
                'allowed_values': [
                    'Electronics', 'Clothing', 'Home & Garden', 
                    'Books', 'Sports', 'Beauty', 'Toys', 
                    'Automotive', 'Health', 'Food'
                ],
                'required': False
            }
        }
    
    def _load_normalization_maps(self) -> Dict:
        """Load category and brand normalization mappings"""
        return {
            'categories': {
                'electronic': 'Electronics',
                'tech': 'Electronics',
                'gadget': 'Electronics',
                'clothing': 'Clothing',
                'apparel': 'Clothing',
                'fashion': 'Clothing',
                'home': 'Home & Garden',
                'garden': 'Home & Garden',
                'furniture': 'Home & Garden'
            },
            'brands': {
                'apple inc': 'Apple',
                'apple computer': 'Apple',
                'samsung electronics': 'Samsung',
                'amazon basics': 'Amazon Basics'
            }
        }
    
    def transform_product_data(self, raw_data: Dict, site_config: Dict) -> TransformResult:
        """Transform raw scraped data into normalized format"""
        
        transformed = {}
        validation_errors = []
        transformations_applied = []
        
        try:
            # 1. Price Normalization
            price_result = self._normalize_price(
                raw_data.get('price'), 
                site_config.get('currency', 'GBP')
            )
            if price_result['success']:
                transformed['price'] = price_result['value']
                transformations_applied.append('price_normalized')
            else:
                validation_errors.append(f"Price normalization failed: {price_result['error']}")
            
            # 2. Title Cleaning and Standardization
            title_result = self._clean_title(raw_data.get('title', ''))
            if title_result['success']:
                transformed['title'] = title_result['value']
                transformations_applied.append('title_cleaned')
            else:
                validation_errors.append(f"Title cleaning failed: {title_result['error']}")
            
            # 3. Category Mapping and Standardization
            category_result = self._map_category(
                raw_data.get('category', ''),
                site_config.get('category_mapping', {})
            )
            if category_result['success']:
                transformed['category'] = category_result['value']
                transformations_applied.append('category_mapped')
            
            # 4. Availability Status Processing
            availability_result = self._process_availability(
                raw_data.get('availability', ''),
                raw_data.get('stock_level', '')
            )
            transformed['availability'] = availability_result['value']
            transformations_applied.append('availability_processed')
            
            # 5. Image URL Processing
            images_result = self._process_images(
                raw_data.get('images', []),
                site_config.get('base_url', '')
            )
            transformed['images'] = images_result['value']
            transformations_applied.append('images_processed')
            
            # 6. Brand Normalization
            brand_result = self._normalize_brand(raw_data.get('brand', ''))
            if brand_result['success']:
                transformed['brand'] = brand_result['value']
                transformations_applied.append('brand_normalized')
            
            # 7. Data Quality Validation
            quality_score = self._validate_data_quality(transformed)
            
            # 8. Additional Metadata
            transformed.update({
                'scraped_at': raw_data.get('scraped_at'),
                'source_url': raw_data.get('source_url'),
                'site_id': site_config.get('site_id'),
                'quality_score': quality_score
            })
            
            success = len(validation_errors) == 0 and quality_score >= 0.6
            
            return TransformResult(
                success=success,
                data=transformed,
                quality_score=quality_score,
                validation_errors=validation_errors,
                transformations_applied=transformations_applied
            )
            
        except Exception as e:
            logger.error(f"Transform failed: {e}")
            return TransformResult(
                success=False,
                validation_errors=[str(e)]
            )
    
    def _normalize_price(self, price_text: any, currency: str) -> Dict:
        """Advanced price normalization with multiple patterns"""
        if not price_text:
            return {'success': False, 'error': 'No price data'}
        
        # Convert to string if not already
        price_str = str(price_text).strip()
        
        # Try each pattern
        for pattern in self.price_patterns:
            match = pattern.search(price_str)
            if match:
                try:
                    # Clean and convert to decimal
                    price_value = match.group(1).replace(',', '')
                    decimal_price = Decimal(price_value)
                    
                    # Validation
                    rules = self.validation_rules['price']
                    if decimal_price < rules['min_value']:
                        return {'success': False, 'error': f'Price too low: {decimal_price}'}
                    if decimal_price > rules['max_value']:
                        return {'success': False, 'error': f'Price too high: {decimal_price}'}
                    
                    return {
                        'success': True,
                        'value': float(decimal_price),
                        'currency': currency
                    }
                    
                except (ValueError, TypeError) as e:
                    continue
        
        return {'success': False, 'error': f'Could not parse price: {price_str}'}
    
    def _clean_title(self, title_text: str) -> Dict:
        """Clean and standardize product titles"""
        if not title_text:
            return {'success': False, 'error': 'No title data'}
        
        # Basic cleaning
        cleaned = title_text.strip()
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common noise patterns
        noise_patterns = [
            r'\[.*?\]',  # Remove bracketed text
            r'\(.*?\)',  # Remove parenthetical text (optional)
            r'NEW!?',    # Remove "NEW" indicators
            r'SALE!?',   # Remove "SALE" indicators
        ]
        
        for pattern in noise_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        cleaned = cleaned.strip()
        
        # Validation
        rules = self.validation_rules['title']
        if len(cleaned) < rules['min_length']:
            return {'success': False, 'error': f'Title too short: {len(cleaned)}'}
        if len(cleaned) > rules['max_length']:
            cleaned = cleaned[:rules['max_length']]
        
        return {'success': True, 'value': cleaned}
    
    def _map_category(self, category_text: str, site_mapping: Dict) -> Dict:
        """Map and standardize category"""
        if not category_text:
            return {'success': True, 'value': 'Other'}
        
        # Clean category text
        cleaned = category_text.lower().strip()
        
        # Try site-specific mapping first
        if cleaned in site_mapping:
            return {'success': True, 'value': site_mapping[cleaned]}
        
        # Try global normalization mapping
        for key, value in self.normalization_maps['categories'].items():
            if key in cleaned:
                return {'success': True, 'value': value}
        
        # Fallback to capitalized original
        return {'success': True, 'value': category_text.title()}
    
    def _process_availability(self, availability_text: str, stock_level: str) -> Dict:
        """Process availability status"""
        if not availability_text and not stock_level:
            return {'value': 'unknown'}
        
        combined_text = f"{availability_text} {stock_level}".lower()
        
        # Check for out of stock indicators
        out_of_stock_indicators = [
            'out of stock', 'unavailable', 'sold out', 
            'not available', 'discontinued'
        ]
        
        for indicator in out_of_stock_indicators:
            if indicator in combined_text:
                return {'value': 'out_of_stock'}
        
        # Check for in stock indicators
        in_stock_indicators = [
            'in stock', 'available', 'ready to ship',
            'ships today', 'immediate dispatch'
        ]
        
        for indicator in in_stock_indicators:
            if indicator in combined_text:
                return {'value': 'in_stock'}
        
        # Check for limited stock
        limited_indicators = ['limited', 'few left', 'only']
        for indicator in limited_indicators:
            if indicator in combined_text:
                return {'value': 'limited_stock'}
        
        return {'value': 'unknown'}
    
    def _process_images(self, images_data: List, base_url: str) -> Dict:
        """Process and validate image URLs"""
        if not images_data:
            return {'value': []}
        
        processed_images = []
        
        for img in images_data:
            if isinstance(img, str):
                # Clean and validate URL
                cleaned_url = self._clean_image_url(img, base_url)
                if cleaned_url:
                    processed_images.append(cleaned_url)
            elif isinstance(img, dict):
                # Handle image objects
                url = img.get('src') or img.get('url') or img.get('href')
                if url:
                    cleaned_url = self._clean_image_url(url, base_url)
                    if cleaned_url:
                        processed_images.append(cleaned_url)
        
        return {'value': processed_images}
    
    def _clean_image_url(self, url: str, base_url: str) -> Optional[str]:
        """Clean and validate image URL"""
        if not url:
            return None
        
        # Handle relative URLs
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = base_url.rstrip('/') + url
        elif not url.startswith(('http://', 'https://')):
            url = base_url.rstrip('/') + '/' + url.lstrip('/')
        
        # Basic validation
        if not re.match(r'https?://.+\.(jpg|jpeg|png|gif|webp)', url, re.IGNORECASE):
            return None
        
        return url
    
    def _normalize_brand(self, brand_text: str) -> Dict:
        """Normalize brand names"""
        if not brand_text:
            return {'success': False, 'error': 'No brand data'}
        
        cleaned = brand_text.strip()
        
        # Check normalization mapping
        cleaned_lower = cleaned.lower()
        if cleaned_lower in self.normalization_maps['brands']:
            return {
                'success': True,
                'value': self.normalization_maps['brands'][cleaned_lower]
            }
        
        return {'success': True, 'value': cleaned}
    
    def _validate_data_quality(self, data: Dict) -> float:
        """Calculate data quality score"""
        score = 0.0
        max_score = 0.0
        
        # Price validation (30% weight)
        max_score += 0.3
        if data.get('price') and data['price'] > 0:
            score += 0.3
        
        # Title validation (25% weight)
        max_score += 0.25
        title = data.get('title', '')
        if title and len(title.split()) >= 3:
            score += 0.25
        
        # Category validation (20% weight)
        max_score += 0.2
        if data.get('category') and data['category'] != 'Other':
            score += 0.2
        
        # Availability validation (15% weight)
        max_score += 0.15
        if data.get('availability') and data['availability'] != 'unknown':
            score += 0.15
        
        # Image validation (10% weight)
        max_score += 0.1
        if data.get('images') and len(data['images']) > 0:
            score += 0.1
        
        return score / max_score if max_score > 0 else 0.0


# Global transformer instance
transformer = CommercialDataTransformer()
