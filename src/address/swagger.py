""" This file contains some types, schemas, decorators, etc. needed to customize the Swagger documentation.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework import status

from address.serializers import AddressSerializer


class UserAddressResponse(AddressSerializer):
    """ Dummy Serializer used for Swagger schema.
    """
    uuid = serializers.UUIDField()

    class Meta(AddressSerializer.Meta):
        fields = AddressSerializer.Meta.fields + ['uuid']


delete_uuids_parameter = openapi.Parameter(
    'uuids',
    openapi.IN_QUERY,
    description='List of uuids to delete. If none are sent, all of the user addresses are deleted.',
    type=openapi.TYPE_STRING,
    required=False
)

get_decorator = swagger_auto_schema(responses={status.HTTP_200_OK: UserAddressResponse})
update_decorator = swagger_auto_schema(
    request_body=AddressSerializer,
    responses={status.HTTP_200_OK: UserAddressResponse}
)
create_decorator = swagger_auto_schema(
    request_body=AddressSerializer,
    responses={status.HTTP_201_CREATED: UserAddressResponse}
)
delete_decorator = swagger_auto_schema(manual_parameters=[delete_uuids_parameter])

swagger_method_decorators = {
    'list': {
        'name': 'list',
        'decorator': get_decorator
    },
    'retrieve': {
        'name': 'retrieve',
        'decorator': get_decorator
    },
    'create': {
        'name': 'create',
        'decorator': create_decorator
    },
    'partial_update': {
        'name': 'partial_update',
        'decorator': update_decorator
    },
    'update': {
        'name': 'update',
        'decorator': update_decorator
    },
    'delete': {
        'name': 'delete',
        'decorator': delete_decorator
    },
}
