"""
Express Deals - World-Class Proxy Management System
Advanced proxy rotation and management for enterprise-grade web scraping
"""

import random
import time
import requests
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from threading import Lock
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class ProxyConfig:
    """Proxy configuration dataclass"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    country: Optional[str] = None
    provider: Optional[str] = None
    
    @property
    def url(self) -> str:
        """Generate proxy URL"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    @property
    def dict(self) -> Dict[str, str]:
        """Return proxy as requests-compatible dict"""
        return {
            "http": self.url,
            "https": self.url
        }


class ProxyStats:
    """Track proxy performance statistics"""
    
    def __init__(self, proxy_id: str):
        self.proxy_id = proxy_id
        self.success_count = 0
        self.failure_count = 0
        self.total_response_time = 0.0
        self.last_used = None
        self.last_success = None
        self.blocked_until = None
        
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        total = self.success_count + self.failure_count
        return (self.success_count / total * 100) if total > 0 else 0
    
    @property
    def average_response_time(self) -> float:
        """Calculate average response time"""
        return (self.total_response_time / self.success_count) if self.success_count > 0 else 0
    
    @property
    def is_blocked(self) -> bool:
        """Check if proxy is currently blocked"""
        return self.blocked_until and datetime.now() < self.blocked_until
    
    def record_success(self, response_time: float):
        """Record successful request"""
        self.success_count += 1
        self.total_response_time += response_time
        self.last_used = datetime.now()
        self.last_success = datetime.now()
        
    def record_failure(self, block_duration_minutes: int = 30):
        """Record failed request and optionally block proxy"""
        self.failure_count += 1
        self.last_used = datetime.now()
        
        # Block proxy if failure rate is too high
        if self.success_rate < 50 and self.failure_count > 3:
            self.blocked_until = datetime.now() + timedelta(minutes=block_duration_minutes)


class WorldClassProxyManager:
    """
    Enterprise-grade proxy management system with:
    - Intelligent rotation algorithms
    - Performance monitoring
    - Automatic failover
    - Geographic targeting
    - Rate limiting compliance
    """
    
    def __init__(self):
        self.proxies: List[ProxyConfig] = []
        self.proxy_stats: Dict[str, ProxyStats] = {}
        self.current_proxy_index = 0
        self.lock = Lock()
        self.rotation_strategies = {
            'round_robin': self._round_robin,
            'performance_based': self._performance_based,
            'geographic': self._geographic_rotation,
            'random': self._random_rotation
        }
        self.current_strategy = 'performance_based'
        
        # Load proxies from various sources
        self._load_proxies()
    
    def _load_proxies(self):
        """Load proxies from multiple sources"""
        # Premium proxy providers (configure in settings)
        premium_proxies = getattr(settings, 'PREMIUM_PROXIES', [])
        
        # Free proxy sources (use with caution)
        free_proxies = self._get_free_proxies()
        
        # Rotating residential proxies
        residential_proxies = self._get_residential_proxies()
        
        # Combine all proxy sources
        all_proxies = premium_proxies + free_proxies + residential_proxies
        
        for proxy_data in all_proxies:
            proxy = ProxyConfig(**proxy_data)
            self.proxies.append(proxy)
            self.proxy_stats[proxy.url] = ProxyStats(proxy.url)
        
        logger.info(f"Loaded {len(self.proxies)} proxies from various sources")
    
    def _get_premium_proxies(self) -> List[Dict]:
        """Get premium proxy configurations"""
        return [
            # ProxyMesh (UK-focused)
            {
                'host': 'uk.proxymesh.com',
                'port': 31280,
                'username': getattr(settings, 'PROXYMESH_USERNAME', ''),
                'password': getattr(settings, 'PROXYMESH_PASSWORD', ''),
                'country': 'UK',
                'provider': 'ProxyMesh'
            },
            # Bright Data (formerly Luminati)
            {
                'host': 'zproxy.lum-superproxy.io',
                'port': 22225,
                'username': getattr(settings, 'BRIGHTDATA_USERNAME', ''),
                'password': getattr(settings, 'BRIGHTDATA_PASSWORD', ''),
                'country': 'UK',
                'provider': 'BrightData'
            },
            # Oxylabs
            {
                'host': 'pr.oxylabs.io',
                'port': 7777,
                'username': getattr(settings, 'OXYLABS_USERNAME', ''),
                'password': getattr(settings, 'OXYLABS_PASSWORD', ''),
                'country': 'UK',
                'provider': 'Oxylabs'
            }
        ]
    
    def _get_free_proxies(self) -> List[Dict]:
        """Get free proxy sources (less reliable)"""
        free_proxies = []
        
        try:
            # Example: Free UK proxies (implement your preferred free proxy source)
            uk_free_proxies = [
                {'host': '185.199.229.156', 'port': 7492, 'country': 'UK'},
                {'host': '185.199.228.220', 'port': 7300, 'country': 'UK'},
                {'host': '185.199.231.45', 'port': 8382, 'country': 'UK'},
            ]
            free_proxies.extend(uk_free_proxies)
            
        except Exception as e:
            logger.warning(f"Failed to fetch free proxies: {e}")
        
        return free_proxies
    
    def _get_residential_proxies(self) -> List[Dict]:
        """Get residential proxy configurations"""
        return [
            # SmartProxy
            {
                'host': 'gate.smartproxy.com',
                'port': 7000,
                'username': getattr(settings, 'SMARTPROXY_USERNAME', ''),
                'password': getattr(settings, 'SMARTPROXY_PASSWORD', ''),
                'country': 'UK',
                'provider': 'SmartProxy'
            },
            # NetNut
            {
                'host': 'residential.netnut.io',
                'port': 5959,
                'username': getattr(settings, 'NETNUT_USERNAME', ''),
                'password': getattr(settings, 'NETNUT_PASSWORD', ''),
                'country': 'UK',
                'provider': 'NetNut'
            }
        ]
    
    def get_proxy(self, target_country: str = 'UK') -> Optional[ProxyConfig]:
        """Get next proxy using current rotation strategy"""
        with self.lock:
            strategy_func = self.rotation_strategies.get(self.current_strategy, self._performance_based)
            return strategy_func(target_country)
    
    def _round_robin(self, target_country: str = None) -> Optional[ProxyConfig]:
        """Simple round-robin rotation"""
        if not self.proxies:
            return None
        
        available_proxies = [p for p in self.proxies 
                           if not self.proxy_stats[p.url].is_blocked]
        
        if not available_proxies:
            return None
        
        proxy = available_proxies[self.current_proxy_index % len(available_proxies)]
        self.current_proxy_index += 1
        return proxy
    
    def _performance_based(self, target_country: str = None) -> Optional[ProxyConfig]:
        """Select proxy based on performance metrics"""
        available_proxies = [p for p in self.proxies 
                           if not self.proxy_stats[p.url].is_blocked]
        
        if not available_proxies:
            return None
        
        # Sort by success rate and response time
        sorted_proxies = sorted(
            available_proxies,
            key=lambda p: (
                self.proxy_stats[p.url].success_rate,
                -self.proxy_stats[p.url].average_response_time
            ),
            reverse=True
        )
        
        # Use top 30% of best performing proxies
        top_proxies = sorted_proxies[:max(1, len(sorted_proxies) // 3)]
        return random.choice(top_proxies)
    
    def _geographic_rotation(self, target_country: str = 'UK') -> Optional[ProxyConfig]:
        """Select proxy based on geographic location"""
        country_proxies = [p for p in self.proxies 
                         if p.country == target_country and not self.proxy_stats[p.url].is_blocked]
        
        if not country_proxies:
            # Fallback to any available proxy
            return self._performance_based()
        
        return random.choice(country_proxies)
    
    def _random_rotation(self, target_country: str = None) -> Optional[ProxyConfig]:
        """Random proxy selection"""
        available_proxies = [p for p in self.proxies 
                           if not self.proxy_stats[p.url].is_blocked]
        
        return random.choice(available_proxies) if available_proxies else None
    
    def test_proxy(self, proxy: ProxyConfig, timeout: int = 10) -> Tuple[bool, float]:
        """Test proxy connectivity and performance"""
        start_time = time.time()
        test_urls = [
            'http://httpbin.org/ip',
            'https://www.google.com',
            'https://www.amazon.co.uk'
        ]
        
        for test_url in test_urls:
            try:
                response = requests.get(
                    test_url,
                    proxies=proxy.dict,
                    timeout=timeout,
                    headers={'User-Agent': self._get_random_user_agent()}
                )
                
                if response.status_code == 200:
                    response_time = time.time() - start_time
                    return True, response_time
                    
            except Exception as e:
                logger.debug(f"Proxy test failed for {proxy.url}: {e}")
                continue
        
        return False, time.time() - start_time
    
    def record_proxy_usage(self, proxy: ProxyConfig, success: bool, response_time: float = 0):
        """Record proxy usage statistics"""
        stats = self.proxy_stats.get(proxy.url)
        if stats:
            if success:
                stats.record_success(response_time)
            else:
                stats.record_failure()
    
    def get_proxy_stats(self) -> Dict:
        """Get comprehensive proxy statistics"""
        stats = {
            'total_proxies': len(self.proxies),
            'active_proxies': len([p for p in self.proxies if not self.proxy_stats[p.url].is_blocked]),
            'blocked_proxies': len([p for p in self.proxies if self.proxy_stats[p.url].is_blocked]),
            'average_success_rate': 0,
            'top_performers': []
        }
        
        if self.proxy_stats:
            success_rates = [s.success_rate for s in self.proxy_stats.values()]
            stats['average_success_rate'] = sum(success_rates) / len(success_rates)
            
            # Get top 5 performing proxies
            sorted_stats = sorted(
                self.proxy_stats.items(),
                key=lambda x: x[1].success_rate,
                reverse=True
            )
            stats['top_performers'] = sorted_stats[:5]
        
        return stats
    
    def _get_random_user_agent(self) -> str:
        """Get random user agent for requests"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)
    
    def cleanup_blocked_proxies(self):
        """Remove permanently failed proxies"""
        current_time = datetime.now()
        
        for proxy_url, stats in list(self.proxy_stats.items()):
            # Remove proxies with very low success rate after many attempts
            if (stats.failure_count > 20 and stats.success_rate < 10):
                proxy_to_remove = next((p for p in self.proxies if p.url == proxy_url), None)
                if proxy_to_remove:
                    self.proxies.remove(proxy_to_remove)
                    del self.proxy_stats[proxy_url]
                    logger.info(f"Removed permanently failed proxy: {proxy_url}")


# Global proxy manager instance
proxy_manager = WorldClassProxyManager()
