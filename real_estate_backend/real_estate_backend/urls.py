from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include('users.apis.v1.urls')),
    path('admin/', admin.site.urls),
]
