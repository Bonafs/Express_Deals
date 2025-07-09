#!/usr/bin/env python
"""
Express Deals UK - Currency Utilities
Handle multi-currency support with GBP as default
"""

import requests
from decimal import Decimal
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Exchange rate API (free tier available)
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/GBP"


class CurrencyConverter:
    """Handle currency conversions for Express Deals UK"""
    
    def __init__(self):
        self.rates = self.get_exchange_rates()
        self.default_currency = getattr(settings, 'DEFAULT_CURRENCY', 'GBP')
    
    def get_exchange_rates(self):
        """Fetch current exchange rates from API"""
        try:
            response = requests.get(EXCHANGE_API_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('rates', {})
        except Exception as e:
            logger.warning(f"Failed to fetch exchange rates: {e}")
        
        # Fallback rates if API fails
        return {
            'GBP': 1.0,
            'USD': 1.27,  # Approximate rates
            'EUR': 1.17,
        }
    
    def convert_price(self, amount, from_currency='GBP', to_currency='GBP'):
        """Convert price between currencies"""
        try:
            amount = Decimal(str(amount))
            
            if from_currency == to_currency:
                return amount
            
            # Convert to GBP first if needed
            if from_currency != 'GBP':
                gbp_rate = self.rates.get(from_currency, 1.0)
                amount = amount / Decimal(str(gbp_rate))
            
            # Convert from GBP to target currency
            if to_currency != 'GBP':
                target_rate = self.rates.get(to_currency, 1.0)
                amount = amount * Decimal(str(target_rate))
            
            return round(amount, 2)
            
        except Exception as e:
            logger.error(f"Currency conversion failed: {e}")
            return Decimal(str(amount))
    
    def format_price(self, amount, currency='GBP'):
        """Format price with appropriate currency symbol"""
        amount = Decimal(str(amount))
        
        currency_symbols = {
            'GBP': '£',
            'USD': '$',
            'EUR': '€',
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        if currency == 'GBP':
            return f"{symbol}{amount:,.2f}"
        else:
            return f"{symbol}{amount:,.2f} ({currency})"
    
    def get_multi_currency_display(self, gbp_amount):
        """Display price in multiple currencies"""
        gbp_amount = Decimal(str(gbp_amount))
        
        prices = {
            'GBP': {
                'amount': gbp_amount,
                'formatted': self.format_price(gbp_amount, 'GBP'),
                'symbol': '£'
            }
        }
        
        # Add USD and EUR conversions
        for currency in ['USD', 'EUR']:
            converted = self.convert_price(gbp_amount, 'GBP', currency)
            symbol_map = {'GBP': '£', 'USD': '$', 'EUR': '€'}
            prices[currency] = {
                'amount': converted,
                'formatted': self.format_price(converted, currency),
                'symbol': symbol_map.get(currency, currency)
            }
        
        return prices
    
    def parse_uk_price(self, price_text):
        """Parse UK price from text"""
        import re
        
        # UK price patterns
        patterns = getattr(settings, 'UK_PRICE_PATTERNS', [
            r'£\s*(\d+(?:\.\d{2})?)',  # £99.99
            r'(\d+(?:\.\d{2})?)\s*£',  # 99.99£
            r'GBP\s*(\d+(?:\.\d{2})?)',  # GBP 99.99
        ])
        
        for pattern in patterns:
            match = re.search(pattern, price_text)
            if match:
                try:
                    return Decimal(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return None


# Global instance
currency_converter = CurrencyConverter()


def format_gbp_price(amount):
    """Quick helper to format GBP price"""
    return currency_converter.format_price(amount, 'GBP')


def convert_to_gbp(amount, from_currency):
    """Quick helper to convert to GBP"""
    return currency_converter.convert_price(amount, from_currency, 'GBP')


def get_price_display(gbp_amount):
    """Get multi-currency price display"""
    return currency_converter.get_multi_currency_display(gbp_amount)
