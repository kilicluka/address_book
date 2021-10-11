from rest_framework import serializers

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


class UserAddressSerializer(serializers.ModelSerializer):
    address_two = serializers.CharField(allow_blank=True, required=False, default='')

    class Meta:
        model = UserAddress
        fields = ['address_two']

    def validate(self, attrs):
        super().validate(attrs)

        address_serializer = AddressSerializer(data=self.initial_data)
        address_serializer.is_valid(raise_exception=True)

        return {**address_serializer.validated_data, **attrs}

    def create(self, validated_data):
        address_two = validated_data.pop('address_two')

        address, _ = Address.objects.get_or_create(
            zip_code=validated_data['zip_code'],
            address_one=validated_data['address_one'],
            defaults=validated_data
        )

        return UserAddress.objects.create(
            user=self.context['request'].user,
            address=address,
            additional_address_data=address_two
        )

    def to_representation(self, instance):
        return {
            **AddressSerializer(instance.address).data,
            'address_two': instance.additional_address_data
        }
