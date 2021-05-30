import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
SECRET_KEY = 'pae*=)f1$60gcj0_re-2u(tzqg4ni$sq2nvh1wgcx@hrh6_2+t'
ROOT_URLCONF = 'service.urls'
WSGI_APPLICATION = 'service.wsgi.application'
DEBUG = True
ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'drf_yasg',
    'machine.apps.MachineConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}

INFLUXDB_ORG = os.environ['INFLUXDB_ORG']
INFLUXDB_URL = os.environ['INFLUXDB_URL']
INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']
INFLUXDB_BUCKET = os.environ['INFLUXDB_BUCKET']

from drf_yasg import openapi
SWAGGER_SETTINGS = {
    'DEFAULT_INFO': openapi.Info(
        title='FactoryPal API',
        default_version='v1',
        description='description',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
}
