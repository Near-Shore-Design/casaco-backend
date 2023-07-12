from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from .serializers import (
    UserSignUpSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    permission_classes = ()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            "message": "User created successfully.",
            "user": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response_data = {
                "message": "Password updated successfully."
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
