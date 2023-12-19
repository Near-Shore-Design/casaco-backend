from django.urls import path
from favouriteproperties.apis.v1 import views

app_name = 'favouriteproperties'

urlpatterns = [
    path('property/<int:property_id>/', views.PropertyFavouriteUsersView.as_view(), name='favourite_users'),
    path('user/<int:user_id>/', views.PropertyFavouritePropertiesView.as_view(), name='favourite_properties'),
    path('update', views.CreateDestroyFavouritePropertyView.as_view(), name='create_or_delete_favourite_property'),
]
