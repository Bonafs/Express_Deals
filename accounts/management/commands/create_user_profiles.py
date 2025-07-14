from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from credentials import SAMPLE_USERS


class Command(BaseCommand):
    help = 'Create missing user profiles for authentication fix'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Creating missing user profiles...")
        
        created_count = 0
        
        # Create profile for admin user if missing
        try:
            admin_user = User.objects.get(username='admin')
            profile, created = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'phone_number': '+44 20 7946 0000',
                    'address': 'Admin Office, London, UK'
                }
            )
            if created:
                self.stdout.write(f"✅ Created profile for admin")
                created_count += 1
        except User.DoesNotExist:
            pass
        
        # Create profiles for sample users
        for user_data in SAMPLE_USERS:
            try:
                user = User.objects.get(username=user_data['username'])
                profile_data = user_data.get('profile_data', {})
                
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone_number': profile_data.get('phone', ''),
                        'date_of_birth': profile_data.get('date_of_birth'),
                        'address': profile_data.get('address', ''),
                    }
                )
                
                if created:
                    self.stdout.write(f"✅ Created profile for {user.username}")
                    created_count += 1
                else:
                    self.stdout.write(f"ℹ️  Profile already exists for {user.username}")
                    
            except User.DoesNotExist:
                self.stdout.write(f"❌ User {user_data['username']} not found")
        
        self.stdout.write(f"\n🎉 Created {created_count} new user profiles")
        self.stdout.write("✅ All user profiles are now complete!")
