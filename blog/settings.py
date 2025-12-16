"""
Django settings for blog project.
"""

from pathlib import Path
import os
from datetime import timedelta
from decouple import config

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = config('SECRET_KEY')

# Reads DEBUG value from .env, defaults to False for production
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',

    # Local apps
    'post',
    'account',
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]


# --------------------------------------------------
# AUTO LOGOUT & SESSIONS
# --------------------------------------------------
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(hours=1),
    'SESSION_TIME': timedelta(hours=1),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    'MESSAGE': 'Your session has expired. Please log in again.',
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True


# --------------------------------------------------
# URLS / TEMPLATES
# --------------------------------------------------
ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# --------------------------------------------------
# DATABASE (Supabase PostgreSQL)
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC FILES (Vercel + WhiteNoise)
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ---------------- MEDIA (SUPABASE STORAGE) ----------------
# Uses Supabase S3 API to handle file storage, resolving the Read-only file system error on Vercel.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_REGION = config('SUPABASE_REGION')
SUPABASE_PROJECT_REF = config('SUPABASE_PROJECT_REF')

# S3 Configuration using Supabase keys:
# AWS_ACCESS_KEY_ID uses the Project REF as a placeholder.
# AWS_SECRET_ACCESS_KEY must use the highly secret SUPABASE_SERVICE_ROLE_KEY (JWT).
AWS_ACCESS_KEY_ID = SUPABASE_PROJECT_REF
AWS_SECRET_ACCESS_KEY = config('SUPABASE_SERVICE_ROLE_KEY')

AWS_STORAGE_BUCKET_NAME = 'media' # The name of your bucket in Supabase
AWS_S3_ENDPOINT_URL = f'{SUPABASE_URL}/storage/v1/s3'
AWS_S3_REGION_NAME = SUPABASE_REGION
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'path'

# Public URL for accessing media files
MEDIA_URL = f'{SUPABASE_URL}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}/'


# --------------------------------------------------
# DEFAULT PK
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------
# CRISPY FORMS
# --------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# --------------------------------------------------
# EMAIL
# --------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Values taken from .env file
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')