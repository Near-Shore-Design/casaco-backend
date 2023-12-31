# Generated by Django 3.2 on 2023-06-03 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20230603_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_status',
            field=models.CharField(choices=[('for_sale', 'For Sale'), ('for_rent', 'For Rent'), ('rented', 'Rented')], default='idle', max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('condo', 'Condo'), ('studio', 'Studio'), ('house', 'House'), ('plot', 'Plot'), ('mension', 'Mension'), ('shop', 'Shop'), ('hotel', 'Hotel'), ('warehouse', 'Warehouse')], default='house', max_length=30),
        ),
    ]
