# Generated by Django 4.2.7 on 2024-12-22 14:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shirts', '0007_shirt_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='shirt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shirt',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
