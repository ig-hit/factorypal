from typing import Dict

import influxdb_client
from django.conf import settings

from influx import client


class Machine(client.Client):
    measurement = 'machines'

    def exists(self, key: str) -> bool:
        query = (
            f'from(bucket: "{settings.INFLUXDB_BUCKET}") '
            f'|> range(start: 0, stop: now())'
            f'|> filter(fn: (r) => r._measurement == "{self.measurement}" and r.key == "{key}")'
            f'|> count()'
        )
        res = self.read(query)

        return len(res) > 0

    def save(self, item: Dict):
        return super().write(
            influxdb_client.Point.from_dict(
                {
                    'measurement': self.measurement,
                    'tags': {
                        'key': item.get('key'),
                    },
                    'fields': {
                        'name': item.get('name'),
                    },
                    'time': 0,
                }
            )
        )


class Parameters(client.Client):
    measurement = 'params'

    def latest(self, machine_key: str):
        ts = self.last_timestamp(machine_key)
        if not ts:
            return

        query = (
            f'from(bucket: "{settings.INFLUXDB_BUCKET}") '
            f'|> range(start: {ts.isoformat()}, stop: now())'
            f'|> filter(fn: (r) => r._measurement == "{self.measurement}" and r.machine_key == "{machine_key}")'
            f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
            f'|> drop(columns: ["_start", "_stop", "_time", "_measurement", "machine_key"])'
        )
        res = self.read(query)
        if not res:
            return {}

        first = res[0]
        cols = {c.label for c in first.columns if c.label not in {'result', 'table'}}

        return {k: v for k, v in first.records[0].values.items() if k in cols}

    def last_timestamp(self, machine_key: str):
        query = (
            f'from(bucket: "{settings.INFLUXDB_BUCKET}")'
            f'|> range(start: 0, stop: now())'
            f'|> filter(fn: (r) => r._measurement == "{self.measurement}" and r.machine_key == "{machine_key}")'
            f'|> keep(columns: ["_time"])'
            f'|> last(column: "_time")'
        )
        res = self.read(query)
        if not res:
            return None
        return res[0].records[0]['_time']

    def aggregates(self, machine_key: str, param_name: str, last_minutes=None):
        fns = ('median', 'mean', 'min', 'max')
        values = {}
        start_q = 0 if not last_minutes else f'-{last_minutes}m'

        # todo(igor): collect async
        for fn in fns:
            values[fn] = None
            query = (
                f'from(bucket: "{settings.INFLUXDB_BUCKET}") '
                f'|> range(start: {start_q}, stop: now())'
                f'|> filter(fn: (r) => r._measurement == "{self.measurement}" and r.machine_key == "{machine_key}")'
                f'|> filter(fn: (r) => r._field == "{param_name}")'
                f'|> {fn}()'
            )

            res = self.read(query)
            if not res:
                continue

            values[fn] = res[0].records[0].get_value()

        return values

    def save(self, machine_key: str, params: Dict[str, float]):
        return super().write(
            influxdb_client.Point.from_dict(
                {
                    'measurement': self.measurement,
                    'tags': {
                        'machine_key': machine_key,
                    },
                    'fields': {k: float(v)
                               for k, v in params.items()},
                }
            )
        )
