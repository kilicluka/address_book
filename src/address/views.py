from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from address.serializers import UserAddressSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]
