from unittest import mock

import ddt
import schema

from machine import validators
from machine.tests import bootstrap


@ddt.ddt
class ValidatorsTest(bootstrap.UnitTestCase):
    @ddt.data(
        (
            {
                'key': 'z',
                'name': 'Z'
            },
            None,
        ),
        (
            {
                'key': '',
                'name': ''
            },
            'invalid machine key',
        ),
        (
            {
                'key': 'z',
                'name': ''
            },
            'invalid machine name',
        ),
    )
    def test_validate_machine(self, case):
        input_data, expected_exception = case
        fn = validators.validate_machine

        if expected_exception:
            with self.assertRaisesMessage(expected_exception=schema.SchemaError, expected_message=expected_exception):
                fn(input_data)
        else:
            self.assertTrue(fn(input_data))

    @ddt.data(
        (
            {
                'machineKey': 'x',
                'parameters': {
                    'p-1': 1,
                    'p-2': 1.1,
                },
            },
            None,
        ),
        (
            {
                'machineKey': 'x',
                'parameters': {},
            },
            'invalid parameters',
        ),
        (
            {
                'machineKey': 'x',
                'parameters': {
                    'p-1': 'P',
                },
            },
            'invalid parameter value',
        ),
    )
    @mock.patch('machine.validators._is_valid_key')
    @mock.patch('machine.validators._is_existing_key')
    def test_validate_parameters(self, case, is_existing_key, is_valid_key):
        input_data, expected_exception = case
        fn = validators.validate_parameters

        if expected_exception:
            with self.assertRaisesMessage(expected_exception=schema.SchemaError, expected_message=expected_exception):
                fn(input_data)
        else:
            self.assertTrue(fn(input_data))
