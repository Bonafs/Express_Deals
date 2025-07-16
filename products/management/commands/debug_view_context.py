from django.core.management.base import BaseCommand
from django.http import HttpRequest
from products.views import ProductListView
from django.test import RequestFactory


class Command(BaseCommand):
    help = 'Debug the ProductListView context and pagination'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Debugging ProductListView context..."))

        # Use Django's test client to create a proper request
        from django.test.client import Client
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.auth.middleware import AuthenticationMiddleware
        
        # Create a mock request with proper middleware
        factory = RequestFactory()
        request = factory.get('/products/')
        
        # Add session and user attributes
        request.user = AnonymousUser()
        
        # Add session
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        
        # Create the view instance
        view = ProductListView()
        view.setup(request)
        
        # Get the queryset and context
        queryset = view.get_queryset()
        self.stdout.write(f"Queryset count: {queryset.count()}")
        
        # Test pagination manually
        view.object_list = queryset
        context = view.get_context_data()
        
        self.stdout.write(f"Products in context: {len(context['products'])}")
        self.stdout.write(f"Featured products: {len(context['featured_products'])}")
        self.stdout.write(f"Is paginated: {context.get('is_paginated', False)}")
        self.stdout.write(f"Page obj exists: {'page_obj' in context}")
        
        if 'page_obj' in context:
            page_obj = context['page_obj']
            self.stdout.write(f"Current page: {page_obj.number}")
            self.stdout.write(f"Total pages: {page_obj.paginator.num_pages}")
            self.stdout.write(f"Has previous: {page_obj.has_previous()}")
            self.stdout.write(f"Has next: {page_obj.has_next()}")
            self.stdout.write(f"Objects on this page: {len(page_obj.object_list)}")
        
        # Check which products are both featured and in main list
        main_products = set(context['products'])
        featured_products = set(context['featured_products'])
        overlap = main_products.intersection(featured_products)
        
        self.stdout.write(f"\nProducts appearing in both main and featured:")
        for product in overlap:
            self.stdout.write(f"  - {product.name}")
        
        self.stdout.write(f"\nOverlap count: {len(overlap)} out of {len(main_products)} main products")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Debug completed!")
