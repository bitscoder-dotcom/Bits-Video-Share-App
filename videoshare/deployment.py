import os
from .settings import *  # noqa
from .settings import BASE_DIR

# --- Security / host headers ---
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
WEBSITE_HOSTNAME = os.getenv("WEBSITE_HOSTNAME")  # set by Azure, None locally
ALLOWED_HOSTS = [h for h in [WEBSITE_HOSTNAME, "bits-videoshare.azurewebsites.net"] if h] + ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [f"https://{WEBSITE_HOSTNAME}"] if WEBSITE_HOSTNAME else []
# Behind Azure’s proxy/load balancer:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

DEBUG = False  # flip to True only for local debugging

# --- Static (served by WhiteNoise) ---`~`
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Media to Azure Blob via django-storages ---
INSTALLED_APPS += ["storages"]

DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"

AZURE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")       # e.g. bitsvideostorage
AZURE_ACCOUNT_KEY  = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
AZURE_CONTAINER    = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "media")
AZURE_OVERWRITE_FILES = False

AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
# MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/" if AZURE_CUSTOM_DOMAIN else "/media/"
AZURE_URL_EXPIRATION_SECS = 3600

# --- Database (Azure Postgres) ---
# Expecting a connection string like: "host=... dbname=... user=... password=... port=5432 sslmode=require"
conn = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING", "")
pairs = [kv.split("=", 1) for kv in conn.split() if "=" in kv]
params = {k: v for k, v in pairs}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": params.get("dbname"),
        "HOST": params.get("host"),
        "USER": params.get("user"),
        "PASSWORD": params.get("password"),
        "PORT": params.get("port", "5432"),
        "OPTIONS": {"sslmode": params.get("sslmode", "require")},
    }
}

# --- Middleware & logging ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
