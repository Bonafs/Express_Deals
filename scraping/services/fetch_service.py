"""
Express Deals - Fetch Service
Advanced request management with anti-detection
"""

import asyncio
import random
import time
import aiohttp
import ssl
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
import logging
from django.conf import settings
from django.core.cache import cache
import cloudscraper
from fake_useragent import UserAgent
from ..proxy_manager import proxy_manager

logger = logging.getLogger(__name__)


@dataclass
class SiteConfig:
    """Site-specific configuration"""
    base_delay: float = 2.0
    max_delay: float = 10.0
    respect_robots: bool = True
    min_reputation: float = 0.8
    target_geo: str = 'UK'
    requires_js: bool = False
    anti_bot_level: str = 'medium'  # low, medium, high
    

@dataclass
class RequestResult:
    """Result of fetch request"""
    success: bool
    content: str = ""
    status_code: int = 0
    response_time: float = 0.0
    error: Optional[str] = None
    proxy_used: Optional[str] = None


class CommercialFetchService:
    """Enterprise-grade fetch service with advanced anti-detection"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.session_pool = {}
        self.site_configs = self._load_site_configs()
        self.request_stats = {'total': 0, 'success': 0, 'failed': 0}
    
    def _load_site_configs(self) -> Dict[str, SiteConfig]:
        """Load site-specific configurations"""
        return {
            'amazon.co.uk': SiteConfig(
                base_delay=5.0,
                max_delay=15.0,
                anti_bot_level='high',
                requires_js=True
            ),
            'johnlewis.com': SiteConfig(
                base_delay=3.0,
                max_delay=8.0,
                anti_bot_level='medium'
            ),
            'argos.co.uk': SiteConfig(
                base_delay=2.0,
                max_delay=6.0,
                anti_bot_level='low'
            ),
            # Add more as needed
        }
    
    async def fetch_with_intelligence(self, url: str, custom_config: Optional[Dict] = None) -> RequestResult:
        """Intelligent fetching with all anti-detection measures"""
        start_time = time.time()
        domain = urlparse(url).netloc
        
        try:
            # Get site configuration
            site_config = self._get_site_config(domain, custom_config)
            
            # Apply pre-request delays
            await self._apply_smart_delay(domain, site_config)
            
            # Choose optimal session
            session = await self._get_optimal_session(domain, site_config)
            
            # Execute request with protection
            result = await self._protected_request(session, url, site_config)
            
            # Update statistics
            self._update_stats(result.success)
            
            result.response_time = time.time() - start_time
            return result
            
        except Exception as e:
            logger.error(f"Fetch failed for {url}: {e}")
            self._update_stats(False)
            return RequestResult(
                success=False,
                error=str(e),
                response_time=time.time() - start_time
            )
    
    def _get_site_config(self, domain: str, custom_config: Optional[Dict]) -> SiteConfig:
        """Get configuration for specific domain"""
        base_config = self.site_configs.get(domain, SiteConfig())
        
        if custom_config:
            # Override with custom settings
            for key, value in custom_config.items():
                setattr(base_config, key, value)
        
        return base_config
    
    async def _apply_smart_delay(self, domain: str, config: SiteConfig):
        """Apply intelligent delay based on domain and recent activity"""
        # Check recent requests to this domain
        recent_requests = cache.get(f'recent_requests_{domain}', 0)
        
        # Calculate delay based on recent activity
        base_delay = config.base_delay
        if recent_requests > 10:
            # High activity - increase delay
            delay = base_delay * (1 + (recent_requests / 20))
            delay = min(delay, config.max_delay)
        else:
            # Normal activity
            delay = random.uniform(base_delay, base_delay * 1.5)
        
        # Add randomization to appear human
        delay += random.uniform(0.5, 2.0)
        
        logger.debug(f"Applying delay of {delay:.1f}s for {domain}")
        await asyncio.sleep(delay)
        
        # Update request counter
        cache.set(f'recent_requests_{domain}', recent_requests + 1, timeout=300)
    
    async def _get_optimal_session(self, domain: str, config: SiteConfig) -> aiohttp.ClientSession:
        """Get optimal session for domain"""
        session_key = f"{domain}_{config.anti_bot_level}"
        
        if session_key not in self.session_pool:
            # Create new session with optimal settings
            self.session_pool[session_key] = await self._create_protected_session(config)
        
        return self.session_pool[session_key]
    
    async def _create_protected_session(self, config: SiteConfig) -> aiohttp.ClientSession:
        """Create session with advanced protection"""
        # SSL context for TLS fingerprint variation
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA')
        
        # Connector with optimized settings
        connector = aiohttp.TCPConnector(
            ssl_context=ssl_context,
            limit=10,
            limit_per_host=2,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        # Headers that mimic real browsers
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Create session with timeout
        timeout = aiohttp.ClientTimeout(total=30)
        
        session = aiohttp.ClientSession(
            connector=connector,
            headers=headers,
            timeout=timeout
        )
        
        return session
    
    async def _protected_request(self, session: aiohttp.ClientSession, url: str, config: SiteConfig) -> RequestResult:
        """Execute protected request"""
        try:
            # Get proxy if needed
            proxy = None
            if config.anti_bot_level in ['medium', 'high']:
                proxy_config = proxy_manager.get_proxy(target_country=config.target_geo)
                if proxy_config:
                    proxy = f"http://{proxy_config.host}:{proxy_config.port}"
            
            # Execute request
            async with session.get(url, proxy=proxy) as response:
                content = await response.text()
                
                return RequestResult(
                    success=response.status == 200,
                    content=content,
                    status_code=response.status,
                    proxy_used=proxy
                )
                
        except Exception as e:
            logger.warning(f"Protected request failed: {e}")
            return RequestResult(
                success=False,
                error=str(e)
            )
    
    def _update_stats(self, success: bool):
        """Update request statistics"""
        self.request_stats['total'] += 1
        if success:
            self.request_stats['success'] += 1
        else:
            self.request_stats['failed'] += 1
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        total = self.request_stats['total']
        if total == 0:
            return {'success_rate': 0.0, 'total_requests': 0}
        
        return {
            'success_rate': self.request_stats['success'] / total,
            'total_requests': total,
            'failed_requests': self.request_stats['failed']
        }
    
    async def cleanup(self):
        """Cleanup sessions"""
        for session in self.session_pool.values():
            await session.close()
        self.session_pool.clear()


# Global fetch service instance
fetch_service = CommercialFetchService()
