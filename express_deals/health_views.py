"""
Simple health check views for debugging
"""
from django.http import HttpResponse
from django.db import connection
from products.models import Product, Category

def health_check(request):
    """Basic health check"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check models
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        
        return HttpResponse(f"""
        <h1>Health Check</h1>
        <p>Database: ✅ Connected</p>
        <p>Products: {product_count}</p>
        <p>Categories: {category_count}</p>
        <p>Django: ✅ Working</p>
        """, content_type="text/html")
        
    except Exception as e:
        return HttpResponse(f"""
        <h1>Health Check</h1>
        <p>❌ Error: {str(e)}</p>
        """, content_type="text/html", status=500)
