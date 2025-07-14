from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.db import transaction
import sys
import os

# Add the parent directory to the path to import credentials
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

try:
    import credentials
except ImportError:
    try:
        import credentials_template as credentials
    except ImportError:
        credentials = None


class Command(BaseCommand):
    help = 'Create sample users for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip users that already exist',
        )

    def handle(self, *args, **options):
        if not credentials or not hasattr(credentials, 'SAMPLE_USERS'):
            self.stdout.write(
                self.style.ERROR('No credentials file found or SAMPLE_USERS not defined')
            )
            return

        sample_users = credentials.SAMPLE_USERS
        created_count = 0
        skipped_count = 0

        for user_data in sample_users:
            username = user_data['username']
            
            if User.objects.filter(username=username).exists():
                if options['skip_existing']:
                    self.stdout.write(f'User {username} already exists, skipping...')
                    skipped_count += 1
                    continue
                else:
                    self.stdout.write(f'User {username} already exists, updating...')
                    user = User.objects.get(username=username)
            else:
                user = User(username=username)

            # Set user fields
            user.email = user_data['email']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.set_password(user_data['password'])
            
            try:
                with transaction.atomic():
                    user.save()
                    
                    # Create or update profile if profile_data exists
                    if 'profile_data' in user_data:
                        profile, profile_created = UserProfile.objects.get_or_create(user=user)
                        profile_data = user_data['profile_data']
                        
                        if 'phone' in profile_data:
                            profile.phone = profile_data['phone']
                        if 'date_of_birth' in profile_data:
                            profile.date_of_birth = profile_data['date_of_birth']
                        if 'address' in profile_data:
                            profile.address = profile_data['address']
                        
                        profile.save()
                        
                        action = 'Created' if profile_created else 'Updated'
                        self.stdout.write(f'{action} profile for user {username}')
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created/updated user: {username}')
                    )
                    created_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating user {username}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Setup complete! Created/updated {created_count} users, skipped {skipped_count}'
            )
        )
