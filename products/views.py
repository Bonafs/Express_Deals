from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from .models import Product, Category, ProductReview
from .forms import ProductSearchForm
from scraping.url_tracking_service import url_tracking_service
from scraping.models import PriceAlert
import logging
import json
from django.utils import timezone
from decimal import Decimal

logger = logging.getLogger(__name__)

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # Restored complex template
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(
            is_featured=True, is_active=True
        )[:6]
        
        # URL tracking functionality
        context['url_tracking_enabled'] = True
        context['supported_retailers'] = list(url_tracking_service.SUPPORTED_RETAILERS.keys())
        
        # Check if user has active alerts
        if self.request.user.is_authenticated:
            context['user_alert_count'] = PriceAlert.objects.filter(
                user=self.request.user, 
                status='active'
            ).count()
        else:
            context['user_alert_count'] = 0
        
        # Preserve filters in pagination
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Related products
        context['related_products'] = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(pk=product.pk)[:4]
        
        # Reviews
        reviews = ProductReview.objects.filter(product=product).select_related('user')
        context['reviews'] = reviews[:5]  # Show first 5 reviews
        context['review_count'] = reviews.count()
        
        # Average rating
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else 0
        
        # Rating distribution
        rating_counts = reviews.values('rating').annotate(count=Count('rating'))
        context['rating_distribution'] = {r['rating']: r['count'] for r in rating_counts}
        
        return context

class CategoryListView(ListView):
    model = Product
    template_name = 'products/category_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(
            category=self.category, is_active=True
        ).select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

def search_products(request):
    """AJAX search for autocomplete"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:10]
        
        results = [
            {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'url': product.get_absolute_url(),
                'image': product.image.url if product.image else None,
            }
            for product in products
        ]
        
        from django.http import JsonResponse
        return JsonResponse({'results': results})
    
    from django.http import JsonResponse
    return JsonResponse({'results': []})


def check_url_tracking(request):
    """
    API endpoint to check URL tracking effectiveness
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'Authentication required',
            'redirect_login': True
        })
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'})
    
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        
        if not url:
            return JsonResponse({'success': False, 'error': 'URL is required'})
        
        # Check tracking effectiveness
        effectiveness = url_tracking_service.get_tracking_effectiveness(url)
        
        return JsonResponse({
            'success': True,
            'effectiveness': effectiveness,
            'can_create_alert': effectiveness['can_track'] and effectiveness['score'] >= 40
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        logger.error(f"URL tracking check error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})


def create_url_alert(request):
    """
    API endpoint to create URL-based price alert
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'Authentication required',
            'redirect_login': True
        })
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST method required'})
    
    try:
        data = json.loads(request.body)
        url = data.get('url', '').strip()
        
        if not url:
            return JsonResponse({'success': False, 'error': 'URL is required'})
        
        # Prepare alert data
        alert_data = {
            'alert_type': data.get('alert_type', 'below'),
            'target_price': data.get('target_price'),
            'percentage_threshold': data.get('percentage_threshold'),
            'email_enabled': data.get('email_enabled', True),
            'sms_enabled': data.get('sms_enabled', False),
            'push_enabled': data.get('push_enabled', True)
        }
        
        # Validate required fields based on alert type
        if alert_data['alert_type'] == 'below' and not alert_data['target_price']:
            return JsonResponse({'success': False, 'error': 'Target price is required for price alerts'})
        
        if alert_data['alert_type'] == 'percentage' and not alert_data['percentage_threshold']:
            return JsonResponse({'success': False, 'error': 'Percentage threshold is required for discount alerts'})
        
        # Create alert
        success, message, alert = url_tracking_service.create_alert_for_url(
            request.user, url, alert_data
        )
        
        if success:
            return JsonResponse({
                'success': True,
                'message': message,
                'alert_id': alert.id if alert else None,
                'redirect_dashboard': reverse('alerts:dashboard')
            })
        else:
            return JsonResponse({'success': False, 'error': message})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        logger.error(f"URL alert creation error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})


def get_user_tracking_stats(request):
    """
    API endpoint to get user's URL tracking statistics
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    try:
        from scraping.models import PriceAlert
        
        # Get user's URL-based alerts
        url_alerts = PriceAlert.objects.filter(
            user=request.user,
            product_url__isnull=False
        ).exclude(product_url='')
        
        stats = {
            'total_url_alerts': url_alerts.count(),
            'active_url_alerts': url_alerts.filter(status='active').count(),
            'triggered_url_alerts': url_alerts.filter(status='triggered').count(),
            'recent_url_alerts': []
        }
        
        # Get recent URL alerts
        recent_alerts = url_alerts.filter(status='active').order_by('-created_at')[:5]
        for alert in recent_alerts:
            try:
                from urllib.parse import urlparse
                domain = urlparse(alert.product_url).netloc
                retailer_name = url_tracking_service.SUPPORTED_RETAILERS.get(domain, {}).get('name', domain)
            except:
                retailer_name = 'Unknown'
            
            stats['recent_url_alerts'].append({
                'id': alert.id,
                'retailer': retailer_name,
                'target_price': str(alert.target_price) if alert.target_price else None,
                'alert_type': alert.get_alert_type_display(),
                'created_at': alert.created_at.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"User tracking stats error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})
