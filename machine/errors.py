import enum


class Error(enum.Enum):
    FAILED_TO_SAVE = 'failed to save'
    INVALID_MACHINE_KEY = 'invalid machine key'
    INVALID_MACHINE_NAME = 'invalid machine name'
    INVALID_PARAMETER_VALUE = 'invalid parameter value'
    INVALID_PARAMETERS = 'invalid parameters'
