import os
from ._base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split()
# https://docs.djangoproject.com/en/4.0/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS
MIDDLEWARE += ["django.middleware.csrf.CsrfViewMiddleware"]
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split()

# CORS HEADERS
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr
CORS_ALLOWED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split()
# https://github.com/adamchainz/django-cors-headers#cors_urls_regex-str--patternstr
CORS_URLS_REGEX = r"^/api/.*$"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "OPTIONS": {"sslmode": "require"},
    }
}

# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# STORAGE
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = f'https://{os.getenv("AWS_S3_ENDPOINT")}'
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_STATIC_FILE_LOCATION = "staticfiles/"
AWS_MEDIA_FILE_LOCATION = "mediafiles/"

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR / "staticfiles" / "react" / "build" / "static"]  # noqa
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STATIC_FILE_LOCATION)
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# MEDIA
# ------------------------------------------------------------------------------
# MEDIA_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_MEDIA_FILE_LOCATION)
