from rest_framework import serializers
from rest_framework import validators

from address.models import Address, UserAddress


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
        ]

    def run_validators(self, value):
        """ Skip the unique together validation, since we don't want to punish users for not knowing that an address
        already exists in the database.
        """

        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super().run_validators(value)


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ['user', 'address', 'additional_address_data']

    def to_representation(self, instance):
        return {
            **AddressSerializer(instance.address).data,
            'address_two': instance.additional_address_data
        }
