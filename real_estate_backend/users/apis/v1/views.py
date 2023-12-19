from rest_framework import generics
from http.client import METHOD_NOT_ALLOWED
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from tours.func import send_email_to_user
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User
import uuid
from real_estate_backend import settings
from botocore.exceptions import NoCredentialsError
import boto3


from .serializers import (
    UserSignUpSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    EditUserSerializer
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

class UserEditProfileView(UpdateAPIView):
    serializer_class = EditUserSerializer

    http_method_names = ['put', 'patch']
    lookup_field = 'id'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['id'])
        image = self.request.FILES

        image_urls = []

        if image:
            try:
                s3 = boto3.client(
                    service_name='s3',
                    region_name=settings.AWS_S3_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                for key, value in image.items():
                    unique_filename = f"{uuid.uuid4().hex}.{key}"
                    s3.upload_fileobj(value, settings.AWS_PROFILE_IMAGE_BUCKET_NAME, unique_filename)
                    url = f"https://{settings.AWS_S3_USER_CUSTOM_DOMAIN}/{unique_filename}"
                    image_urls.append(url)

            except NoCredentialsError as err:
                return Response({"message": "Invalid AWS credentials"}, status=401)
        if image_urls:
            user.image = image_urls
            user.save()

        user = User.objects.filter(pk=self.kwargs['id'])
        return user



    def get_authenticators(self):
        if self.request and (self.request.method == 'PUT' or self.request.method == 'PATCH'):
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and (self.request.method == 'PUT' or self.request.method == 'PATCH'):
            return [IsAuthenticated()]
        return []


class UserChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put', 'get']

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

    def patch(self, request, *args, **kwargs):
        raise METHOD_NOT_ALLOWED(request.method)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        data = {
            'access_token': response.data['access'],
            'refresh_token': response.data['refresh'],
            'user': {
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }
        response.data = data
        return response



class GoogleSignInView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Get the token from the frontend
        token = request.data.get('token')
        CLIENT_ID = '730656096422-ci4m83co5jgpca0lndhj7oc2btaaehk0.apps.googleusercontent.com'

        # Verify the token with Google
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            if idinfo['aud'] not in [CLIENT_ID]:
                raise ValueError('Invalid token')

            # Get the user details
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo['name']
            firstName = idinfo['given_name']
            lastName = idinfo['family_name']
            password=f"abc{google_id}xyz"
            
            if not email or not name:
                return Response({"Email and name is required"}, status=400)

            # Check if the user already exists in Django
            user = get_user_model().objects.filter(email=email).first()
            if not user:
                serializer = UserSignUpSerializer
                serializer = serializer(data={"email":email, "first_name":firstName, "last_name":lastName, "password":password})
                
                serializer.is_valid(raise_exception=True)
                serializer.save()

            
            request.data['email'] = email            
            request.data['password'] = password
            response = super().post(request, *args, **kwargs)
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.user

            data = {
                'access_token': response.data['access'],
                'refresh_token': response.data['refresh'],
                'user': {
                    'user_id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }
            response.data = data
            return response
        except ValueError as err:
            # Handle invalid token
            return Response({"message": str(err)}, status=400)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token") or ''
        uid = request.GET.get("uid") or ''
        try:
            if not token or not uid:
                return Response({"message": "Unauthorized request"}, status=400)
            user_id = urlsafe_base64_decode(uid).decode('utf-8')
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"status": False}, status=400)

        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            return Response({"status": True}, status=200)
        return Response({"status": False}, status=400)



    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({"message": "Email is required"}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            done = send_email_to_user(recepient_email=user.email, link=f"https://https://casa-colombia-two.vercel.app/reset-password?{uid}&{token}")
            if done['status']:
                return Response({"message": "Email sent successfully", "token": token}, status=200)
        return Response({"message": "Email is not registered"}, status=401)
            


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token):
        
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None
        
        if user and PasswordResetTokenGenerator().check_token(user, token):
            new_password = request.data.get('new_password')
            try:
                if not new_password:
                    return Response({"message": "Password is required"}, status=400)

                user.set_password(new_password)
                user.save()
                return Response({"message": "Password Updated"}, status=200)
            except Exception as exc:
                return Response({"message": str(exc)}, status=401)
        return Response({"message": "Unauthorized access"}, status=401)