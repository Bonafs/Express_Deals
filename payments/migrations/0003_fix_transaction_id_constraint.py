# Generated by Django 5.1.4 on 2025-07-18 13:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_total_amount_order_subtotal_and_more'),
        ('payments', '0002_stripewebhookevent_remove_payment_stripe_charge_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('amex', 'American Express'), ('discover', 'Discover')], max_length=20)),
                ('card_number', models.CharField(max_length=19)),
                ('card_holder_name', models.CharField(max_length=100)),
                ('expiry_month', models.CharField(max_length=2)),
                ('expiry_year', models.CharField(max_length=4)),
                ('cvv', models.CharField(max_length=4)),
                ('scenario', models.CharField(help_text="e.g., 'Success', 'Declined', 'Insufficient Funds'", max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['card_type', 'scenario'],
            },
        ),
        migrations.RemoveField(
            model_name='payment',
            name='stripe_payment_method_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('one_time', 'One-time Payment'), ('subscription', 'Subscription Payment'), ('recurring', 'Recurring Payment')], default='one_time', max_length=20),
        ),
        migrations.AddField(
            model_name='stripewebhookevent',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='GBP', max_length=3),
        ),
        migrations.AlterField(
            model_name='payment',
            name='gateway_response',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('succeeded', 'Succeeded'), ('failed', 'Failed'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_payment_intent_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='stripewebhookevent',
            name='event_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stripewebhookevent',
            name='stripe_event_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('paypal', 'PayPal'), ('stripe', 'Stripe')], max_length=20)),
                ('card_number', models.CharField(blank=True, max_length=19)),
                ('card_holder_name', models.CharField(blank=True, max_length=100)),
                ('expiry_month', models.CharField(blank=True, max_length=2)),
                ('expiry_year', models.CharField(blank=True, max_length=4)),
                ('cvv', models.CharField(blank=True, max_length=4)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=100)),
                ('stripe_payment_method_id', models.CharField(blank=True, max_length=100)),
                ('is_demo', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_default', '-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.paymentmethod'),
        ),
        migrations.CreateModel(
            name='RecurringPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='GBP', max_length=3)),
                ('frequency', models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], max_length=20)),
                ('start_date', models.DateTimeField()),
                ('next_payment_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default='active', max_length=20)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurring_payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium'), ('vip', 'VIP')], max_length=20)),
                ('billing_period_start', models.DateTimeField()),
                ('billing_period_end', models.DateTimeField()),
                ('max_alerts', models.IntegerField(default=0)),
                ('max_wishlists', models.IntegerField(default=0)),
                ('priority_support', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_details', to='payments.payment')),
                ('recurring_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.recurringpayment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Refund',
        ),
    ]
