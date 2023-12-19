from rest_framework import serializers
from properties.models import Property
from real_estate_backend import settings
from botocore.exceptions import NoCredentialsError
from rest_framework.fields import ListField
import boto3
import uuid

class PropertySerializer(serializers.ModelSerializer):
    property_status = serializers.CharField(required=False, allow_blank=True, default='idle')
    price = serializers.DecimalField(required=False, default=20.00, max_digits=18, decimal_places=2)
    images = ListField(child=serializers.ImageField(), required=False)  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property_status'].required = False
        self.fields['price'].required = False
    class Meta:
        model = Property
        fields = (
            'property_id',
            'user',
            'title',
            'property_status',
            'description',
            'price',
            'beds',
            'baths',
            'types',
            'interior_size',
            'exterior_size',
            'size_unit',
            'total',
            'location',
            'longitude',
            'latitude',
            'feature',
            'images',
            'created_at'
        )
        read_only_fields = ('property_id', 'user')
        price = serializers.DecimalField(decimal_places=2, max_digits=18, coerce_to_string= False)
        total = serializers.DecimalField(decimal_places=2, max_digits=10, coerce_to_string= False)

    def create(self, validated_data):
        print('create')
        longitude = validated_data.get('longitude')
        latitude = validated_data.get('latitude')

        if longitude is None:
            raise serializers.ValidationError("longitude is a required field.")
        if latitude is None:
            raise serializers.ValidationError("latitude is a required field.")
        
        property = Property.objects.create(
            baths=validated_data['baths'],
            beds=validated_data['beds'],
            description=validated_data['description'],
            feature=validated_data['feature'],
            latitude=validated_data['latitude'],
            location=validated_data['location'],
            longitude=validated_data['longitude'],
            interior_size=validated_data['interior_size'],
            exterior_size=validated_data['exterior_size'],
            title=validated_data['title'],
            types=validated_data['types'],
            user=self.context['request'].user,
            property_status = validated_data['property_status'],
            price = validated_data['price'],
        )
        return property

    def update(self, instance):
        print('yooo boyesss')
        images = self.context['request'].FILES
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
                    print(url)
                    image_urls.append(url)

                instance.images = image_urls
                print(instance.__dict__)
            except NoCredentialsError as err:
                print('im here')
                pass

        
        
        instance.save()
        return instance
    
    def validate_images(self, value):
        print(value)

    def validate_interior_size(self, value):
        if value < 0:
            raise serializers.ValidationError("interior_size cannot be negative.")
        return value
    
    def validate_exterior_size(self, value):
        if value < 0:
            raise serializers.ValidationError("exterior_size cannot be negative.")
        return value

    def validate_price(self, value):
        print('here')
        if not value:
            value = 20000.00
        elif value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_property_status(self, value):
        if not value:
            value = "idle"
        return value

    def validate_beds(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of beds cannot be negative.")
        return value

    def validate_baths(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of baths cannot be negative.")
        return value

    def validate_images(self, value):
        print('im reallu here S')