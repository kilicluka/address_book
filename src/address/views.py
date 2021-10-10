from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
