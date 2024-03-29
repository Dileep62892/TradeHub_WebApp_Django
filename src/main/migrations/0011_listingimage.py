# Generated by Django 5.0 on 2024-02-15 10:26

import django.db.models.deletion
import main.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_listing_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.utils.user_listings_path)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.listing')),
            ],
        ),
    ]
