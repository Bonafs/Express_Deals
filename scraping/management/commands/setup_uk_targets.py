from django.core.management.base import BaseCommand
from scraping.models import ScrapeTarget
from products.models import Category


class Command(BaseCommand):
    help = 'Create UK retail scraping targets for major British online stores.'

    def handle(self, *args, **options):
        """
        Create scraping targets for major UK retailers
        """
        
        # Get or create categories
        electronics, _ = Category.objects.get_or_create(name='Electronics')
        clothing, _ = Category.objects.get_or_create(name='Clothing')
        home_garden, _ = Category.objects.get_or_create(name='Home & Garden')
        sports_fitness, _ = Category.objects.get_or_create(name='Sports & Fitness')
        
        uk_targets = [
            {
                'name': 'Amazon UK Electronics',
                'site_type': 'amazon_uk',
                'base_url': 'https://www.amazon.co.uk',
                'search_url_template': 'https://www.amazon.co.uk/s?k={query}&ref=sr_pg_{page}',
                'category': electronics,
                'product_selector': '[data-component-type="s-search-result"]',
                'title_selector': 'h2 a span',
                'price_selector': '.a-price-whole',
                'image_selector': '.s-image',
                'url_selector': 'h2 a',
                'rating_selector': '.a-icon-alt',
            },
            {
                'name': 'Currys PC World',
                'site_type': 'currys',
                'base_url': 'https://www.currys.co.uk',
                'search_url_template': 'https://www.currys.co.uk/search?q={query}&page={page}',
                'category': electronics,
                'product_selector': '.product-item',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'John Lewis Electronics',
                'site_type': 'john_lewis',
                'base_url': 'https://www.johnlewis.com',
                'search_url_template': 'https://www.johnlewis.com/search?search-term={query}&page={page}',
                'category': electronics,
                'product_selector': '.product-card',
                'title_selector': '.product-card__title',
                'price_selector': '.price',
                'image_selector': '.product-card__image img',
                'url_selector': '.product-card__link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Argos Electronics',
                'site_type': 'argos',
                'base_url': 'https://www.argos.co.uk',
                'search_url_template': 'https://www.argos.co.uk/search/{query}/?page={page}',
                'category': electronics,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Next Fashion',
                'site_type': 'next',
                'base_url': 'https://www.next.co.uk',
                'search_url_template': 'https://www.next.co.uk/search?w={query}&page={page}',
                'category': clothing,
                'product_selector': '.Product',
                'title_selector': '.Title',
                'price_selector': '.Price',
                'image_selector': '.ProductImage img',
                'url_selector': '.Product a',
                'rating_selector': '.Rating',
            },
            {
                'name': 'ASOS Fashion',
                'site_type': 'asos',
                'base_url': 'https://www.asos.com',
                'search_url_template': 'https://www.asos.com/search/?q={query}&page={page}',
                'category': clothing,
                'product_selector': '[data-testid="product-tile"]',
                'title_selector': '[data-testid="product-title"]',
                'price_selector': '[data-testid="current-price"]',
                'image_selector': 'img[data-testid="product-image"]',
                'url_selector': 'a[data-testid="product-link"]',
                'rating_selector': '.rating',
            },
            {
                'name': 'JD Sports',
                'site_type': 'jd_sports',
                'base_url': 'https://www.jdsports.co.uk',
                'search_url_template': 'https://www.jdsports.co.uk/search/{query}/?page={page}',
                'category': sports_fitness,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'IKEA UK Home',
                'site_type': 'ikea_uk',
                'base_url': 'https://www.ikea.com/gb/en',
                'search_url_template': 'https://www.ikea.com/gb/en/search/products/?q={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-compact',
                'title_selector': '.product-compact__name',
                'price_selector': '.product-compact__price',
                'image_selector': '.product-compact__image img',
                'url_selector': '.product-compact__link',
                'rating_selector': '.rating',
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for target_data in uk_targets:
            target, created = ScrapeTarget.objects.get_or_create(
                name=target_data['name'],
                defaults=target_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created target: {target.name}')
                )
            else:
                # Update existing target
                for key, value in target_data.items():
                    setattr(target, key, value)
                target.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated target: {target.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\\nUK Scraping targets setup completed:\\n'
                f'- Created: {created_count}\\n'
                f'- Updated: {updated_count}\\n'
                f'- Total UK targets: {ScrapeTarget.objects.count()}'
            )
        )
