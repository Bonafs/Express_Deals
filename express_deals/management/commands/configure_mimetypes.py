"""
Management command to configure MIME types for static files
"""
from django.core.management.base import BaseCommand
import mimetypes


class Command(BaseCommand):
    help = 'Configure MIME types for static files'

    def handle(self, *args, **options):
        """Configure MIME types for proper static file serving"""
        mimetypes.add_type("text/css", ".css", True)
        mimetypes.add_type("application/javascript", ".js", True)
        mimetypes.add_type("image/svg+xml", ".svg", True)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully configured MIME types')
        )
