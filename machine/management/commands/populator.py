import csv

from django.conf import settings
from django.core import management
from influxdb_client.client import write_api

from machine import influx


class Populator(management.BaseCommand):
    fixture_path = None

    def handle(self, *args, **kwargs):
        reader = csv.reader(open(self.fixture_path, 'r'))
        hdr = next(reader)
        writer = influx.Machine().writer(write_api.WriteOptions(write_type=write_api.SYNCHRONOUS))
        for row in reader:
            point = self.parse_row(dict(zip(hdr, row)))
            writer.write(bucket=settings.INFLUXDB_BUCKET, record=point)

    def parse_row(self, row):
        raise NotImplemented()
