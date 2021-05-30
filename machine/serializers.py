from rest_framework import serializers, exceptions

from machine import validators, influx, errors


class MachineSerializer(serializers.Serializer):
    class Meta:
        validators = (validators.validate_machine,)

    key = serializers.CharField(help_text='Machine key')
    name = serializers.CharField(help_text='Machine name')

    def save(self, **kwargs):
        if not self.is_valid():
            raise exceptions.ValidationError(errors.Error.FAILED_TO_SAVE.value)

        influx.Machine().save(self.validated_data)


class ParametersSerializer(serializers.Serializer):
    class Meta:
        validators = (validators.validate_parameters,)

    machineKey = serializers.CharField(help_text='Machine key')
    parameters = serializers.DictField(help_text='Parameters')

    def save(self, **kwargs):
        if not self.is_valid():
            raise exceptions.ValidationError(errors.Error.FAILED_TO_SAVE.value)

        data = self.validated_data
        influx.Parameters().save(machine_key=data.get('machineKey'), params=data.get('parameters'))
