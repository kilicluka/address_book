import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from address.models import Address, UserAddress

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
def address_instance(user_address_data):
    address_data = dict(user_address_data)
    address_data.pop('address_two')
    return Address.objects.create(**address_data)


@pytest.fixture
def user_address_instance(authenticated_user, address_instance):
    return UserAddress.objects.create(
        user=authenticated_user,
        address=address_instance,
        additional_address_data='5th floor, name: Jackson'
    )


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
    _assert_address_and_user_address_counts(authenticated_user, 0, 0)

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=user_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_201_CREATED
    assert response.data == {
        'uuid': str(user_address.address.uuid),
        **user_address_data
    }

    _assert_address_and_user_address_counts(authenticated_user, 1, 1)


@pytest.mark.django_db(transaction=True)
def test_when_user_tries_to_add_duplicated_address__bad_request_is_returned(
    authenticated_client,
    user_address_instance,
    user_address_data,
    authenticated_user
):
    _assert_address_and_user_address_counts(authenticated_user, 1, 1)

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=user_address_data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data == 'You already have an address with those zip_code and address_one values.'

    assert UserAddress.objects.filter(user=authenticated_user).count() == 1
    assert Address.objects.count() == 1


def test_when_address_is_already_in_database__new_one_is_not_created(
    authenticated_client,
    address_instance,
    user_address_data,
    authenticated_user
):
    _assert_address_and_user_address_counts(authenticated_user, 1, 0)

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=user_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)
    print('mrs')

    assert response.status_code == HTTP_201_CREATED
    assert response.data == {
        'uuid': str(user_address.address.uuid),
        **user_address_data
    }

    _assert_address_and_user_address_counts(authenticated_user, 1, 1)


def _assert_address_and_user_address_counts(user, address_count, user_address_count):
    assert Address.objects.count() == address_count
    assert UserAddress.objects.filter(user=user).count() == user_address_count
