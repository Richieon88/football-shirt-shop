# Generated by Django 4.2.7 on 2024-10-29 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shirts", "0005_alter_shirt_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shirt",
            name="season",
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name="shirt",
            name="team",
            field=models.CharField(max_length=50),
        ),
    ]
