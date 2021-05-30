from django import http
from rest_framework import exceptions, views
from influxdb import exceptions as influxdb_exceptions
import schema


def rest_exception_handler(exc, context):
    # Order matters: from specific to generic
    handlers = {
        http.Http404: _404,
        exceptions.ValidationError: _validation_error,
        exceptions.APIException: _api_exception,
        schema.SchemaError: _schema_error,
        Exception: _catch_all,
    }

    for target, handler in handlers.items():
        if isinstance(exc, target):
            return handler(exc=exc, context=context)


def _404(exc, context):
    err = exceptions.NotFound(detail=str(exc), code='not_found')
    return _api_exception(exc=err, context=context)


def _validation_error(exc, context):
    return views.exception_handler(exc, context)


def _api_exception(exc, context):
    messages = exc.get_full_details()
    message = messages.get('message')
    code = messages.get('code')
    return views.exception_handler(exc, context)


def _schema_error(exc, context):
    new = Exception(str(exc))
    return views.exception_handler(new, context)


def _catch_all(exc, context):
    err = exceptions.APIException(detail=str(exc))
    return _api_exception(exc=err, context=context)
