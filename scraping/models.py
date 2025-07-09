"""
Express Deals - Web Scraping Models
Defines models for managing scraping targets, rules, and collected data
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Category
import json


class ScrapeTarget(models.Model):
    """
    Defines websites and product categories to scrape
    """
    SITE_CHOICES = [
        ('amazon', 'Amazon'),
        ('walmart', 'Walmart'),
        ('target', 'Target'),
        ('bestbuy', 'Best Buy'),
        ('ebay', 'eBay'),
        ('newegg', 'Newegg'),
        ('custom', 'Custom Website'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('disabled', 'Disabled'),
    ]
    
    name = models.CharField(max_length=200)
    site_type = models.CharField(max_length=50, choices=SITE_CHOICES)
    base_url = models.URLField()
    search_url_template = models.TextField(help_text="URL template with {query} placeholder")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Scraping configuration
    scrape_frequency_hours = models.PositiveIntegerField(default=24)
    max_pages = models.PositiveIntegerField(default=5)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # CSS Selectors for data extraction
    product_selector = models.TextField(help_text="CSS selector for product containers")
    title_selector = models.TextField(help_text="CSS selector for product title")
    price_selector = models.TextField(help_text="CSS selector for product price")
    image_selector = models.TextField(help_text="CSS selector for product image")
    url_selector = models.TextField(help_text="CSS selector for product URL")
    rating_selector = models.TextField(blank=True, help_text="CSS selector for rating")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_scraped = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.site_type})"
    
    class Meta:
        ordering = ['-created_at']


class ScrapeJob(models.Model):
    """
    Tracks individual scraping jobs and their results
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    target = models.ForeignKey(ScrapeTarget, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    search_query = models.CharField(max_length=500, blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    products_found = models.PositiveIntegerField(default=0)
    products_imported = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    # Job metadata
    pages_scraped = models.PositiveIntegerField(default=0)
    execution_time_seconds = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Job #{self.id} - {self.target.name} ({self.status})"
    
    class Meta:
        ordering = ['-started_at']


class ScrapedProduct(models.Model):
    """
    Stores raw scraped product data before processing
    """
    job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=200, help_text="Product ID from source site")
    
    # Raw scraped data
    title = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField()
    product_url = models.URLField()
    description = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    review_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional metadata
    brand = models.CharField(max_length=200, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    shipping_info = models.TextField(blank=True)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    imported_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title[:50]}... - ${self.price}"
    
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100, 2)
        return 0
    
    class Meta:
        ordering = ['-scraped_at']
        unique_together = ['job', 'external_id']


class PriceAlert(models.Model):
    """
    User-defined price alerts for products
    """
    ALERT_TYPES = [
        ('below', 'Price Below'),
        ('above', 'Price Above'),
        ('change', 'Price Change'),
        ('percentage', 'Percentage Drop'),
        ('deal', 'Deal Alert'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('triggered', 'Triggered'),
        ('paused', 'Paused'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    search_keywords = models.CharField(max_length=500, blank=True, help_text="Alert for any product matching keywords")
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage_threshold = models.PositiveIntegerField(null=True, blank=True, help_text="Percentage drop threshold")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Notification preferences
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    
    # Enhanced price tracking fields
    onset_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                     help_text="Price when alert was created")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       help_text="Latest tracked price")
    last_price_update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        if self.product:
            return f"Alert: {self.product.name} - {self.get_alert_type_display()}"
        return f"Keyword Alert: {self.search_keywords} - {self.get_alert_type_display()}"
    
    class Meta:
        ordering = ['-created_at']


class AlertNotification(models.Model):
    """
    Records of sent alert notifications
    """
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('webhook', 'Webhook'),
    ]
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    alert = models.ForeignKey(PriceAlert, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    message = models.TextField()
    recipient = models.CharField(max_length=200)  # email, phone, or device ID
    
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.channel} to {self.recipient} - {self.status}"
    
    class Meta:
        ordering = ['-sent_at']
