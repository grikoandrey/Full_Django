# Generated by Django 5.0.1 on 2024-02-22 07:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_rename_subscription_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='last_notification_sent',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]