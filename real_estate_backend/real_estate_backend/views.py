import boto3
import uuid
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_to_s3(request):
    try:
        files = request.FILES
        s3 = boto3.client(
            service_name='s3',
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        files_urls = []
        for key, value in files.items():
            unique_filename = f"{uuid.uuid4().hex}.{key}"
            s3.upload_fileobj(value, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
            url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
            files_urls.append(url)
        return Response({'files_urls': files_urls}, status=status.HTTP_201_CREATED)
    except NoCredentialsError as err:
        return Response({'error': 'Failed to generate a pre-signed URL for file upload'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)