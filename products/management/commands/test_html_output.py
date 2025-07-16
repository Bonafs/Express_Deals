from django.core.management.base import BaseCommand
from django.test.client import Client


class Command(BaseCommand):
    help = 'Test the actual HTML output of the ProductListView'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Testing ProductListView HTML output..."))

        # Create a test client
        client = Client()
        
        # Get the home page
        response = client.get('/')
        
        self.stdout.write(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.content.decode('utf-8')
            
            # Count products in the main grid
            product_cards = html_content.count('<div class="col-lg-4 col-md-6 col-sm-6 mb-4">')
            self.stdout.write(f"Product cards found in HTML: {product_cards}")
            
            # Check if pagination is rendered
            if 'pagination' in html_content:
                self.stdout.write("✅ Pagination section found in HTML")
                if 'page-item' in html_content:
                    page_items = html_content.count('page-item')
                    self.stdout.write(f"Pagination items found: {page_items}")
                else:
                    self.stdout.write("❌ No pagination items found")
            else:
                self.stdout.write("❌ No pagination section found in HTML")
            
            # Check for featured products
            if 'Featured Products' in html_content:
                self.stdout.write("✅ Featured Products section found")
            else:
                self.stdout.write("❌ Featured Products section not found")
            
            # Check for specific pagination markers
            if 'is_paginated' in html_content:
                self.stdout.write("✅ is_paginated context variable found")
            
            if 'page_obj' in html_content:
                self.stdout.write("✅ page_obj context variable found")
            
            # Check for "Next" and "Previous" links
            if 'Next</a>' in html_content:
                self.stdout.write("✅ Next pagination link found")
            else:
                self.stdout.write("❌ No Next pagination link found")
            
        else:
            self.stdout.write(f"❌ Error: Got status {response.status_code}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("HTML test completed!")
