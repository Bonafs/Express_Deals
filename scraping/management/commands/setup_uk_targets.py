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
            # Major UK Electronics Retailers
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
                'name': 'AO.com Electronics',
                'site_type': 'ao',
                'base_url': 'https://www.ao.com',
                'search_url_template': 'https://www.ao.com/search?search={query}&page={page}',
                'category': electronics,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Very Electronics',
                'site_type': 'very',
                'base_url': 'https://www.very.co.uk',
                'search_url_template': 'https://www.very.co.uk/search/{query}?page={page}',
                'category': electronics,
                'product_selector': '.product-item',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            
            # Major UK Fashion Retailers
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
                'name': 'Marks & Spencer',
                'site_type': 'marks_spencer',
                'base_url': 'https://www.marksandspencer.com',
                'search_url_template': 'https://www.marksandspencer.com/search?q={query}&page={page}',
                'category': clothing,
                'product_selector': '.product-item',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Zara UK',
                'site_type': 'zara_uk',
                'base_url': 'https://www.zara.com/uk',
                'search_url_template': 'https://www.zara.com/uk/en/search?searchTerm={query}&page={page}',
                'category': clothing,
                'product_selector': '.product-item',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'H&M UK',
                'site_type': 'h_and_m_uk',
                'base_url': 'https://www2.hm.com/en_gb',
                'search_url_template': 'https://www2.hm.com/en_gb/search-results.html?q={query}&page={page}',
                'category': clothing,
                'product_selector': '.product-item',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Uniqlo UK',
                'site_type': 'uniqlo_uk',
                'base_url': 'https://www.uniqlo.com/uk',
                'search_url_template': 'https://www.uniqlo.com/uk/en/search/?q={query}&page={page}',
                'category': clothing,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'TK Maxx',
                'site_type': 'tk_maxx',
                'base_url': 'https://www.tkmaxx.com',
                'search_url_template': 'https://www.tkmaxx.com/uk/en/search/{query}?page={page}',
                'category': clothing,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            
            # Sports & Fitness Retailers
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
                'name': 'Size? UK',
                'site_type': 'size',
                'base_url': 'https://www.size.co.uk',
                'search_url_template': 'https://www.size.co.uk/search/{query}/?page={page}',
                'category': sports_fitness,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Foot Locker UK',
                'site_type': 'footlocker_uk',
                'base_url': 'https://www.footlocker.co.uk',
                'search_url_template': 'https://www.footlocker.co.uk/en/search/{query}?page={page}',
                'category': sports_fitness,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            
            # Home & Garden Retailers
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
            },
            {
                'name': 'B&Q Home',
                'site_type': 'b_and_q',
                'base_url': 'https://www.diy.com',
                'search_url_template': 'https://www.diy.com/search?term={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Homebase',
                'site_type': 'homebase',
                'base_url': 'https://www.homebase.co.uk',
                'search_url_template': 'https://www.homebase.co.uk/search?q={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Dunelm Home',
                'site_type': 'dunelm',
                'base_url': 'https://www.dunelm.com',
                'search_url_template': 'https://www.dunelm.com/search?q={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'The Range',
                'site_type': 'the_range',
                'base_url': 'https://www.therange.co.uk',
                'search_url_template': 'https://www.therange.co.uk/search?q={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Wickes',
                'site_type': 'wickes',
                'base_url': 'https://www.wickes.co.uk',
                'search_url_template': 'https://www.wickes.co.uk/search?term={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Screwfix',
                'site_type': 'screwfix',
                'base_url': 'https://www.screwfix.com',
                'search_url_template': 'https://www.screwfix.com/search?search={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
                'rating_selector': '.rating',
            },
            {
                'name': 'Toolstation',
                'site_type': 'toolstation',
                'base_url': 'https://www.toolstation.com',
                'search_url_template': 'https://www.toolstation.com/search?q={query}&page={page}',
                'category': home_garden,
                'product_selector': '.product-tile',
                'title_selector': '.product-title',
                'price_selector': '.price',
                'image_selector': '.product-image img',
                'url_selector': '.product-link',
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
