import influxdb_client
from django.conf import settings


def get_client():
    return influxdb_client.InfluxDBClient(
        url=settings.INFLUXDB_URL,
        token=settings.INFLUXDB_TOKEN,
    )
