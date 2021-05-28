from django.utils import decorators
from rest_framework import response, viewsets, decorators as drf_decorators

method_decorator = decorators.method_decorator
action = drf_decorators.action


@drf_decorators.api_view()
def home(request):
    return response.Response(dict(success=True, message='Hallo, Motto!'))


class IndexView(viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        return response.Response(dict(success=True, message='Hallo, Create Machine!'))


class ParametersView(viewsets.ViewSet, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        machine_id = kwargs.get('machine_pk')
        return response.Response(dict(success=True, message=f'Hallo, Create Param for Machine {machine_id}!'))

    @drf_decorators.action(methods=['GET'], detail=False, name='machine-parameters-latest')
    def latest(self, request, *args, **kwargs):
        machine_id = kwargs.get('machine_pk')
        return response.Response(dict(success=True, message=f'Hallo, Latest from Machine {machine_id}!'))

    @drf_decorators.action(methods=['GET'], detail=False, name='machine-parameters-aggregates')
    def aggregates(self, request, *args, **kwargs):
        machine_id = kwargs.get('machine_pk')
        return response.Response(dict(success=True, message=f'Hallo, Aggregates from Machine {machine_id}!'))
