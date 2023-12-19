from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property

class FavouriteProperty(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'property_id')
