import pytest
from django.urls import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__all_address_views_are_inaccessible(client):
    response = client.get(reverse('address-list'), format='json')

    assert response.status_code == HTTP_401_UNAUTHORIZED
