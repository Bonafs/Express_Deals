"""
Express Deals - Alert Management Forms
Forms for creating and managing price alerts
"""

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import PriceAlert
from products.models import Product


class PriceAlertForm(forms.ModelForm):
    """
    Form for creating and editing price alerts
    """
    
    class Meta:
        model = PriceAlert
        fields = [
            'product', 'search_keywords', 'product_url', 'alert_type', 
            'target_price', 'percentage_threshold',
            'email_enabled', 'sms_enabled', 'push_enabled',
            'expires_at'
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select a product'
            }),
            'search_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter keywords to monitor (e.g., "iPhone 13 Pro")',
                'maxlength': 500
            }),
            'product_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product URL (e.g., Amazon, eBay, Currys link)',
                'maxlength': 500
            }),
            'alert_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'target_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'percentage_threshold': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 20 for 20% off',
                'min': '1',
                'max': '90'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'email_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sms_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'push_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize field labels and help text
        self.fields['product'].label = 'Specific Product (Optional)'
        self.fields['product'].help_text = 'Choose a specific product to monitor, or leave blank to use keywords/URL'
        self.fields['product'].required = False
        
        self.fields['search_keywords'].label = 'Search Keywords (Optional)'
        self.fields['search_keywords'].help_text = 'Monitor any product matching these keywords'
        self.fields['search_keywords'].required = False
        
        self.fields['product_url'].label = 'Product URL (Optional)'
        self.fields['product_url'].help_text = 'Direct link to external product for tracking (Amazon, eBay, etc.)'
        self.fields['product_url'].required = False
        
        self.fields['alert_type'].label = 'Alert Type'
        self.fields['alert_type'].choices = [
            ('below', 'Price drops below target'),
            ('percentage', 'Percentage discount reaches threshold'),
            ('deal', 'Any good deal (20%+ off or under £50)'),
        ]
        
        self.fields['target_price'].label = 'Target Price (£)'
        self.fields['target_price'].help_text = 'Alert when price drops to this amount or below'
        self.fields['target_price'].required = False
        
        self.fields['percentage_threshold'].label = 'Discount Threshold (%)'
        self.fields['percentage_threshold'].help_text = 'Alert when discount reaches this percentage'
        self.fields['percentage_threshold'].required = False
        
        self.fields['expires_at'].label = 'Expiration Date (Optional)'
        self.fields['expires_at'].help_text = 'Alert will automatically disable after this date'
        self.fields['expires_at'].required = False
        
        # Notification preferences
        self.fields['email_enabled'].label = 'Email Notifications'
        self.fields['sms_enabled'].label = 'SMS Notifications'
        self.fields['push_enabled'].label = 'Browser Notifications'
        
        # Set default values
        self.fields['email_enabled'].initial = True
        self.fields['push_enabled'].initial = True
        self.fields['sms_enabled'].initial = False
    
    def clean(self):
        """
        Custom validation for the form
        """
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        search_keywords = cleaned_data.get('search_keywords')
        product_url = cleaned_data.get('product_url')
        alert_type = cleaned_data.get('alert_type')
        target_price = cleaned_data.get('target_price')
        percentage_threshold = cleaned_data.get('percentage_threshold')
        
        # Must specify either product, keywords, or URL
        if not product and not search_keywords and not product_url:
            raise forms.ValidationError(
                "You must specify either a specific product, search keywords, or a product URL."
            )
        
        # Validate product URL if provided
        if product_url:
            supported_sites = [
                'amazon.co.uk', 'amazon.com', 'ebay.co.uk', 'ebay.com',
                'currys.co.uk', 'johnlewis.com', 'argos.co.uk',
                'asos.com', 'next.co.uk', 'jdsports.co.uk'
            ]
            
            if not any(site in product_url.lower() for site in supported_sites):
                raise forms.ValidationError(
                    f"Product URL must be from a supported site: {', '.join(supported_sites)}"
                )
        
        # Validate based on alert type
        if alert_type == 'below':
            if not target_price:
                raise forms.ValidationError(
                    "Target price is required for 'price below' alerts."
                )
        
        elif alert_type == 'percentage':
            if not percentage_threshold:
                raise forms.ValidationError(
                    "Percentage threshold is required for discount alerts."
                )
            
            if percentage_threshold < 1 or percentage_threshold > 90:
                raise forms.ValidationError(
                    "Percentage threshold must be between 1% and 90%."
                )
        
        # Validate target price if specified
        if target_price and target_price <= 0:
            raise forms.ValidationError("Target price must be greater than zero.")
        
        return cleaned_data


class QuickAlertForm(forms.Form):
    """
    Simplified form for quick alert creation from product pages
    """
    alert_type = forms.ChoiceField(
        choices=[
            ('below', 'Notify when price drops below'),
            ('percentage', 'Notify when discount reaches'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    target_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        })
    )
    
    percentage_threshold = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)],
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '20',
            'min': '1',
            'max': '90'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        alert_type = cleaned_data.get('alert_type')
        target_price = cleaned_data.get('target_price')
        percentage_threshold = cleaned_data.get('percentage_threshold')
        
        if alert_type == 'below' and not target_price:
            raise forms.ValidationError("Target price is required for price alerts.")
        
        if alert_type == 'percentage' and not percentage_threshold:
            raise forms.ValidationError("Percentage threshold is required for discount alerts.")
        
        return cleaned_data


class BulkAlertForm(forms.Form):
    """
    Form for creating alerts for multiple products at once
    """
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    alert_type = forms.ChoiceField(
        choices=[
            ('below', 'Price drops below target'),
            ('percentage', 'Percentage discount reaches threshold'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    target_price_percentage = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Percentage below current price (e.g., 20 for 20% off current price)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '20',
            'min': '1',
            'max': '50'
        })
    )
    
    percentage_threshold = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)],
        required=False,
        help_text="For discount alerts: minimum discount percentage",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '25',
            'min': '1',
            'max': '90'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        alert_type = cleaned_data.get('alert_type')
        percentage_threshold = cleaned_data.get('percentage_threshold')
        
        if alert_type == 'percentage' and not percentage_threshold:
            raise forms.ValidationError(
                "Percentage threshold is required for discount alerts."
            )
        
        return cleaned_data


class AlertPreferencesForm(forms.Form):
    """
    Form for managing user notification preferences
    """
    email_alerts = forms.BooleanField(
        required=False,
        label="Email Notifications",
        help_text="Receive price alerts via email"
    )
    
    sms_alerts = forms.BooleanField(
        required=False,
        label="SMS Notifications",
        help_text="Receive price alerts via text message"
    )
    
    push_alerts = forms.BooleanField(
        required=False,
        label="Browser Notifications",
        help_text="Receive real-time notifications in your browser"
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label="Phone Number",
        help_text="Required for SMS notifications (format: +1234567890)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890'
        })
    )
    
    daily_digest = forms.BooleanField(
        required=False,
        label="Daily Deal Digest",
        help_text="Receive a daily email with the best deals"
    )
    
    weekly_summary = forms.BooleanField(
        required=False,
        label="Weekly Summary",
        help_text="Receive a weekly summary of your alerts and savings"
    )
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '').strip()
        
        if phone_number:
            # Basic phone number validation
            import re
            if not re.match(r'^\+?1?\d{10,15}$', phone_number.replace(' ', '').replace('-', '')):
                raise forms.ValidationError(
                    "Please enter a valid phone number (10-15 digits, optionally starting with +1)"
                )
        
        return phone_number
