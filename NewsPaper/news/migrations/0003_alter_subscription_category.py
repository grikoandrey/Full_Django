# Generated by Django 5.0.1 on 2024-02-19 19:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='news.category'),
        ),
    ]