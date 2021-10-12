from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from address.models import Address, UserAddress
from address.serializers import AddressSerializer, UserAddressSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        address_serializer = AddressSerializer(data=request.data)
        address_serializer.is_valid(raise_exception=True)
        address, _ = Address.objects.get_or_create(
            zip_code=address_serializer.validated_data['zip_code'],
            address_one=address_serializer.validated_data['address_one'],
            defaults=address_serializer.validated_data
        )

        user_address_serializer = UserAddressSerializer(
            data={
                'user': request.user.pk,
                'address': address.pk,
                'additional_address_data': request.data.get('address_two', '')
            }
        )

        user_address_serializer.is_valid(raise_exception=True)
        user_address_serializer.save()

        return Response(user_address_serializer.data, status=status.HTTP_201_CREATED)
