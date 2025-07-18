# Generated by Django 5.2.4 on 2025-07-04 03:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='deal_categories',
            field=models.JSONField(blank=True, default=list, help_text='Preferred product categories for deals'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_notifications_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_currency',
            field=models.CharField(default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='price_alert_threshold',
            field=models.DecimalField(decimal_places=0, default=10, help_text='Minimum discount percentage for alerts', max_digits=5),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='push_notifications_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sms_notifications_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default='UTC', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='whatsapp_notifications_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default='United States', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profiles',
        ),
    ]
