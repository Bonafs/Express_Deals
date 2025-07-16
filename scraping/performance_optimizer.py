"""
Express Deals - Advanced Proxy Error Analysis and Performance Optimizer
Analyzes scraping errors and automatically improves performance
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests
from django.core.cache import cache
from .proxy_manager import proxy_manager

logger = logging.getLogger(__name__)


@dataclass
class ScrapingError:
    """Track scraping error details"""
    timestamp: datetime
    error_type: str
    target_url: str
    proxy_used: Optional[str]
    http_status: Optional[int]
    error_message: str
    retry_count: int


class ScrapingPerformanceOptimizer:
    """
    Advanced system to analyze scraping errors and optimize performance
    """
    
    def __init__(self):
        self.error_history: List[ScrapingError] = []
        self.blocked_domains: Dict[str, datetime] = {}
        self.domain_delays: Dict[str, float] = {}
        self.proxy_performance: Dict[str, Dict] = {}
        
    def analyze_terminal_errors(self, error_logs: List[str]) -> Dict:
        """
        Analyze terminal error logs to identify patterns and issues
        """
        analysis = {
            'proxy_errors': 0,
            'timeout_errors': 0,
            'http_errors': 0,
            'blocked_domains': set(),
            'failing_proxies': set(),
            'recommendations': []
        }
        
        for log_line in error_logs:
            if 'Proxy error' in log_line:
                analysis['proxy_errors'] += 1
                # Extract proxy info if available
                if 'proxy:' in log_line:
                    proxy = log_line.split('proxy:')[1].split()[0]
                    analysis['failing_proxies'].add(proxy)
            
            elif 'Timeout' in log_line or 'timeout' in log_line:
                analysis['timeout_errors'] += 1
                
            elif 'Failed to fetch' in log_line:
                analysis['http_errors'] += 1
                # Extract domain
                if 'https://' in log_line:
                    url = log_line.split('https://')[1].split()[0]
                    domain = url.split('/')[0]
                    analysis['blocked_domains'].add(domain)
            
            elif any(code in log_line for code in ['403', '429', '503', '502']):
                analysis['http_errors'] += 1
        
        # Generate recommendations
        if analysis['proxy_errors'] > 5:
            analysis['recommendations'].append("HIGH_PROXY_FAILURE_RATE")
        
        if analysis['timeout_errors'] > 3:
            analysis['recommendations'].append("INCREASE_TIMEOUTS")
            
        if len(analysis['blocked_domains']) > 2:
            analysis['recommendations'].append("DOMAIN_BLOCKING_DETECTED")
            
        if len(analysis['failing_proxies']) > 0:
            analysis['recommendations'].append("ROTATE_FAILING_PROXIES")
        
        return analysis
    
    def implement_performance_improvements(self, analysis: Dict):
        """
        Automatically implement performance improvements based on error analysis
        """
        improvements_made = []
        
        # Handle high proxy failure rate
        if "HIGH_PROXY_FAILURE_RATE" in analysis['recommendations']:
            self._improve_proxy_rotation()
            improvements_made.append("Enhanced proxy rotation algorithm")
        
        # Handle timeout issues
        if "INCREASE_TIMEOUTS" in analysis['recommendations']:
            self._adjust_timeout_settings()
            improvements_made.append("Increased timeout settings")
        
        # Handle domain blocking
        if "DOMAIN_BLOCKING_DETECTED" in analysis['recommendations']:
            self._implement_domain_cooling(analysis['blocked_domains'])
            improvements_made.append("Implemented domain cooling period")
        
        # Handle failing proxies
        if "ROTATE_FAILING_PROXIES" in analysis['recommendations']:
            self._remove_failing_proxies(analysis['failing_proxies'])
            improvements_made.append("Removed failing proxies from rotation")
        
        return improvements_made
    
    def _improve_proxy_rotation(self):
        """
        Enhance proxy rotation strategy
        """
        # Switch to performance-based rotation
        proxy_manager.current_strategy = 'performance_based'
        
        # Cleanup blocked proxies more aggressively
        proxy_manager.cleanup_blocked_proxies()
        
        # Add more premium proxies if available
        self._add_premium_proxies()
        
        logger.info("Enhanced proxy rotation algorithm activated")
    
    def _adjust_timeout_settings(self):
        """
        Dynamically adjust timeout settings based on errors
        """
        # Increase timeouts globally
        cache.set('scraper_timeout', 45, timeout=3600)  # 45 seconds
        cache.set('page_load_timeout', 30, timeout=3600)  # 30 seconds
        
        logger.info("Increased timeout settings for better reliability")
    
    def _implement_domain_cooling(self, blocked_domains: set):
        """
        Implement cooling period for blocked domains
        """
        cooling_period = datetime.now() + timedelta(hours=2)
        
        for domain in blocked_domains:
            self.blocked_domains[domain] = cooling_period
            # Set longer delays for these domains
            self.domain_delays[domain] = 10.0  # 10 second delay
            
        logger.info(f"Implemented cooling period for {len(blocked_domains)} domains")
    
    def _remove_failing_proxies(self, failing_proxies: set):
        """
        Remove consistently failing proxies from rotation
        """
        for proxy_url in failing_proxies:
            # Find and remove the proxy
            proxy_to_remove = None
            for proxy in proxy_manager.proxies:
                if proxy.url == proxy_url:
                    proxy_to_remove = proxy
                    break
            
            if proxy_to_remove:
                proxy_manager.proxies.remove(proxy_to_remove)
                if proxy_url in proxy_manager.proxy_stats:
                    del proxy_manager.proxy_stats[proxy_url]
                
        logger.info(f"Removed {len(failing_proxies)} failing proxies")
    
    def _add_premium_proxies(self):
        """
        Add additional premium proxies for better performance
        """
        # Add more UK-specific proxies
        additional_proxies = [
            {
                'host': 'proxy-uk-1.example.com',
                'port': 8000,
                'country': 'UK',
                'provider': 'Premium-UK'
            },
            {
                'host': 'proxy-uk-2.example.com', 
                'port': 8001,
                'country': 'UK',
                'provider': 'Premium-UK'
            },
            # Add more as needed
        ]
        
        for proxy_data in additional_proxies:
            try:
                from .proxy_manager import ProxyConfig
                proxy = ProxyConfig(**proxy_data)
                
                # Test proxy before adding
                is_working, response_time = proxy_manager.test_proxy(proxy)
                if is_working:
                    proxy_manager.proxies.append(proxy)
                    proxy_manager.proxy_stats[proxy.url] = proxy_manager.ProxyStats(proxy.url)
                    logger.info(f"Added premium proxy: {proxy.host}")
                
            except Exception as e:
                logger.warning(f"Failed to add premium proxy: {e}")
    
    def get_optimized_request_settings(self, target_domain: str) -> Dict:
        """
        Get optimized request settings based on error history
        """
        settings = {
            'timeout': 30,
            'delay': 2.0,
            'max_retries': 3,
            'use_premium_proxy': False
        }
        
        # Check if domain is in cooling period
        if target_domain in self.blocked_domains:
            cooling_end = self.blocked_domains[target_domain]
            if datetime.now() < cooling_end:
                settings['delay'] = 15.0  # Much longer delay
                settings['use_premium_proxy'] = True
                settings['max_retries'] = 1  # Fewer retries
        
        # Apply domain-specific delays
        if target_domain in self.domain_delays:
            settings['delay'] = max(settings['delay'], self.domain_delays[target_domain])
        
        # Increase timeout for problematic domains
        recent_errors = self._get_recent_domain_errors(target_domain)
        if recent_errors > 3:
            settings['timeout'] = 45
            settings['max_retries'] = 5
        
        return settings
    
    def _get_recent_domain_errors(self, domain: str) -> int:
        """
        Get count of recent errors for a specific domain
        """
        cutoff_time = datetime.now() - timedelta(hours=1)
        recent_errors = [
            error for error in self.error_history
            if error.timestamp > cutoff_time and domain in error.target_url
        ]
        return len(recent_errors)
    
    def record_error(self, error_type: str, target_url: str, proxy_used: str = None, 
                    http_status: int = None, error_message: str = "", retry_count: int = 0):
        """
        Record a scraping error for analysis
        """
        error = ScrapingError(
            timestamp=datetime.now(),
            error_type=error_type,
            target_url=target_url,
            proxy_used=proxy_used,
            http_status=http_status,
            error_message=error_message,
            retry_count=retry_count
        )
        
        self.error_history.append(error)
        
        # Keep only last 1000 errors to prevent memory issues
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-1000:]
    
    def generate_performance_report(self) -> Dict:
        """
        Generate comprehensive performance report
        """
        report = {
            'total_errors': len(self.error_history),
            'error_types': {},
            'most_problematic_domains': {},
            'proxy_success_rates': {},
            'recommendations': []
        }
        
        # Analyze error types
        for error in self.error_history:
            error_type = error.error_type
            if error_type not in report['error_types']:
                report['error_types'][error_type] = 0
            report['error_types'][error_type] += 1
        
        # Find most problematic domains
        domain_errors = {}
        for error in self.error_history:
            try:
                domain = error.target_url.split('://')[1].split('/')[0]
                if domain not in domain_errors:
                    domain_errors[domain] = 0
                domain_errors[domain] += 1
            except:
                continue
        
        # Sort by error count
        report['most_problematic_domains'] = dict(
            sorted(domain_errors.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        
        # Generate recommendations
        if report['total_errors'] > 50:
            report['recommendations'].append("Consider implementing more aggressive rate limiting")
        
        if 'proxy_error' in report['error_types'] and report['error_types']['proxy_error'] > 20:
            report['recommendations'].append("Upgrade to premium proxy service")
        
        if len(report['most_problematic_domains']) > 0:
            top_domain = list(report['most_problematic_domains'].keys())[0]
            report['recommendations'].append(f"Implement specific handling for {top_domain}")
        
        return report


# Global optimizer instance
scraping_optimizer = ScrapingPerformanceOptimizer()
