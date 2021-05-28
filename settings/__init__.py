import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
SECRET_KEY = 'pae*=)f1$60gcj0_re-2u(tzqg4ni$sq2nvh1wgcx@hrh6_2+t'
ROOT_URLCONF = 'service.urls'
WSGI_APPLICATION = 'service.wsgi.application'

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'drf_yasg',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

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
