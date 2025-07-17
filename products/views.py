from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.urls import reverse
from .models import Product, Category, ProductReview
import logging
import json

logger = logging.getLogger(__name__)


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
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
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'created_at')
        if sort_by in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories for filtering
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(
            is_featured=True, is_active=True
        )[:6]
        
        # URL tracking functionality
        context['url_tracking_enabled'] = True
        context['supported_retailers'] = ['amazon', 'walmart', 'target']
        
        # Check if user has active alerts
        if self.request.user.is_authenticated:
            context['user_alert_count'] = 0
        else:
            context['user_alert_count'] = 0
        
        # Preserve filters in pagination
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_sort'] = self.request.GET.get('sort', 'created_at')
        context['current_min_price'] = self.request.GET.get('min_price', '')
        context['current_max_price'] = self.request.GET.get('max_price', '')
        
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
        
        # Get related products
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        # Get reviews
        reviews = ProductReview.objects.filter(product=product).select_related('user')
        
        # Calculate average rating
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Get rating distribution
        rating_counts = reviews.values('rating').annotate(count=Count('rating'))
        context['rating_distribution'] = {r['rating']: r['count'] for r in rating_counts}
        
        context['related_products'] = related_products
        context['reviews'] = reviews
        context['avg_rating'] = avg_rating
        context['review_count'] = reviews.count()
        
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)


def product_search(request):
    """Handle product search requests"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
        'current_category': category_id
    }
    
    return render(request, 'products/search_results.html', context)


def get_user_tracking_stats(request):
    """Get user's URL tracking statistics"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    try:
        stats = {
            'total_url_alerts': 0,
            'active_url_alerts': 0,
            'triggered_url_alerts': 0,
            'recent_url_alerts': []
        }
        
        return JsonResponse({'success': True, 'stats': stats})
        
    except Exception as e:
        logger.error(f"User tracking stats error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})


def track_url_click(request):
    """Track URL click for analytics"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            product_id = data.get('product_id')
            
            logger.info(f"URL click tracked: {url} for product {product_id}")
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            logger.error(f"URL tracking error: {e}")
            return JsonResponse({'success': False, 'error': 'Failed to track URL'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def search_products(request):
    """Handle product search requests - alias for product_search"""
    return product_search(request)


def check_url_tracking(request):
    """Check if URL tracking is available for a product"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    try:
        product_id = request.GET.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID required'})
        
        # Check if product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Mock response for URL tracking availability
        response = {
            'success': True,
            'tracking_available': True,
            'product_name': product.name,
            'supported_retailers': ['amazon', 'walmart', 'target'],
            'message': 'URL tracking is available for this product'
        }
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"URL tracking check error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})


def create_url_alert(request):
    """Create URL tracking alert for a product"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        target_url = data.get('target_url')
        target_price = data.get('target_price')
        
        if not all([product_id, target_url]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        # Check if product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Mock response for URL alert creation
        response = {
            'success': True,
            'alert_id': f"url_alert_{product_id}_{request.user.id}",
            'product_name': product.name,
            'target_url': target_url,
            'target_price': target_price,
            'message': 'URL tracking alert created successfully'
        }
        
        logger.info(f"URL alert created for user {request.user.id}: {target_url}")
        
        return JsonResponse(response)
        
    except Exception as e:
        logger.error(f"URL alert creation error: {e}")
        return JsonResponse({'success': False, 'error': 'Server error occurred'})
