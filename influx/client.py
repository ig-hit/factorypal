import influxdb_client
from django.conf import settings
from influxdb_client.client import write_api


class Client(object):
    _client = None

    def __init__(self):
        self._client = influxdb_client.InfluxDBClient(
            org=settings.INFLUXDB_ORG,
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
        )

    def read(self, query: str):
        return self._client.query_api().query(query=query)

    def writer(self, write_options=write_api.SYNCHRONOUS):
        return self._client.write_api(write_options=write_options)

    def write(self, point: influxdb_client.Point, write_options=write_api.SYNCHRONOUS):
        return self._client.write_api(write_options=write_options).write(
            bucket=settings.INFLUXDB_BUCKET,
            record=point,
        )
