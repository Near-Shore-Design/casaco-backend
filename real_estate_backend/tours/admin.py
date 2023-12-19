from django.contrib import admin
from .models import Tour

class TourAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'property_id', 'created_at', 'scheduled_date', 'scheduled_time']

admin.site.register(Tour, TourAdmin)
