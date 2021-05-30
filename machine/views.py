from django.http import response
from django.utils import decorators
from rest_framework import viewsets, decorators as drf_decorators, status

from machine import serializers, influx

method_decorator = decorators.method_decorator
action = drf_decorators.action


@drf_decorators.api_view()
def home(request):
    """
    Health check
    """
    return response.JsonResponse(dict(success=True, message='Hallo, Motto!'))


class WithCreateMixin(viewsets.GenericViewSet):
    def post(self, data, **kwargs):
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return response.JsonResponse(dict(error=str(err)), status=status.HTTP_400_BAD_REQUEST)


class IndexView(WithCreateMixin):
    serializer_class = serializers.MachineSerializer

    def create(self, request, **kwargs):
        return super().post(request.data)


class ParametersView(viewsets.ViewSet, WithCreateMixin):
    serializer_class = serializers.ParametersSerializer

    def create(self, request, *args, **kwargs):
        machine_key = kwargs.get('machine_pk')
        data = request.data
        # replace deprecated machineKey
        # it's passed in the url
        data['machineKey'] = machine_key

        return super().post(data)

    @drf_decorators.action(methods=['GET'], detail=False, name='machine-parameters-latest')
    def latest(self, request, *args, **kwargs):
        machine_key = kwargs.get('machine_pk')
        res = influx.Parameters().latest(machine_key)
        return response.JsonResponse(res)

    @drf_decorators.action(methods=['GET'], detail=True, name='machine-parameters-aggregates')
    def aggregates(self, request, pk, *args, **kwargs):
        machine_key = kwargs.get('machine_pk')
        last_minutes = request.GET.get('lastMinutes')
        last_minutes = int(last_minutes) if last_minutes else None
        res = influx.Parameters().aggregates(machine_key=machine_key, param_name=pk, last_minutes=last_minutes)
        return response.JsonResponse(res)
