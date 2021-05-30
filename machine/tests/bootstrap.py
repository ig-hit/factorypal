import influxdb_client
from django import test
from django.conf import settings


@test.tag('integration')
@test.override_settings(
    INFLUXDB_ORG='factorypal',
    INFLUXDB_URL='http://localhost:8086',
    INFLUXDB_TOKEN='factorypal',
    INFLUXDB_BUCKET='testing-bucket',
)
class IntegrationTestCase(test.SimpleTestCase):
    http_client = None
    influx_client = None
    bucket_client = None

    def setUp(self):
        self.http_client = test.client.Client()

        self.influx_client = influxdb_client.InfluxDBClient(
            org=settings.INFLUXDB_ORG,
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
        )

        # recreate buckets for every test
        buckets_api = self.influx_client.buckets_api()
        org_api = self.influx_client.organizations_api()
        orgs = org_api.find_organizations()
        org = orgs[0]

        bucket = buckets_api.find_bucket_by_name(settings.INFLUXDB_BUCKET)
        if bucket:
            buckets_api.delete_bucket(bucket)
        bucket = buckets_api.create_bucket(bucket_name=settings.INFLUXDB_BUCKET, org_id=org.id)

        self.bucket_client = buckets_api


@test.tag('unit')
@test.override_settings(
    INFLUXDB_ORG='testing-org',
    INFLUXDB_URL='http://testing-url',
    INFLUXDB_TOKEN='testing-token',
    INFLUXDB_BUCKET='testing-bucket',
)
class UnitTestCase(test.SimpleTestCase):
    pass
