import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], '169.254.131.4', '*']
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME'], 'https://169.254.131.4']
DEBUG = True ## for debugging, st to false when going to prod

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

INSTALLED_APPS += [
    'storages',
]

# ─── AZURE BLOB STORAGE FOR MEDIA ────────────────────────────────────────

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_ACCOUNT_NAME   = os.environ['AZURE_STORAGE_ACCOUNT_NAME']
AZURE_ACCOUNT_KEY    = os.environ['AZURE_STORAGE_ACCOUNT_KEY']
AZURE_CONTAINER      = os.environ['AZURE_STORAGE_CONTAINER_NAME']

AZURE_CUSTOM_DOMAIN  = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
MEDIA_URL            = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"


# ─── DATABASE VIA AZURE POSTGRES ────────────────────────────────────────

connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
paramters = {
    kv.split('=',1)[0]: kv.split('=',1)[1]
    for kv in connection_string.split()
}

DATABASES = {

      'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': paramters['dbname'],
            'HOST': paramters['host'],
            'USER': paramters['user'],
            'PASSWORD': paramters['password'],
      }
}


# ─── MIDDLEWARE & LOGGING ───────────────────────────────────────────────

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

## for debugging, remove when going to prod
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}