from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email:
            raise serializers.ValidationError("Email is required.")
        if not password:
            raise serializers.ValidationError("Password is required.")

        return data


class UserSignUpSerializer(UserSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("first_name", "last_name")

    def validate(self, data):
        super().validate(data)
        password = data.get("password")
        email = data.get("email")

        if password:
            validate_password(password)

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'email', 'image']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if not self.context["request"].user.check_password(data["old_password"]):
            raise serializers.ValidationError("Incorrect old password.")

        return data

class ResetPasswordSerializer(serializers.Serializer):
    def validate(self, data):
        return data