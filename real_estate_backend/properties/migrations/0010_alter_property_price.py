# Generated by Django 3.2 on 2023-09-24 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_auto_20230703_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.DecimalField(decimal_places=2, default=20000.0, max_digits=18),
        ),
    ]
