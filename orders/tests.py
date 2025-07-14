

from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Category
from .models import Cart, CartItem, Order, OrderItem, WishlistItem

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cartuser')
        self.cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(name='Prod', slug='prod', category=self.cat, description='desc', price=10, stock_quantity=5)
        self.cart = Cart.objects.create(user=self.user, session_key='abc123')
        self.item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_str(self):
        self.assertIn('cartuser', str(self.cart))

    def test_total_items(self):
        self.assertEqual(self.cart.total_items, 2)

    def test_subtotal(self):
        self.assertEqual(self.cart.subtotal, 20)

    def test_total(self):
        self.assertAlmostEqual(float(self.cart.total), 21.7, places=1)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='orderuser')
        self.cat = Category.objects.create(name='Cat2', slug='cat2')
        self.product = Product.objects.create(name='Prod2', slug='prod2', category=self.cat, description='desc', price=15, stock_quantity=5)
        self.order = Order.objects.create(user=self.user, subtotal=30, tax_amount=2.55, shipping_cost=5, total=37.55, shipping_name='Name', shipping_email='a@b.com', shipping_address_line1='Addr', shipping_city='City', shipping_state='State', shipping_postal_code='12345')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=15)

    def test_order_str(self):
        self.assertIn('orderuser', str(self.order))

    def test_orderitem_str(self):
        self.assertIn('Prod2', str(self.order_item))

    def test_orderitem_total_price(self):
        self.assertEqual(self.order_item.get_total_price(), 30)

class WishlistItemModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='wishuser')
        cat = Category.objects.create(name='WishCat', slug='wishcat')
        prod = Product.objects.create(name='WishProd', slug='wishprod', category=cat, description='desc', price=5)
        wish = WishlistItem.objects.create(user=user, product=prod)
        self.assertIn('wishuser', str(wish))
