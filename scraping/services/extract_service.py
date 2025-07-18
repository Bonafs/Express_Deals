"""
Express Deals - Extract Service  
ML-powered intelligent parsing with self-healing selectors
"""

import re
import joblib
import pandas as pd
import difflib
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
from django.core.cache import cache
from django.conf import settings
import numpy as np

logger = logging.getLogger(__name__)


@dataclass 
class ExtractionResult:
    """Result of data extraction"""
    success: bool
    data: Dict = None
    confidence: float = 0.0
    method_used: str = ""
    fallback_used: bool = False
    error: Optional[str] = None


@dataclass
class ElementFeatures:
    """Features for ML element detection"""
    tag_name: str
    class_names: List[str]
    id_value: str
    text_length: int
    has_price_pattern: bool
    position_in_dom: int
    parent_tag: str
    sibling_count: int


class SelfHealingExtractor:
    """ML-powered extractor that adapts to layout changes"""
    
    def __init__(self):
        self.model = self._load_or_train_model()
        self.selector_cache = {}
        self.diff_threshold = 0.15
        self.confidence_threshold = 0.7
        self.price_patterns = self._compile_price_patterns()
        
    def _compile_price_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for price detection"""
        return [
            re.compile(r'£\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
            re.compile(r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*£', re.IGNORECASE),
            re.compile(r'GBP\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
            re.compile(r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*GBP', re.IGNORECASE),
            re.compile(r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE),
        ]
    
    def extract_product_data(self, html: str, site_id: str, url: str) -> ExtractionResult:
        """Extract using ML-predicted selectors with fallbacks"""
        
        try:
            # 1. Check for significant layout changes
            if self._layout_changed_significantly(html, site_id):
                logger.warning(f"Layout change detected for {site_id}")
                self._trigger_layout_alert(site_id)
                return self._fallback_extraction(html, url)
            
            # 2. Try cached selectors first
            cached_result = self._try_cached_selectors(html, site_id)
            if cached_result and cached_result.confidence > self.confidence_threshold:
                return cached_result
            
            # 3. ML-powered element detection
            ml_result = self._ml_powered_extraction(html, site_id)
            if ml_result and ml_result.confidence > self.confidence_threshold:
                # Cache successful selectors
                self._cache_successful_selectors(site_id, ml_result)
                return ml_result
            
            # 4. Fallback to rule-based extraction
            return self._fallback_extraction(html, url)
            
        except Exception as e:
            logger.error(f"Extraction failed for {site_id}: {e}")
            return ExtractionResult(
                success=False,
                error=str(e)
            )
    
    def _layout_changed_significantly(self, html: str, site_id: str) -> bool:
        """Detect layout changes using HTML diff analysis"""
        
        cached_html = cache.get(f'html_structure_{site_id}')
        if not cached_html:
            # First time seeing this site - cache structure
            self._cache_html_structure(html, site_id)
            return False
        
        # Extract structural elements for comparison
        current_structure = self._extract_html_structure(html)
        cached_structure = self._extract_html_structure(cached_html)
        
        # Calculate structural similarity
        similarity = difflib.SequenceMatcher(None, cached_structure, current_structure).ratio()
        
        if similarity < (1 - self.diff_threshold):
            # Significant change detected - update cache
            self._cache_html_structure(html, site_id)
            return True
        
        return False
    
    def _extract_html_structure(self, html: str) -> str:
        """Extract structural signature of HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Focus on key structural elements
        structure_elements = []
        for tag in soup.find_all(['div', 'section', 'article', 'main']):
            if tag.get('class') or tag.get('id'):
                structure_elements.append(f"{tag.name}:{tag.get('class', [])}:{tag.get('id', '')}")
        
        return '|'.join(structure_elements[:50])  # Limit to prevent memory issues
    
    def _cache_html_structure(self, html: str, site_id: str):
        """Cache HTML structure for diff detection"""
        cache.set(f'html_structure_{site_id}', html[:10000], timeout=86400)  # 24 hours
    
    def _try_cached_selectors(self, html: str, site_id: str) -> Optional[ExtractionResult]:
        """Try previously successful selectors"""
        cached_selectors = cache.get(f'selectors_{site_id}')
        if not cached_selectors:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        confidence_scores = []
        
        try:
            # Try cached price selector
            if 'price' in cached_selectors:
                price_elem = soup.select_one(cached_selectors['price'])
                if price_elem:
                    data['price'] = self._extract_price_from_element(price_elem)
                    confidence_scores.append(0.9)
                else:
                    confidence_scores.append(0.0)
            
            # Try cached title selector
            if 'title' in cached_selectors:
                title_elem = soup.select_one(cached_selectors['title'])
                if title_elem:
                    data['title'] = title_elem.get_text(strip=True)
                    confidence_scores.append(0.8)
                else:
                    confidence_scores.append(0.0)
            
            # Try cached image selector
            if 'image' in cached_selectors:
                img_elem = soup.select_one(cached_selectors['image'])
                if img_elem:
                    data['image'] = img_elem.get('src') or img_elem.get('data-src')
                    confidence_scores.append(0.7)
                else:
                    confidence_scores.append(0.0)
            
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.0
            
            if data and avg_confidence > 0.5:
                return ExtractionResult(
                    success=True,
                    data=data,
                    confidence=avg_confidence,
                    method_used='cached_selectors',
                    fallback_used=False
                )
                
        except Exception as e:
            logger.debug(f"Cached selectors failed: {e}")
        
        return None
    
    def _ml_powered_extraction(self, html: str, site_id: str) -> Optional[ExtractionResult]:
        """Use ML model to predict element locations"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract features for all potential elements
        candidates = self._find_element_candidates(soup)
        
        if not candidates:
            return None
        
        # Prepare features for ML model
        features_matrix = []
        for elem, features in candidates:
            feature_vector = self._element_to_feature_vector(features)
            features_matrix.append(feature_vector)
        
        # Predict probabilities
        if len(features_matrix) == 0:
            return None
        
        try:
            probabilities = self.model.predict_proba(features_matrix)
            
            # Find best candidates for each data type
            data = {}
            confidence_scores = []
            
            # Extract price (class 0)
            price_probs = probabilities[:, 0] if probabilities.shape[1] > 0 else []
            if len(price_probs) > 0:
                best_price_idx = np.argmax(price_probs)
                if price_probs[best_price_idx] > 0.6:
                    price_elem = candidates[best_price_idx][0]
                    data['price'] = self._extract_price_from_element(price_elem)
                    confidence_scores.append(price_probs[best_price_idx])
            
            # Extract title (class 1)
            title_probs = probabilities[:, 1] if probabilities.shape[1] > 1 else []
            if len(title_probs) > 0:
                best_title_idx = np.argmax(title_probs)
                if title_probs[best_title_idx] > 0.6:
                    title_elem = candidates[best_title_idx][0]
                    data['title'] = title_elem.get_text(strip=True)
                    confidence_scores.append(title_probs[best_title_idx])
            
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.0
            
            if data and avg_confidence > 0.5:
                return ExtractionResult(
                    success=True,
                    data=data,
                    confidence=avg_confidence,
                    method_used='ml_prediction',
                    fallback_used=False
                )
                
        except Exception as e:
            logger.debug(f"ML extraction failed: {e}")
        
        return None
    
    def _find_element_candidates(self, soup: BeautifulSoup) -> List[Tuple]:
        """Find potential product data elements"""
        candidates = []
        
        # Look for elements that might contain product data
        for elem in soup.find_all(['span', 'div', 'h1', 'h2', 'h3', 'p', 'strong']):
            text = elem.get_text(strip=True)
            
            # Skip empty or very short elements
            if len(text) < 2:
                continue
            
            # Extract features
            features = ElementFeatures(
                tag_name=elem.name,
                class_names=elem.get('class', []),
                id_value=elem.get('id', ''),
                text_length=len(text),
                has_price_pattern=any(pattern.search(text) for pattern in self.price_patterns),
                position_in_dom=len(list(elem.parents)),
                parent_tag=elem.parent.name if elem.parent else '',
                sibling_count=len(elem.find_siblings())
            )
            
            candidates.append((elem, features))
        
        return candidates[:100]  # Limit to prevent performance issues
    
    def _element_to_feature_vector(self, features: ElementFeatures) -> List[float]:
        """Convert element features to ML feature vector"""
        return [
            1.0 if features.tag_name == 'span' else 0.0,
            1.0 if features.tag_name in ['h1', 'h2', 'h3'] else 0.0,
            1.0 if any('price' in cls.lower() for cls in features.class_names) else 0.0,
            1.0 if any('title' in cls.lower() for cls in features.class_names) else 0.0,
            1.0 if 'price' in features.id_value.lower() else 0.0,
            min(features.text_length / 100.0, 1.0),  # Normalized text length
            1.0 if features.has_price_pattern else 0.0,
            min(features.position_in_dom / 20.0, 1.0),  # Normalized DOM depth
            min(features.sibling_count / 10.0, 1.0),  # Normalized sibling count
        ]
    
    def _extract_price_from_element(self, elem) -> Optional[float]:
        """Extract price value from element"""
        text = elem.get_text(strip=True)
        
        for pattern in self.price_patterns:
            match = pattern.search(text)
            if match:
                try:
                    price_str = match.group(1).replace(',', '')
                    return float(price_str)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _fallback_extraction(self, html: str, url: str) -> ExtractionResult:
        """Fallback rule-based extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        
        # Common price selectors
        price_selectors = [
            '[data-testid*="price"]',
            '.price',
            '.product-price',
            '[class*="price"]',
            '[id*="price"]'
        ]
        
        for selector in price_selectors:
            elem = soup.select_one(selector)
            if elem:
                price = self._extract_price_from_element(elem)
                if price:
                    data['price'] = price
                    break
        
        # Common title selectors
        title_selectors = [
            'h1',
            '.product-title',
            '[data-testid*="title"]',
            '.title'
        ]
        
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if len(title) > 5:
                    data['title'] = title
                    break
        
        success = len(data) > 0
        
        return ExtractionResult(
            success=success,
            data=data,
            confidence=0.5 if success else 0.0,
            method_used='fallback_rules',
            fallback_used=True
        )
    
    def _cache_successful_selectors(self, site_id: str, result: ExtractionResult):
        """Cache successful selectors for reuse"""
        if result.success and not result.fallback_used:
            # This would need to be implemented based on how selectors are determined
            # For now, we'll cache the fact that ML worked
            cache.set(f'ml_success_{site_id}', True, timeout=3600)
    
    def _trigger_layout_alert(self, site_id: str):
        """Trigger alert for layout changes"""
        logger.warning(f"Layout change detected for {site_id} - may need selector updates")
        # Could send Slack/email alert here
    
    def _load_or_train_model(self) -> RandomForestClassifier:
        """Load existing model or train a new one"""
        try:
            # Try to load existing model
            model = joblib.load('ml_extraction_model.pkl')
            logger.info("Loaded existing ML extraction model")
            return model
        except FileNotFoundError:
            # Train new model with basic data
            logger.info("Training new ML extraction model")
            return self._train_basic_model()
    
    def _train_basic_model(self) -> RandomForestClassifier:
        """Train basic model with synthetic data"""
        # Generate synthetic training data
        X = []
        y = []
        
        # Price element features (class 0)
        for _ in range(100):
            X.append([
                0.8,  # is_span
                0.0,  # is_heading
                0.9,  # has_price_class
                0.0,  # has_title_class
                0.8,  # has_price_id
                0.3,  # text_length (normalized)
                1.0,  # has_price_pattern
                0.5,  # dom_depth
                0.3   # sibling_count
            ])
            y.append(0)  # Price class
        
        # Title element features (class 1)
        for _ in range(100):
            X.append([
                0.2,  # is_span
                0.9,  # is_heading
                0.0,  # has_price_class
                0.8,  # has_title_class
                0.0,  # has_price_id
                0.8,  # text_length
                0.0,  # has_price_pattern
                0.3,  # dom_depth
                0.5   # sibling_count
            ])
            y.append(1)  # Title class
        
        # Noise/other elements (class 2)
        for _ in range(100):
            X.append([
                np.random.random(),  # Random features
                np.random.random(),
                np.random.random(),
                np.random.random(),
                np.random.random(),
                np.random.random(),
                0.0,  # No price pattern
                np.random.random(),
                np.random.random()
            ])
            y.append(2)  # Other class
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, 'ml_extraction_model.pkl')
        
        return model


# Global extractor instance
extractor = SelfHealingExtractor()
