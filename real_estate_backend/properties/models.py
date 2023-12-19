from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Property(TimeStampedModel):
    PROPERTY_STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
        ('rented', 'Rented'),
        ('idle', 'Idle'),
    ]
    PROPERTY_TYPE_CHOICES = [
        ('condo', 'Condo'),
        ('studio', 'Studio'),
        ('house', 'House'),
        ('plot', 'Plot'),
        ('mension', 'Mension'),
        ('shop', 'Shop'),
        ('hotel', 'Hotel'),
        ('warehouse', 'Warehouse'),
    ]
    SIZE_UNIT = [
        ('meter', 'm^2'),
        ('hectares', 'hectáreas')
    ]
    property_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    property_status = models.CharField(
        max_length=30, choices=PROPERTY_STATUS_CHOICES, default="idle")
    property_type = models.CharField(
        max_length=30, choices=PROPERTY_TYPE_CHOICES, default='house')
    description = models.TextField()
    price = models.DecimalField(
        max_digits=18, decimal_places=2, default=20000.00)
    images = ArrayField(models.CharField(max_length=200), size=5, null=True)
    beds = models.IntegerField()
    baths = models.IntegerField()
    types = models.CharField(max_length=255)
    interior_size = models.DecimalField(
        max_digits=10, decimal_places=6, max_length=255, default=0)
    exterior_size = models.DecimalField(
        max_digits=10, decimal_places=6, max_length=255, default=0)
    size_unit = models.CharField(
        max_length=10, choices=SIZE_UNIT, default='meter', null=True, blank=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=20000.00)
    location = models.CharField(max_length=255)
    longitude = models.DecimalField(
        max_digits=10, decimal_places=5, default=-72.5039)
    latitude = models.DecimalField(
        max_digits=10, decimal_places=5, default=7.8942)
    feature = ArrayField(models.CharField(max_length=255), size=10, default=[])
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return self.title
