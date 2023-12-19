from django.contrib.auth import get_user_model
from rest_framework import serializers
import datetime
from tours.models import Tour
from users.apis.v1.serializers import UserSerializer
from properties.apis.v1.serializers import PropertySerializer


class TourSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Tour
        fields = ['tour_id', 'user_id', 'property_id', 'scheduled_date', 'scheduled_time', 'message', 'property', 'user']

    def validate(self, data):
        # Perform custom validation for the serializer fields
        # Add your validation logic here
        if data['scheduled_date'] < datetime.date.today():
            raise serializers.ValidationError("Scheduled date must be in the future.")
        
        return data
        
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         validated_data["email"],
    #         validated_data["password"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data["last_name"],
    #     )
    #     return user


class PropertyToursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['tour_id', 'property_id', 'scheduled_date', 'scheduled_time']