from django.contrib import admin
from .models import FavouriteProperty

class FavouritePropertyAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'property_id', 'created_at']
    list_filter = ['user_id', 'property_id']
    search_fields = ['user_id', 'property_id']

admin.site.register(FavouriteProperty, FavouritePropertyAdmin)
