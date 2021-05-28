import pathlib
import os


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
    'drf_yasg',
]

INFLUXDB_HOST = os.environ['INFLUX_HOST']
INFLUXDB_PORT = os.environ['INFLUX_PORT']
INFLUXDB_USERNAME = os.environ['INFLUX_USERNAME']
INFLUXDB_PASSWORD = os.environ['INFLUX_PASSWORD']
INFLUXDB_DATABASE = os.environ['INFLUX_USERNAME']
INFLUXDB_TIMEOUT = 10

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
