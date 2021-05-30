import schema

from machine import errors, influx


def validate_machine(data):
    return schema.Schema(
        {
            'key': schema.And(str, _is_valid_key, error=errors.Error.INVALID_MACHINE_KEY.value),
            'name': schema.And(str, len, error=errors.Error.INVALID_MACHINE_NAME.value),
        },
    ).validate(data)


def validate_parameters(data):
    return schema.Schema(
        {
            'machineKey': schema.And(
                str,
                _is_valid_key,
                _is_existing_key,
                error=errors.Error.INVALID_MACHINE_KEY.value,
            ),
            'parameters': schema.And(
                {
                    str: schema.And(
                        schema.Or(int, float),
                        error=errors.Error.INVALID_PARAMETER_VALUE.value,
                    ),
                },
                error=errors.Error.INVALID_PARAMETERS.value
            ),
        },
    ).validate(data)


def _is_valid_key(value):
    return len(value)


def _is_existing_key(value):
    return influx.Machine().exists(value)
