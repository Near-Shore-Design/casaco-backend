from django.urls import path
from tours.apis.v1 import views

app_name = 'tours'

urlpatterns = [
    path('request-tour', views.RequestTour.as_view(), name='request-tour'),
]
