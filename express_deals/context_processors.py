"""
Context processors for Express Deals
"""
from orders.models import Cart
import logging

logger = logging.getLogger(__name__)


def cart_processor(request):
    """Add cart information to template context."""
    cart_total_items = 0
    
    try:
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_total_items = cart.total_items
            except Cart.DoesNotExist:
                cart_total_items = 0
            except Exception as e:
                logger.error(f"Database error in cart_processor for user {request.user.id}: {e}")
                cart_total_items = 0
    except Exception as e:
        logger.error(f"Context processor error: {e}")
        cart_total_items = 0
    
    return {
        'cart_total_items': cart_total_items,
    }
