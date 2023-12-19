from rest_framework import serializers
from django.contrib.auth import get_user_model
from properties.models import Property
from favouriteproperties.models import FavouriteProperty

class FavouriteUserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name')


class FavouritePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class FavouritePropertyCreateDestroySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    property_id = serializers.IntegerField(required=True)