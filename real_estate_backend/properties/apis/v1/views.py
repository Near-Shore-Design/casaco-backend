from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from properties.models import Property
from .serializers import PropertySerializer
import uuid
from real_estate_backend import settings
from botocore.exceptions import NoCredentialsError
import boto3


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        'property_status': ['exact'],
        'types': ['in'],
        'price': ['exact', 'lt', 'gt'],
        'interior_size': ['exact', 'lt', 'gt'],
        'exterior_size': ['exact', 'lt', 'gt'],
        'beds': ['exact', 'lt', 'gt'],
        'baths': ['exact', 'lt', 'gt'],
        'location': ['in'],
    }
    ordering_fields = ['price', 'beds', 'baths']
    search_fields = ['title', 'description']

    pagination_class = LargeResultsSetPagination

    def get_authenticators(self):
        if self.request and self.request.method == 'POST':
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        features = self.request.query_params.get('feature__contains')
        if features:
            features = features.split(',')
            queryset = queryset.filter(feature__contains=features)
        
        queryset = queryset.order_by('-created_at')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # Handle image uploads
        property_instance = serializer.instance
        images = self.request.FILES
        if images:
            try:
                s3 = boto3.client(
                    service_name='s3',
                    region_name=settings.AWS_S3_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                image_urls = []
                for key, value in images.items():
                    unique_filename = f"{uuid.uuid4().hex}.{key}"
                    s3.upload_fileobj(value, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
                    url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
                    image_urls.append(url)
    
                property_instance.images = image_urls
                property_instance.save()
            except NoCredentialsError as err:
                pass


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    # http_method_names = ['get', 'put', 'delete']
    lookup_field = 'property_id'

    def get_authenticators(self):
        if self.request and (self.request.method == 'PUT' or self.request.method == 'DELETE'):
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and (self.request.method == 'PUT' or self.request.method == 'DELETE'):
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        features = self.request.query_params.get('feature__contains')
        if features:
            features = features.split(',')
            queryset = queryset.filter(feature__contains=features)
        
        queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def perform_update(self, serializer):
        instance = serializer.instance
        updated_instance = serializer.update(instance, serializer.validated_data)
        return updated_instance
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
