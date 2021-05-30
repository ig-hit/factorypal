from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import collections


def latest():
    return swagger_auto_schema(
        operation_description='Returns the latest parameters for a machine',
        responses=openapi.Responses(
            responses={
                200: openapi.Response(
                    '',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
                    ),
                ),
            },
        ),
    )


def aggregates():
    return swagger_auto_schema(
        operation_description='Returns aggregates parameters for a machine with a parameter',
        responses=openapi.Responses(
            responses={
                200: openapi.Response(
                    '',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=collections.OrderedDict(
                            min=decimal(),
                            max=decimal(),
                            median=decimal(),
                            mean=decimal(),
                        ),
                        required=['min', 'max', 'median', 'mean'],
                    ),
                ),
            },
        ),
    )


def decimal(**kwargs):
    return openapi.Schema(
        type=openapi.TYPE_NUMBER,
        format=openapi.FORMAT_FLOAT,
        **kwargs,
    )
