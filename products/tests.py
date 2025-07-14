

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, ProductReview

class CategoryModelTest(TestCase):
    def test_str(self):
        cat = Category.objects.create(name='Electronics', slug='electronics')
        self.assertEqual(str(cat), 'Electronics')

class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Books', slug='books')
        self.product = Product.objects.create(
            name='Django Book', slug='django-book', category=self.cat,
            description='A book about Django', price=20, original_price=25, stock_quantity=10
        )

    def test_str(self):
        self.assertEqual(str(self.product), 'Django Book')

    def test_is_on_sale(self):
        self.assertTrue(self.product.is_on_sale)

    def test_discount_percentage(self):
        self.assertEqual(self.product.discount_percentage, 20)

class ProductImageModelTest(TestCase):
    def test_str(self):
        cat = Category.objects.create(name='Toys', slug='toys')
        prod = Product.objects.create(name='Toy Car', slug='toy-car', category=cat, description='A toy', price=10)
        img = ProductImage.objects.create(product=prod, image='test.jpg')
        self.assertIn('Toy Car', str(img))

class ProductReviewModelTest(TestCase):
    def test_str(self):
        user = User.objects.create_user(username='reviewer')
        cat = Category.objects.create(name='Games', slug='games')
        prod = Product.objects.create(name='Chess', slug='chess', category=cat, description='A game', price=15)
        review = ProductReview.objects.create(product=prod, user=user, rating=5, title='Great', comment='Loved it!')
        self.assertIn('Chess', str(review))
