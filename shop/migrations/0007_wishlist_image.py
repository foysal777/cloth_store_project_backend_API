# Generated by Django 5.0.6 on 2024-07-09 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_rename_product_wishlist_products_alter_review_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='image',
            field=models.ImageField(default='shop/images/p2.png', upload_to='shop/images'),
        ),
    ]
