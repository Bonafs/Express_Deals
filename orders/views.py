from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView, ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.core.exceptions import ValidationError
import json

from .models import Cart, CartItem, Order, OrderItem, WishlistItem
from products.models import Product


class CartView(LoginRequiredMixin, View):
    """
    Display shopping cart contents
    """
    template_name = 'orders/cart.html'
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('product').all(),
        }
        return render(request, self.template_name, context)


class AddToCartView(LoginRequiredMixin, View):
    """
    Add item to shopping cart (AJAX and regular POST)
    """
    
    def post(self, request):
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity < 1 or quantity > 100:
                raise ValidationError("Quantity must be between 1 and 100")
            
            product = get_object_or_404(Product, id=product_id, is_active=True)
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Check if item already exists in cart
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not item_created:
                # Update quantity if item already exists
                cart_item.quantity += quantity
                if cart_item.quantity > 100:
                    cart_item.quantity = 100
                cart_item.save()
            
            messages.success(request, f"Added {product.name} to your cart!")
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"Added {product.name} to your cart!",
                    'cart_total_items': cart.total_items,
                    'cart_subtotal': str(cart.subtotal),
                })
            
            return redirect('orders:cart')
            
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


class UpdateCartView(LoginRequiredMixin, View):
    """
    Update cart item quantity
    """
    
    def post(self, request):
        try:
            cart_item_id = request.POST.get('cart_item_id')
            quantity = int(request.POST.get('quantity', 1))
            
            if quantity < 1 or quantity > 100:
                raise ValidationError("Quantity must be between 1 and 100")
            
            cart_item = get_object_or_404(
                CartItem, 
                id=cart_item_id, 
                cart__user=request.user
            )
            
            cart_item.quantity = quantity
            cart_item.save()
            
            messages.success(request, "Cart updated successfully!")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': "Cart updated successfully!",
                    'item_total': str(cart_item.get_total_price()),
                    'cart_subtotal': str(cart_item.cart.subtotal),
                    'cart_total': str(cart_item.cart.total),
                })
            
            return redirect('orders:cart')
            
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            return redirect('orders:cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Remove item from shopping cart
    """
    
    def post(self, request):
        try:
            cart_item_id = request.POST.get('cart_item_id')
            cart_item = get_object_or_404(
                CartItem, 
                id=cart_item_id, 
                cart__user=request.user
            )
            
            product_name = cart_item.product.name
            cart_item.delete()
            
            messages.success(request, f"Removed {product_name} from your cart!")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                cart = Cart.objects.get(user=request.user)
                return JsonResponse({
                    'success': True,
                    'message': f"Removed {product_name} from your cart!",
                    'cart_total_items': cart.total_items,
                    'cart_subtotal': str(cart.subtotal),
                    'cart_total': str(cart.total),
                })
            
            return redirect('orders:cart')
            
        except Exception as e:
            messages.error(request, "Error removing item from cart")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            return redirect('orders:cart')


class CheckoutView(LoginRequiredMixin, View):
    """
    Checkout process - collect shipping information
    """
    template_name = 'orders/checkout.html'
    
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('orders:cart')
        
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('product').all(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('orders:cart')
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    subtotal=cart.subtotal,
                    tax_amount=cart.tax_amount,
                    shipping_cost=0,  # Free shipping for now
                    total=cart.total,
                    shipping_name=request.POST.get('shipping_name'),
                    shipping_email=request.POST.get('shipping_email'),
                    shipping_phone=request.POST.get('shipping_phone', ''),
                    shipping_address_line1=request.POST.get('shipping_address_line1'),
                    shipping_address_line2=request.POST.get('shipping_address_line2', ''),
                    shipping_city=request.POST.get('shipping_city'),
                    shipping_state=request.POST.get('shipping_state'),
                    shipping_postal_code=request.POST.get('shipping_postal_code'),
                    shipping_country=request.POST.get('shipping_country', 'United States'),
                )
                
                # Create order items from cart items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,
                    )
                
                # Clear cart
                cart.items.all().delete()
                
                messages.success(request, f"Order {order.order_number} created successfully!")
                return redirect('payments:payment', order_id=order.id)
                
        except Exception as e:
            messages.error(request, f"Error creating order: {str(e)}")
            return redirect('orders:checkout')


class OrderListView(LoginRequiredMixin, ListView):
    """
    Display user's order history
    """
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Display individual order details
    """
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


class WishlistView(LoginRequiredMixin, ListView):
    """
    Display user's wishlist
    """
    model = WishlistItem
    template_name = 'orders/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 20
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')


class AddToWishlistView(LoginRequiredMixin, View):
    """
    Add/remove item from wishlist
    """
    
    def post(self, request):
        try:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if created:
                messages.success(request, f"Added {product.name} to your wishlist!")
                action = 'added'
            else:
                wishlist_item.delete()
                messages.success(request, f"Removed {product.name} from your wishlist!")
                action = 'removed'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'action': action,
                    'message': f"{'Added' if action == 'added' else 'Removed'} {product.name} {'to' if action == 'added' else 'from'} your wishlist!",
                })
            
            return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))
            
        except Exception as e:
            messages.error(request, "Error updating wishlist")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
            return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


# Legacy placeholder view for backward compatibility
class OrderHistoryView(OrderListView):
    """Redirect to OrderListView for backward compatibility"""
    pass
