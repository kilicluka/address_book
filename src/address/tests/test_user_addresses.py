import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from address.models import UserAddress

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_address_data():
    return {
        'country': 'Croatia',
        'state': '',
        'city': 'Split',
        'zip_code': '21000',
        'address_one': 'Split Address 15',
        'address_two': '',
    }


@pytest.fixture
def authenticated_user(django_user_model):
    return django_user_model.objects.create(username='authenticated_user', password='authenticated_password')


@pytest.fixture
def authenticated_client(authenticated_user, api_client):
    api_client.force_authenticate(authenticated_user)
    return api_client


def test_when_user_is_not_authenticated__all_address_views_are_inaccessible(api_client):
    response = api_client.get(reverse('user-addresses-list'), format='json')

    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_create_an_address(
    authenticated_client,
    user_address_data,
    authenticated_user
):
    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=user_address_data)

    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_201_CREATED
    assert response.data == {
        'uuid': str(user_address.address.uuid),
        **user_address_data
    }
