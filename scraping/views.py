"""
Express Deals - Alert Management Views
User-facing interface for managing price alerts and notifications
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urlparse

from .models import PriceAlert, AlertNotification, ScrapedProduct
from .forms import PriceAlertForm
from products.models import Product
from .url_tracking_service import url_tracking_service


@login_required
def alert_dashboard(request):
    """
    Enhanced user dashboard for managing price alerts with URL tracking
    """
    # Get user's alerts
    alerts = PriceAlert.objects.filter(user=request.user).select_related('product__category').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter in ['active', 'triggered', 'paused', 'expired']:
        alerts = alerts.filter(status=status_filter)
    
    # Filter by category if requested
    category_filter = request.GET.get('category')
    if category_filter:
        alerts = alerts.filter(product__category__name=category_filter)
    
    # Get categories for filter
    from products.models import Category
    categories = Category.objects.filter(
        products__pricealert__user=request.user
    ).distinct().order_by('name')
    
    # Pagination
    paginator = Paginator(alerts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get recent notifications
    recent_notifications = AlertNotification.objects.filter(
        alert__user=request.user
    ).order_by('-sent_at')[:5]
    
    # Enhanced statistics with URL tracking
    stats = {
        'total_alerts': alerts.count(),
        'active_alerts': PriceAlert.objects.filter(user=request.user, status='active').count(),
        'triggered_today': AlertNotification.objects.filter(
            alert__user=request.user,
            sent_at__date=timezone.now().date()
        ).count(),
        'savings_this_month': calculate_user_savings(request.user),
    }
    
    # URL tracking specific stats
    url_alerts = PriceAlert.objects.filter(
        user=request.user,
        product_url__isnull=False
    ).exclude(product_url='')
    
    stats.update({
        'url_alerts_count': url_alerts.count(),
        'product_alerts_count': PriceAlert.objects.filter(
            user=request.user, 
            product__isnull=False
        ).count(),
        'keyword_alerts_count': PriceAlert.objects.filter(
            user=request.user,
            search_keywords__isnull=False
        ).exclude(search_keywords='').count(),
    })
    
    # URL tracking effectiveness data for charts
    url_tracking_data = []
    if url_alerts.exists():
        for alert in url_alerts[:10]:  # Limit to avoid performance issues
            try:
                score, error = url_tracking_service.get_tracking_effectiveness_score(alert.product_url)
                if not error:
                    parsed_url = urlparse(alert.product_url)
                    domain = parsed_url.netloc.replace('www.', '')
                    
                    url_tracking_data.append({
                        'alert_id': alert.id,
                        'domain': domain,
                        'effectiveness': score,
                        'status': alert.status,
                        'created_at': alert.created_at.strftime('%Y-%m-%d')
                    })
            except Exception:
                pass
    
    context = {
        'page_obj': page_obj,
        'recent_notifications': recent_notifications,
        'stats': stats,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'categories': categories,
        'url_tracking_data': url_tracking_data,
        'supported_retailers': list(url_tracking_service.SUPPORTED_RETAILERS.keys()) if 'url_tracking_service' in locals() else [],
    }
    
    return render(request, 'alerts/dashboard.html', context)


@login_required
def create_alert(request, product_id=None):
    """
    Create a new price alert
    """
    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = PriceAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            if product:
                alert.product = product
            alert.save()
            
            messages.success(request, 'Price alert created successfully!')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Alert created successfully',
                    'alert_id': alert.id
                })
            
            return redirect('alerts:dashboard')
    else:
        initial_data = {}
        if product:
            initial_data = {
                'product': product,
                'target_price': product.price * 0.9,  # 10% discount as default
            }
        form = PriceAlertForm(initial=initial_data)
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'alerts/create_alert.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_alert(request, alert_id):
    """
    Toggle alert active/paused status
    """
    alert = get_object_or_404(PriceAlert, id=alert_id, user=request.user)
    
    if alert.status == 'active':
        alert.status = 'paused'
        message = 'Alert paused'
    elif alert.status == 'paused':
        alert.status = 'active'
        message = 'Alert activated'
    else:
        return JsonResponse({'success': False, 'error': 'Cannot toggle this alert'})
    
    alert.save()
    
    return JsonResponse({
        'success': True,
        'message': message,
        'new_status': alert.status
    })


@login_required
@require_http_methods(["POST"])
def delete_alert(request, alert_id):
    """
    Delete a price alert
    """
    alert = get_object_or_404(PriceAlert, id=alert_id, user=request.user)
    alert.delete()
    
    messages.success(request, 'Alert deleted successfully')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Alert deleted'})
    
    return redirect('alerts:dashboard')


@login_required
def alert_history(request):
    """
    View alert notification history
    """
    notifications = AlertNotification.objects.filter(
        alert__user=request.user
    ).order_by('-sent_at')
    
    # Filter by channel if requested
    channel_filter = request.GET.get('channel')
    if channel_filter in ['email', 'sms', 'push']:
        notifications = notifications.filter(channel=channel_filter)
    
    # Filter by date range
    date_filter = request.GET.get('date_range', '30')  # Default to 30 days
    if date_filter == '7':
        start_date = timezone.now() - timedelta(days=7)
    elif date_filter == '30':
        start_date = timezone.now() - timedelta(days=30)
    elif date_filter == '90':
        start_date = timezone.now() - timedelta(days=90)
    else:
        start_date = None
    
    if start_date:
        notifications = notifications.filter(sent_at__gte=start_date)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'channel_filter': channel_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'alerts/history.html', context)


@login_required
def discover_deals(request):
    """
    Discover current deals and trending products
    """
    # Get recent products with significant discounts
    recent_deals = ScrapedProduct.objects.filter(
        scraped_at__gte=timezone.now() - timedelta(hours=24),
        is_processed=True,
        imported_product__isnull=False
    ).exclude(
        original_price__isnull=True
    ).order_by('-scraped_at')
    
    # Filter for good deals (20%+ discount)
    good_deals = [
        product for product in recent_deals 
        if product.discount_percentage >= 20
    ][:20]
    
    # Get trending categories
    trending_categories = get_trending_categories()
    
    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        search_results = ScrapedProduct.objects.filter(
            Q(title__icontains=search_query) | Q(brand__icontains=search_query),
            is_processed=True,
            imported_product__isnull=False,
            scraped_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-scraped_at')[:50]
    else:
        search_results = []
    
    context = {
        'good_deals': good_deals,
        'trending_categories': trending_categories,
        'search_results': search_results,
        'search_query': search_query,
    }
    
    return render(request, 'alerts/discover_deals.html', context)


@login_required
def alert_preferences(request):
    """
    Manage alert notification preferences
    """
    if request.method == 'POST':
        # Update user preferences
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None
        
        if user_profile:
            user_profile.email_alerts = request.POST.get('email_alerts') == 'on'
            user_profile.sms_alerts = request.POST.get('sms_alerts') == 'on'
            user_profile.push_alerts = request.POST.get('push_alerts') == 'on'
            user_profile.phone_number = request.POST.get('phone_number', '')
            user_profile.save()
            
            messages.success(request, 'Preferences updated successfully')
        
        return redirect('alerts:preferences')
    
    context = {
        'user_profile': getattr(request.user, 'profile', None),
    }
    
    return render(request, 'alerts/preferences.html', context)


# Helper functions

def calculate_user_savings(user):
    """
    Calculate total savings from alerts this month
    """
    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get triggered alerts this month
    triggered_alerts = PriceAlert.objects.filter(
        user=user,
        status='triggered',
        last_triggered__gte=start_of_month
    )
    
    total_savings = 0
    for alert in triggered_alerts:
        if alert.product and alert.target_price:
            # Estimate savings based on target vs current price
            potential_savings = float(alert.product.price) - float(alert.target_price)
            if potential_savings > 0:
                total_savings += potential_savings
    
    return total_savings


def get_trending_categories():
    """
    Get trending product categories based on recent scraping activity
    """
    from products.models import Category
    from django.db.models import Count
    
    trending = ScrapedProduct.objects.filter(
        scraped_at__gte=timezone.now() - timedelta(days=7),
        imported_product__category__isnull=False
    ).values(
        'imported_product__category__name'
    ).annotate(
        product_count=Count('id')
    ).order_by('-product_count')[:10]
    
    return trending


# API endpoints for AJAX requests

@login_required
def api_alert_count(request):
    """
    API endpoint to get user's alert counts
    """
    counts = {
        'total': PriceAlert.objects.filter(user=request.user).count(),
        'active': PriceAlert.objects.filter(user=request.user, status='active').count(),
        'triggered': PriceAlert.objects.filter(user=request.user, status='triggered').count(),
    }
    
    return JsonResponse(counts)


@login_required
def api_recent_deals(request):
    """
    API endpoint to get recent deals
    """
    limit = min(int(request.GET.get('limit', 10)), 50)
    
    deals = ScrapedProduct.objects.filter(
        scraped_at__gte=timezone.now() - timedelta(hours=24),
        is_processed=True,
        imported_product__isnull=False
    ).exclude(
        original_price__isnull=True
    ).order_by('-scraped_at')[:limit]
    
    deals_data = []
    for deal in deals:
        if deal.discount_percentage >= 10:  # Only include meaningful discounts
            deals_data.append({
                'id': deal.id,
                'title': deal.title,
                'price': float(deal.price),
                'original_price': float(deal.original_price) if deal.original_price else None,
                'discount_percentage': deal.discount_percentage,
                'image_url': deal.image_url,
                'product_url': deal.product_url,
                'scraped_at': deal.scraped_at.isoformat(),
            })
    
    return JsonResponse({'deals': deals_data})


@login_required
def api_create_quick_alert(request):
    """
    API endpoint for quickly creating alerts
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})
    
    try:
        product_id = request.POST.get('product_id')
        alert_type = request.POST.get('alert_type', 'below')
        target_price = request.POST.get('target_price')
        
        if not product_id or not target_price:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        product = Product.objects.get(id=product_id)
        
        # Check if user already has an alert for this product
        existing_alert = PriceAlert.objects.filter(
            user=request.user,
            product=product,
            status='active'
        ).first()
        
        if existing_alert:
            return JsonResponse({
                'success': False, 
                'error': 'You already have an active alert for this product'
            })
        
        # Create the alert
        alert = PriceAlert.objects.create(
            user=request.user,
            product=product,
            alert_type=alert_type,
            target_price=target_price,
            status='active'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Alert created successfully',
            'alert_id': alert.id
        })
    
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
