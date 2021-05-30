from django import urls
from django.conf import settings

from machine import influx
from machine.tests import bootstrap


class HomeTest(bootstrap.IntegrationTestCase):
    def test_home(self):
        url = urls.reverse('home')
        response = self.http_client.get(url)
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual({'success': True}, res)


class IndexViewTest(bootstrap.IntegrationTestCase):
    def test_create(self):
        url = urls.reverse('machine-index-list')
        data = {
            'key': 'm-key',
            'name': 'M-Name',
        }

        # create 2 requests
        _ = self.http_client.post(path=url, data=data)
        response = self.http_client.post(path=url, data=data, content_type='application/json')
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data, res)

        query = (
            f'from(bucket: "{settings.INFLUXDB_BUCKET}")'
            f'|> range(start: 0, stop: now())'
            f'|> filter(fn: (r) => r._measurement == "machines" and r.key == "m-key")'
        )

        machines = []
        for record in self.influx_client.query_api().query_stream(query):
            machines.append({
                'key': record.values.get('key'),
                'name': record.get_value(),
            })
        self.assertEqual([data], machines)

    def test_create_fails(self):
        url = urls.reverse('machine-index-list')
        data = {
            'key': '',
            'name': 'M-Name',
        }

        response = self.http_client.post(path=url, data=data, content_type='application/json')
        res = response.json()

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'error': '{\'key\': [ErrorDetail(string=\'This field may not be blank.\', code=\'blank\')]}'}, res
        )


class ParametersViewTest(bootstrap.IntegrationTestCase):
    def test_create(self):
        # 1. create machine
        machine_key = 'm-2'
        url = urls.reverse('machine-index-list')
        data = {
            'key': machine_key,
            'name': 'M2-Name',
        }

        _ = self.http_client.post(path=url, data=data)

        url = urls.reverse('machine-parameters-list', kwargs={'machine_pk': machine_key})
        data = {
            'machineKey': 'otherKey',
            'parameters': {
                'param-1': 1,
                'param-2': 2,
            },
        }

        response = self.http_client.post(path=url, data=data, content_type='application/json')
        res = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(res, {
            'machineKey': machine_key,
            'parameters': {
                'param-1': 1,
                'param-2': 2,
            },
        })

    def test_create_fails(self):
        url = urls.reverse('machine-parameters-list', kwargs={'machine_pk': 'non-existing'})
        data = {
            'machineKey': 'non-existing',
            'parameters': {
                'param-1': 1,
                'param-2': 2,
            },
        }

        response = self.http_client.post(path=url, data=data, content_type='application/json')
        res = response.json()
        self.assertEqual(400, response.status_code)

        self.assertEqual({'error': 'invalid machine key'}, res)

    def test_latest(self):
        # create machine
        machine_key = 'm-3'
        m = {'key': machine_key, 'name': 'M-3'}
        influx.Machine().save(m)

        # save couple parameters
        influx.Parameters().save(machine_key=machine_key, params={'p-1': 1, 'p-2': 2})
        influx.Parameters().save(machine_key=machine_key, params={'p-3': 3, 'p-4': 4.4})

        url = urls.reverse('machine-parameters-latest', kwargs={'machine_pk': machine_key})
        response = self.http_client.get(path=url)
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(res, {'p-3': 3, 'p-4': 4.4})

    def test_latest_empty(self):
        machine_key = 'm-3'

        url = urls.reverse('machine-parameters-latest', kwargs={'machine_pk': machine_key})
        response = self.http_client.get(path=url)
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(res, {})

    def test_aggregates(self):
        # create machine
        machine_key = 'm-4'
        m = {'key': machine_key, 'name': 'M-4'}
        influx.Machine().save(m)

        # save couple parameters
        influx.Parameters().save(machine_key=machine_key, params={'x': 1, 'y': 11})
        influx.Parameters().save(machine_key=machine_key, params={'x': 2, 'y': 12})
        influx.Parameters().save(machine_key=machine_key, params={'x': 3, 'y': 13})
        influx.Parameters().save(machine_key=machine_key, params={'x': 4, 'y': 14})
        influx.Parameters().save(machine_key=machine_key, params={'x': 5, 'y': 13})
        influx.Parameters().save(machine_key=machine_key, params={'x': 6, 'y': 14})

        url = urls.reverse('machine-parameters-aggregates', kwargs={'machine_pk': machine_key, 'pk': 'x'})
        response = self.http_client.get(path=url)
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(res, {'min': 1, 'max': 6, 'mean': 3.5, 'median': 3.5})

    def test_aggregates_empty(self):
        url = urls.reverse('machine-parameters-aggregates', kwargs={'machine_pk': 'non-existing', 'pk': 'x'})
        response = self.http_client.get(path=url)
        res = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(res, {'min': None, 'max': None, 'mean': None, 'median': None})
