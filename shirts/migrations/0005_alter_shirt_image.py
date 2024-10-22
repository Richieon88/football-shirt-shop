# Generated by Django 4.2.7 on 2024-10-22 18:49

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shirts', '0004_size_remove_shirt_type_shirtsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
