import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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