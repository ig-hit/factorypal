from unittest import mock

from machine import serializers
from machine.tests import bootstrap


class MachineSerializerTest(bootstrap.UnitTestCase):
    @mock.patch('machine.influx.Machine.save')
    @mock.patch('machine.serializers.MachineSerializer.is_valid', return_value=True)
    def test_save(self, is_valid, saver):
        service = serializers.MachineSerializer()
        item = {'key': 'k', 'name': 'N'}
        service._validated_data = item

        service.save()

        is_valid.assert_called_once()
        saver.assert_called_once_with(item)


class ParametersSerializerTest(bootstrap.UnitTestCase):
    @mock.patch('machine.influx.Parameters.save')
    @mock.patch('machine.serializers.ParametersSerializer.is_valid', return_value=True)
    def test_save(self, is_valid, saver):
        service = serializers.ParametersSerializer()
        machine_key = 'm-1'
        parameters = {'p-1': 1.1, 'p-2': 2.2}
        service._validated_data = {
            'machineKey': machine_key,
            'parameters': parameters,
        }

        service.save()

        is_valid.assert_called_once()
        saver.assert_called_once_with(machine_key=machine_key, params=parameters)
