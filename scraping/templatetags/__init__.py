"""
Custom template filters for price tracking
"""
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract arg from value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage_change(current, original):
    """Calculate percentage change between two values"""
    try:
        current = float(current)
        original = float(original)
        if original == 0:
            return 0
        return ((current - original) / original) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def price_status_class(current_price, target_price):
    """Return CSS class based on price comparison"""
    try:
        current = float(current_price)
        target = float(target_price)
        if current <= target:
            return 'text-success'
        elif current <= target * 1.1:  # Within 10% of target
            return 'text-warning'
        else:
            return 'text-danger'
    except (ValueError, TypeError):
        return 'text-muted'
