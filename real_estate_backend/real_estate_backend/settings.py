"""
Django settings for real_estate_backend project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os

from os.path import abspath, basename, dirname, join, normpath
# from sys import path

import environ
from dotenv import load_dotenv


# from utils.oauth2_utils import get_username_from_claim, update_user_details


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6#+pnfd%e$iqx7d0^4bht(to899falixn04-43)ox1&xntn-fk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'users',
    'properties',
    'favouriteproperties',
    'tours',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'real_estate_backend.urls'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'casa.colombia0011@gmail.com'
EMAIL_HOST_PASSWORD = 'emkgwamagfgclgjf'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'casa.colombia0011@gmail.com'

FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


#AWS account credentials
AWS_ACCESS_KEY_ID = 'AKIA2E4HGKGGEAEEPIHB'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'casa-colombia-real-estate'
AWS_PROFILE_IMAGE_BUCKET_NAME='casa-colombia-users-profile-image'
AWS_S3_USER_CUSTOM_DOMAIN = f'{AWS_PROFILE_IMAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_REGION = "us-east-1"
#Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE':'Casa Colombia Real Estate',
    'SCHEMA_PATH': '/schema.yml/'
    }


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
}


WSGI_APPLICATION = 'real_estate_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": env.str("SQL_DATABASE", "casa_real_estate"),
        "USER": env.str("SQL_USER", "postgres"),
        "PASSWORD": env.str("SQL_PASSWORD", "Alpine12*"),
        "HOST": env.str("SQL_HOST", "database-3.c5hpwslivdg0.us-east-1.rds.amazonaws.com"),
        "PORT": env.str("SQL_PORT", "5432"),
    },
}

AUTH_USER_MODEL = 'users.User'  # Change to your user model


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

CORS_ORIGIN_ALLOW_ALL = True


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# JWT_AUTH = {
#     'JWT_SECRET_KEY': SECRET_KEY,
#     'JWT_ALGORITHM': 'HS256',
#     'JWT_ALLOW_REFRESH': True,
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
#     'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
#     'JWT_PAYLOAD_HANDLER': 'accounts.utils.jwt_payload_handler',
#     'JWT_ENCODE_HANDLER': 'accounts.utils.jwt_encode_handler',
#     'JWT_DECODE_HANDLER': 'accounts.utils.jwt_decode_handler',
#     'JWT_GET_USER_SECRET_KEY': 'accounts.utils.get_secret_key_from_user',
#     'JWT_PUBLIC_KEY': None,
#     'JWT_PRIVATE_KEY': None,
#     'JWT_GET_USER_ID_FROM_PAYLOAD_HANDLER': 'accounts.utils.jwt_get_user_id_from_payload_handler',
#     'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'accounts.utils.jwt_get_username_from_payload_handler',
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'accounts.utils.jwt_response_payload_handler',
#     'JWT_AUTH_HEADER_PREFIX': 'JWT',
# }


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
