from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from machine import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', views.IndexView, 'machine-index')

parameters_router = nested_routers.NestedSimpleRouter(router, r'', lookup='machine')
parameters_router.register(r'parameters', views.ParametersView, 'machine-parameters')

urlpatterns = router.urls + parameters_router.urls
