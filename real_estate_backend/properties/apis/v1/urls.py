from django.urls import path
from properties.apis.v1 import views

app_name = 'properties'

urlpatterns = [
    path('', views.PropertyListCreateView.as_view(), name='property_list'),
    path('<int:property_id>/', views.PropertyDetailView.as_view(), name='property_detail'),
]
