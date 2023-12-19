from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views



urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
    path('upload', views.upload_to_s3, name='upload_to_s3'),
    path('schema/', SpectacularAPIView.as_view() ,name='schema'),
    path('users/', include('users.apis.v1.urls')),
    path('properties/', include('properties.apis.v1.urls')),
    path('favourites/', include('favouriteproperties.apis.v1.urls')),
    path('tours/', include('tours.apis.v1.urls')),
    path('admin/', admin.site.urls),
]
