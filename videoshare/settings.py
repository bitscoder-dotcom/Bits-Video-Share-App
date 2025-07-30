import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev-only')
DEBUG = True
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local apps
    'accounts',
    'content',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'videoshare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'content.context_processors.video_categories',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'videoshare.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'videosharing',
        'USER': 'postgres',
        'PASSWORD': '=-098',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'munim',
#         'PASSWORD': 'swordFish@123',
#         'HOST': 'videosharepg.postgres.database.azure.com',
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',
#         }
#     }




# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Allauth Settings
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

# File Storage (Azure or Local)
DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
STATICFILES_STORAGE = os.getenv('STATICFILES_STORAGE', 'django.contrib.staticfiles.storage.StaticFilesStorage')

# Azure Storage Config
AZURE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
AZURE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net' if AZURE_ACCOUNT_NAME else None
AZURE_LOCATION = 'static'
AZURE_OVERWRITE_FILES = True
AZURE_URL_EXPIRATION_SECS = 3600

# Video Upload Settings
MAX_UPLOAD_SIZE = 524288000  # 500MB
ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv']
ALLOWED_THUMBNAIL_EXTENSIONS = ['jpg', 'jpeg', 'png']

# Messages framework
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}