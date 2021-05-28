from django.urls import path, include

from machine import urls as machine_urls, views as machine_views

urlpatterns = [
    path('', machine_views.home, name='home'),
    path('machines/', include(machine_urls.urlpatterns)),
]
