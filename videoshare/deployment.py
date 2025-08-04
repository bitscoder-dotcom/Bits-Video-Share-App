import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = True ## for debugging, st to false when going to prod

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