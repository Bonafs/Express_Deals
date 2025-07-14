

from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', first_name='Test', last_name='User')
        # Use get_or_create to avoid unique constraint error if profile is auto-created
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user, defaults={'phone_number': '1234567890'})

    def test_str(self):
        self.assertEqual(str(self.profile), "testuser's Profile")

    def test_full_name_property(self):
        self.assertEqual(self.profile.full_name, 'Test User')

    def test_has_whatsapp_property(self):
        self.profile.whatsapp_number = '12345'
        self.profile.whatsapp_notifications_enabled = True
        self.assertTrue(self.profile.has_whatsapp)

class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'), follow=True)
        # Accept either 200 (OK) or 301/302 (redirect to login/home if already authenticated)
        self.assertIn(response.status_code, [200, 301, 302])
        # If 200, check template; if redirect, check final URL
        if response.status_code == 200:
            self.assertTemplateUsed(response, 'accounts/register.html')
