"""
Express Deals - Scraping Admin Interface
Django admin configuration for managing scraping targets and monitoring
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import (
    ScrapeTarget, ScrapeJob, ScrapedProduct, 
    PriceAlert, AlertNotification
)


@admin.register(ScrapeTarget)
class ScrapeTargetAdmin(admin.ModelAdmin):
    """
    Admin interface for managing scraping targets
    """
    list_display = [
        'name', 'site_type', 'status', 'category', 
        'scrape_frequency_hours', 'last_scraped', 
        'products_found_today', 'actions_column'
    ]
    list_filter = ['site_type', 'status', 'category', 'created_at']
    search_fields = ['name', 'base_url', 'search_url_template']
    readonly_fields = ['created_at', 'updated_at', 'last_scraped']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'site_type', 'base_url', 'category', 'status')
        }),
        ('Scraping Configuration', {
            'fields': (
                'search_url_template', 'scrape_frequency_hours', 
                'max_pages', 'min_price', 'max_price'
            )
        }),
        ('CSS Selectors', {
            'fields': (
                'product_selector', 'title_selector', 'price_selector',
                'image_selector', 'url_selector', 'rating_selector'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_scraped'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['start_scraping', 'activate_targets', 'deactivate_targets']
    
    def products_found_today(self, obj):
        """Show number of products found today"""
        today = timezone.now().date()
        count = ScrapedProduct.objects.filter(
            job__target=obj,
            scraped_at__date=today
        ).count()
        return count
    products_found_today.short_description = 'Today\'s Products'
    
    def actions_column(self, obj):
        """Action buttons for each target"""
        scrape_url = reverse('admin:scraping_scrape_target', args=[obj.pk])
        view_jobs_url = reverse('admin:scraping_scrapejob_changelist') + f'?target__id__exact={obj.pk}'
        
        return format_html(
            '<a class="button" href="{}">Scrape Now</a> '
            '<a class="button" href="{}">View Jobs</a>',
            scrape_url, view_jobs_url
        )
    actions_column.short_description = 'Actions'
    
    def start_scraping(self, request, queryset):
        """Admin action to start scraping selected targets"""
        from .tasks import scrape_target_task
        
        started_count = 0
        for target in queryset.filter(status='active'):
            try:
                scrape_target_task.delay(target.id)
                started_count += 1
            except Exception as e:
                messages.error(request, f"Failed to start scraping for {target.name}: {e}")
        
        if started_count > 0:
            messages.success(request, f"Started scraping for {started_count} targets")
    
    start_scraping.short_description = "Start scraping selected targets"
    
    def activate_targets(self, request, queryset):
        """Activate selected targets"""
        updated = queryset.update(status='active')
        messages.success(request, f"Activated {updated} targets")
    
    activate_targets.short_description = "Activate selected targets"
    
    def deactivate_targets(self, request, queryset):
        """Deactivate selected targets"""
        updated = queryset.update(status='disabled')
        messages.success(request, f"Deactivated {updated} targets")
    
    deactivate_targets.short_description = "Deactivate selected targets"


@admin.register(ScrapeJob)
class ScrapeJobAdmin(admin.ModelAdmin):
    """
    Admin interface for monitoring scraping jobs
    """
    list_display = [
        'id', 'target', 'status', 'search_query',
        'products_found', 'products_imported', 
        'started_at', 'execution_time', 'actions_column'
    ]
    list_filter = ['status', 'target__site_type', 'started_at']
    search_fields = ['target__name', 'search_query', 'error_message']
    readonly_fields = [
        'started_at', 'completed_at', 'execution_time_seconds',
        'products_found', 'products_imported'
    ]
    
    def execution_time(self, obj):
        """Show execution time in readable format"""
        if obj.execution_time_seconds:
            minutes, seconds = divmod(obj.execution_time_seconds, 60)
            return f"{int(minutes)}m {int(seconds)}s"
        return "-"
    execution_time.short_description = 'Duration'
    
    def actions_column(self, obj):
        """Action buttons for each job"""
        view_products_url = reverse('admin:scraping_scrapedproduct_changelist') + f'?job__id__exact={obj.pk}'
        
        buttons = [f'<a class="button" href="{view_products_url}">View Products</a>']
        
        if obj.status == 'failed' and obj.error_message:
            buttons.append(f'<span title="{obj.error_message}" style="color: red;">❌ Error</span>')
        
        return format_html(' '.join(buttons))
    actions_column.short_description = 'Actions'


@admin.register(ScrapedProduct)
class ScrapedProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing scraped products
    """
    list_display = [
        'title_truncated', 'price', 'discount_percentage',
        'job_target', 'is_processed', 'imported_product_link',
        'scraped_at', 'actions_column'
    ]
    list_filter = [
        'is_processed', 'job__target__site_type', 
        'job__status', 'scraped_at'
    ]
    search_fields = ['title', 'brand', 'external_id']
    readonly_fields = ['scraped_at', 'discount_percentage']
    
    actions = ['import_to_catalog', 'mark_as_processed']
    
    def title_truncated(self, obj):
        """Show truncated title"""
        return obj.title[:50] + "..." if len(obj.title) > 50 else obj.title
    title_truncated.short_description = 'Title'
    
    def job_target(self, obj):
        """Show job target name"""
        return obj.job.target.name
    job_target.short_description = 'Source'
    
    def imported_product_link(self, obj):
        """Link to imported product if exists"""
        if obj.imported_product:
            url = reverse('admin:products_product_change', args=[obj.imported_product.pk])
            return format_html('<a href="{}">View Product</a>', url)
        return "-"
    imported_product_link.short_description = 'Imported Product'
    
    def actions_column(self, obj):
        """Action buttons for each scraped product"""
        buttons = []
        
        if obj.product_url:
            buttons.append(f'<a href="{obj.product_url}" target="_blank">🔗 Source</a>')
        
        if obj.image_url:
            buttons.append(f'<a href="{obj.image_url}" target="_blank">🖼️ Image</a>')
        
        return format_html(' '.join(buttons))
    actions_column.short_description = 'Links'
    
    def import_to_catalog(self, request, queryset):
        """Import selected products to catalog"""
        from .scrapers import ProductScraper
        
        scraper = ProductScraper()
        imported_count = 0
        
        for scraped_product in queryset.filter(is_processed=False):
            if scraper.import_to_catalog(scraped_product):
                imported_count += 1
        
        messages.success(request, f"Imported {imported_count} products to catalog")
    
    import_to_catalog.short_description = "Import selected products to catalog"
    
    def mark_as_processed(self, request, queryset):
        """Mark selected products as processed"""
        updated = queryset.update(is_processed=True)
        messages.success(request, f"Marked {updated} products as processed")
    
    mark_as_processed.short_description = "Mark as processed"


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    """
    Admin interface for managing price alerts with URL tracking
    """
    list_display = [
        'id', 'user', 'product_or_keywords_or_url', 'alert_type',
        'target_price', 'status', 'tracking_effectiveness', 'created_at', 'last_triggered'
    ]
    list_filter = ['alert_type', 'status', 'created_at', 'email_enabled', 'sms_enabled']
    search_fields = [
        'user__username', 'user__email', 'search_keywords', 
        'product__name', 'product_url'
    ]
    readonly_fields = [
        'created_at', 'last_triggered', 'onset_price', 
        'current_price', 'last_price_update', 'url_tracking_info'
    ]
    
    fieldsets = (
        ('User & Target', {
            'fields': ('user', 'product', 'search_keywords', 'product_url')
        }),
        ('Alert Configuration', {
            'fields': ('alert_type', 'target_price', 'percentage_threshold', 'status', 'expires_at')
        }),
        ('Notification Settings', {
            'fields': ('email_enabled', 'sms_enabled', 'push_enabled')
        }),
        ('Price Tracking', {
            'fields': ('onset_price', 'current_price', 'last_price_update'),
            'classes': ('collapse',)
        }),
        ('URL Tracking Info', {
            'fields': ('url_tracking_info',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_triggered'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['test_url_tracking', 'refresh_price_data', 'trigger_test_alert']
    
    def product_or_keywords_or_url(self, obj):
        """Show product name, keywords, or URL"""
        if obj.product:
            return f"Product: {obj.product.name}"
        elif obj.search_keywords:
            return f"Keywords: {obj.search_keywords}"
        elif obj.product_url:
            return f"URL: {obj.product_url[:50]}..."
        return "No target specified"
    product_or_keywords_or_url.short_description = 'Target'
    
    def tracking_effectiveness(self, obj):
        """Show tracking effectiveness for URL-based alerts"""
        if not obj.product_url:
            return '-'
        
        try:
            from .url_tracking_service import url_tracking_service
            score, error = url_tracking_service.get_tracking_effectiveness_score(obj.product_url)
            
            if error:
                return format_html('<span style="color: red;">Error</span>')
            
            if score >= 80:
                color = 'green'
                icon = '✅'
            elif score >= 60:
                color = 'orange'
                icon = '⚠️'
            else:
                color = 'red'
                icon = '❌'
            
            return format_html(
                '<span style="color: {};">{} {}%</span>',
                color, icon, score
            )
        except Exception:
            return format_html('<span style="color: red;">Error</span>')
    tracking_effectiveness.short_description = 'URL Tracking'
    
    def url_tracking_info(self, obj):
        """Display comprehensive URL tracking information"""
        if not obj.product_url:
            return format_html('<em>No URL specified</em>')
        
        try:
            from .url_tracking_service import url_tracking_service
            tracking_info = url_tracking_service.get_url_tracking_info(obj.product_url)
            
            if 'error' in tracking_info:
                return format_html(
                    '<div style="color: red;">❌ Error: {}</div>',
                    tracking_info['error']
                )
            
            effectiveness = tracking_info['effectiveness']
            availability = tracking_info['availability']
            validation = tracking_info['validation']
            
            # Build HTML display
            html_parts = []
            
            # Validation section
            if validation['is_valid']:
                html_parts.append(f"✅ <strong>Retailer:</strong> {validation['retailer']}")
            else:
                html_parts.append(f"❌ <strong>Validation:</strong> {validation['message']}")
            
            # Effectiveness section
            score = effectiveness['score']
            score_color = 'green' if score >= 80 else 'orange' if score >= 60 else 'red'
            html_parts.append(f"📊 <strong>Tracking Score:</strong> <span style='color: {score_color}'>{score}/100</span>")
            
            # Availability section
            if availability['available']:
                response_time = availability.get('response_time', 0)
                html_parts.append(f"🌐 <strong>Available:</strong> ✅ ({response_time:.1f}s response)")
                
                if availability.get('title'):
                    html_parts.append(f"📝 <strong>Product:</strong> {availability['title'][:50]}...")
                
                if availability.get('price'):
                    html_parts.append(f"💰 <strong>Current Price:</strong> {availability['price']}")
            else:
                html_parts.append(f"🌐 <strong>Availability:</strong> ❌ {availability.get('error', 'Unknown error')}")
            
            # Factors section
            if effectiveness['factors']:
                factors_html = '<br>'.join([f"• {factor}" for factor in effectiveness['factors'][:3]])
                html_parts.append(f"<details><summary><strong>Factors</strong></summary>{factors_html}</details>")
            
            # URL link
            html_parts.append(f'<a href="{obj.product_url}" target="_blank" class="button">🔗 Open URL</a>')
            
            return format_html('<div style="line-height: 1.4;">{}</div>', '<br>'.join(html_parts))
            
        except Exception as e:
            return format_html(
                '<div style="color: red;">❌ Error loading tracking info: {}</div>',
                str(e)
            )
    
    url_tracking_info.short_description = 'URL Tracking Information'
    
    def test_url_tracking(self, request, queryset):
        """Admin action to test URL tracking for selected alerts"""
        from .url_tracking_service import url_tracking_service
        
        tested_count = 0
        error_count = 0
        
        for alert in queryset.filter(product_url__isnull=False).exclude(product_url=''):
            try:
                availability = url_tracking_service.check_product_availability(alert.product_url)
                if availability['available'] and availability['price']:
                    alert.current_price = availability['price']
                    alert.last_price_update = timezone.now()
                    alert.save()
                    tested_count += 1
                else:
                    error_count += 1
            except Exception:
                error_count += 1
        
        if tested_count > 0:
            self.message_user(
                request,
                f"Successfully tested {tested_count} URL alert(s). {error_count} error(s).",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"No URL alerts could be tested. {error_count} error(s).",
                messages.WARNING
            )
    test_url_tracking.short_description = "Test URL tracking for selected alerts"
    
    def refresh_price_data(self, request, queryset):
        """Admin action to refresh price data for URL alerts"""
        updated_count = 0
        
        for alert in queryset.filter(product_url__isnull=False).exclude(product_url=''):
            try:
                from .url_tracking_service import url_tracking_service
                availability = url_tracking_service.check_product_availability(alert.product_url)
                
                if availability['available'] and availability['price']:
                    old_price = alert.current_price
                    alert.current_price = availability['price']
                    alert.last_price_update = timezone.now()
                    
                    # Set onset price if not set
                    if not alert.onset_price:
                        alert.onset_price = availability['price']
                    
                    alert.save()
                    updated_count += 1
            except Exception:
                pass
        
        self.message_user(
            request,
            f"Refreshed price data for {updated_count} alert(s).",
            messages.SUCCESS if updated_count > 0 else messages.WARNING
        )
    refresh_price_data.short_description = "Refresh price data for selected alerts"


@admin.register(AlertNotification)
class AlertNotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for monitoring alert notifications
    """
    list_display = [
        'id', 'alert_user', 'channel', 'status',
        'recipient', 'sent_at', 'delivered_at'
    ]
    list_filter = ['channel', 'status', 'sent_at']
    search_fields = ['recipient', 'message', 'alert__user__username']
    readonly_fields = ['sent_at', 'delivered_at']
    
    def alert_user(self, obj):
        """Show alert user"""
        return obj.alert.user.username
    alert_user.short_description = 'User'


# Custom admin views
from django.urls import path
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

class ScrapingAdminMixin:
    """
    Mixin to add custom admin URLs for scraping actions
    """
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:target_id>/scrape/',
                self.admin_site.admin_view(self.scrape_target_view),
                name='scraping_scrape_target',
            ),
        ]
        return custom_urls + urls
    
    def scrape_target_view(self, request, target_id):
        """
        Custom admin view to start scraping a target
        """
        target = get_object_or_404(ScrapeTarget, pk=target_id)
        
        if request.method == 'POST':
            from .tasks import scrape_target_task
            
            try:
                task = scrape_target_task.delay(target_id)
                messages.success(request, f"Started scraping job for {target.name}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f"Started scraping job for {target.name}",
                        'task_id': task.id
                    })
            
            except Exception as e:
                messages.error(request, f"Failed to start scraping: {e}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    })
        
        return HttpResponseRedirect(reverse('admin:scraping_scrapetarget_changelist'))


# Apply the mixin to ScrapeTargetAdmin
ScrapeTargetAdmin.__bases__ = (ScrapingAdminMixin,) + ScrapeTargetAdmin.__bases__
