# Generated by Django 5.1.4 on 2025-07-18 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_fix_duplicate_transaction_ids'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='completed_at',
        ),
    ]
