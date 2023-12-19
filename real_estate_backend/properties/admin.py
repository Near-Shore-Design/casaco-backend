from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'title', 'property_status', 'price', 'location']
    list_filter = ['property_status']
    search_fields = ['title', 'description']

admin.site.register(Property, PropertyAdmin)
