from rest_framework import serializers

from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'uuid',
            'country',
            'state',
            'city',
            'zip_code',
            'address_one',
            'address_two',
            'created_at',
            'updated_at'
        ]
