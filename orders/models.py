from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from products.models import Product


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(
        max_length=40, unique=True, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for session {self.session_key}"
    
    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        """Calculate subtotal of all items"""
        return sum(item.get_total_price() for item in self.items.all())
    
    @property
    def tax_amount(self):
        """Calculate tax amount (20% VAT)"""
        return self.subtotal * Decimal('0.20')
    
    @property
    def shipping_cost(self):
        """Calculate shipping cost (free if over £50)"""
        return Decimal('0.00') if self.subtotal >= 50 else Decimal('4.99')
    
    @property
    def total(self):
        """Calculate total including tax and shipping"""
        return self.subtotal + self.tax_amount + self.shipping_cost
    
    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual items in shopping cart"""
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        cart_owner = (
            self.cart.user.username if self.cart.user
            else f"session {self.cart.session_key}"
        )
        return (
            f"{self.quantity} x {self.product.name} in "
            f"{cart_owner}'s cart"
        )
    
    def get_total_price(self):
        """Calculate total price for this item"""
        return self.product.price * self.quantity
    
    def clean(self):
        """Validate cart item"""
        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive")
        if self.quantity > 100:
            raise ValidationError("Quantity cannot exceed 100")


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    order_number = models.CharField(max_length=20, unique=True)
    
    # Order amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending'
    )
    
    # Shipping information
    shipping_name = models.CharField(max_length=100)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=20, blank=True)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(
        max_length=100, default='United Kingdom'
    )
    
    # Payment integration
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import uuid
        return f"ED-{uuid.uuid4().hex[:8].upper()}"


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} in "
            f"order {self.order.order_number}"
        )
    
    def get_total_price(self):
        """Calculate total price for this item"""
        return self.price * self.quantity


class WishlistItem(models.Model):
    """User wishlist items"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist_items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"
