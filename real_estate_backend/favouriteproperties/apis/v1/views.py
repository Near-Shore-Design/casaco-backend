from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Subquery, OuterRef, F
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from favouriteproperties.models import FavouriteProperty
from properties.models import Property
import json
from itertools import chain
from .serializers import FavouritePropertySerializer, FavouriteUserSerializer, FavouritePropertyCreateDestroySerializer

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PropertyFavouriteUsersView(generics.ListAPIView):
    serializer_class = FavouriteUserSerializer
    lookup_field = 'property_id'

    def get_queryset(self):
        property_id = self.kwargs['property_id'] or None
        favourite_users = []
        favourite_properties = FavouriteProperty.objects.filter(property_id__property_id=property_id)
        for favourite_property in favourite_properties:
            favourite_users.append(favourite_property.__dict__['user_id_id'] or '')
        queryset = get_user_model().objects.filter(id__in=favourite_users)
        return queryset


class PropertyFavouritePropertiesView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FavouritePropertySerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id'] or None
        favourite_properties = []
        favourite_users = FavouriteProperty.objects.filter(user_id__id=user_id)
        for favourite_user in favourite_users:
            favourite_properties.append(favourite_user.__dict__['property_id_id'] or '')
        queryset = Property.objects.filter(property_id__in=favourite_properties)
        return queryset
    
    def get_authenticators(self):
        if self.request and (self.request.method == 'GET'):
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and  (self.request.method == 'GET'):
            return [IsAuthenticated()]
        return []


class CreateDestroyFavouritePropertyView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FavouritePropertyCreateDestroySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        property_id = serializer.validated_data.get('property_id')

        try:
            favourite_property = FavouriteProperty.objects.get(user_id=user_id, property_id=property_id)
            favourite_property.delete()
            content = {'message': 'Property removed from favourites.'}
            return Response(content, status=200)
        except FavouriteProperty.DoesNotExist:
            user = get_user_model().objects.get(id=user_id)
            property = Property.objects.get(property_id=property_id)
            favourite_property = FavouriteProperty.objects.create(user_id=user, property_id=property)
            favourite_property.save()
            content = {'message': 'Property added to favourites.'}
            return Response(content, status=200)

    def get_authenticators(self):
        if self.request and (self.request.method == 'POST'):
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and  (self.request.method == 'POST'):
            return [IsAuthenticated()]
        return []