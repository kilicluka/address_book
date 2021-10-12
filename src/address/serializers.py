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
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    address = AddressSerializer()

    class Meta:
        model = UserAddress
        fields = ['user', 'address', 'additional_address_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        address_data = dict(self.initial_data)
        additional_address_data = address_data.pop('address_two', '')
        self.initial_data = {
            'user': self.context['request'].user,
            'address': address_data,
            'additional_address_data': additional_address_data
        }

    def create(self, validated_data):
        additional_address_data = validated_data.pop('additional_address_data')

        address, _ = Address.objects.get_or_create(
            zip_code=validated_data['address']['zip_code'],
            address_one=validated_data['address']['address_one'],
            defaults=validated_data['address']
        )

        return UserAddress.objects.create(
            user=self.context['request'].user,
            address=address,
            additional_address_data=additional_address_data
        )

    def to_representation(self, instance):
        return {
            **AddressSerializer(instance.address).data,
            'address_two': instance.additional_address_data
        }
