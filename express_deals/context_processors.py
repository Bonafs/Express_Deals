"""
Context processors for Express Deals
"""
from orders.models import Cart


def cart_processor(request):
    """Add cart information to template context."""
    cart_total_items = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_total_items = cart.total_items
        except Cart.DoesNotExist:
            cart_total_items = 0
    
    return {
        'cart_total_items': cart_total_items,
    }
