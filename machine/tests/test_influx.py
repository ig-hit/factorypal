import dataclasses
from datetime import datetime
from typing import List
from unittest import mock

from machine import influx
from machine.tests import bootstrap


class MachineTest(bootstrap.UnitTestCase):
    @mock.patch('machine.influx.Machine.read')
    def test_exists(self, reader):
        service = influx.Machine()
        key = 'm-1'
        reader.return_value = [{}]

        res = service.exists(key)

        self.assertTrue(res)
        reader.assert_called_once_with(
            (
                f'from(bucket: "testing-bucket")'
                f'|> range(start: 0, stop: now())'
                f'|> filter(fn: (r) => r._measurement == "machines" and r.key == "{key}")'
                f'|> count()'
            )
        )

    @mock.patch('influx.client.Client.write')
    def test_save(self, writer):
        service = influx.Machine()
        item = {'key': 'm-1', 'name': 'Machine-1'}

        service.save(item)
        created_point = writer.call_args[0][0]

        self.assertEqual('machines', created_point._name)
        self.assertEqual({'key': 'm-1'}, created_point._tags)
        self.assertEqual({'name': 'Machine-1'}, created_point._fields)
        self.assertEqual(0, created_point._time)


class ParametersTest(bootstrap.UnitTestCase):
    @mock.patch('influx.client.Client.write')
    def test_save(self, writer):
        service = influx.Parameters()

        service.save(machine_key='m-2', params={'p-1': 1.1, 'p-2': 2.2})
        created_point = writer.call_args[0][0]

        self.assertEqual('params', created_point._name)
        self.assertEqual({'machine_key': 'm-2'}, created_point._tags)
        self.assertEqual({'p-1': 1.1, 'p-2': 2.2}, created_point._fields)
        self.assertIsNone(created_point._time)

    @mock.patch('machine.influx.Parameters.get_latest_timestamp')
    @mock.patch('machine.influx.Parameters.read')
    def test_latest(self, reader, latest_ts):
        service = influx.Parameters()
        machine_key = 'm-1'
        latest_ts.return_value = datetime.strptime('2021-05-30', '%Y-%m-%d')

        service.latest(machine_key)

        reader.assert_called_once_with(
            (
                f'from(bucket: "testing-bucket")'
                f'|> range(start: 2021-05-30T00:00:00, stop: now())'
                f'|> filter(fn: (r) => r._measurement == "params" and r.machine_key == "{machine_key}")'
                f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
                f'|> drop(columns: ["_start", "_stop", "_time", "_measurement", "machine_key"])'
            )
        )

    @mock.patch('machine.influx.Parameters.read')
    def test_get_latest_timestamp(self, reader):
        service = influx.Parameters()
        machine_key = 'm-1'

        service.get_latest_timestamp(machine_key)

        reader.assert_called_once_with(
            (
                f'from(bucket: "testing-bucket")'
                f'|> range(start: 0, stop: now())'
                f'|> filter(fn: (r) => r._measurement == "params" and r.machine_key == "{machine_key}")'
                f'|> keep(columns: ["_time"])'
                f'|> last(column: "_time")'
            )
        )

    @mock.patch('machine.influx.Parameters.read')
    def test_aggregates(self, reader):
        service = influx.Parameters()
        machine_key = 'm-1'
        param_name = 'p-1'
        last_minutes = 6

        reader.return_value = [InfluxTable(records=[InfluxRecord(value=1.1)])]

        service.aggregates(machine_key=machine_key, param_name=param_name, last_minutes=last_minutes)

        calls = []
        for f in ('median', 'mean', 'min', 'max'):
            calls.append(
                mock.call(
                    f'from(bucket: "testing-bucket")'
                    f'|> range(start: -6m, stop: now())'
                    f'|> filter(fn: (r) => r._measurement == "params" and r.machine_key == "{machine_key}")'
                    f'|> filter(fn: (r) => r._field == "{param_name}")'
                    f'|> {f}()'
                )
            )

        reader.assert_has_calls(calls)


@dataclasses.dataclass
class InfluxRecord(object):
    value: float

    def get_value(self):
        return self.value


@dataclasses.dataclass
class InfluxTable(object):
    records: List[InfluxRecord]
