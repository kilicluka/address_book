from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from address.models import Address, UserAddress
from address.serializers import AddressSerializer, UserAddressSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'uuid'

    def create(self, request, *args, **kwargs):
        return Response(self._store_user_address(), status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user_address = self.get_object()
        return Response(self._store_user_address(user_address), status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        uuids_to_delete = request.data.get('uuids', '')
        queryset = self.get_queryset()

        if uuids_to_delete:
            queryset = queryset.filter(uuid__in=uuids_to_delete.split(','))

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def get_object(self):
        filters = {self.lookup_url_kwarg: self.kwargs[self.lookup_url_kwarg]}
        return get_object_or_404(self.get_queryset(), **filters)

    def _store_user_address(self, user_address_instance=None):
        address = self._get_address_instance(self.request.data)
        user_address_serializer = UserAddressSerializer(
            user_address_instance,
            data={
                'user': self.request.user.pk,
                'address': address.pk,
                'additional_address_data': self.request.data.get('address_two', '')
            }
        )

        user_address_serializer.is_valid(raise_exception=True)
        user_address_serializer.save()

        return user_address_serializer.data

    def _get_address_instance(self, address_data):
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address, _ = Address.objects.get_or_create(
            country=address_serializer.validated_data['country'],
            state=address_serializer.validated_data['state'],
            city=address_serializer.validated_data['city'],
            zip_code=address_serializer.validated_data['zip_code'],
            address_one=address_serializer.validated_data['address_one'],
            defaults=address_serializer.validated_data
        )

        return address
