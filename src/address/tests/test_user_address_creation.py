import pytest
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from address.models import UserAddress
from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__they_can_not_create_addresses(api_client):
    response = api_client.post(reverse('user-addresses-list'), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_create_addresses(
    authenticated_client,
    get_home_address_data,
    get_work_address_data,
    authenticated_user,
):
    assert_address_and_user_address_counts(authenticated_user, 0, 0)

    for address_data in (get_home_address_data(), get_work_address_data()):
        response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=address_data)
        user_address = UserAddress.objects.filter(user=authenticated_user).latest()

        assert response.status_code == HTTP_201_CREATED
        assert response.data == {'uuid': str(user_address.uuid), **address_data}

    assert_address_and_user_address_counts(authenticated_user, 2, 2)


def test_when_user_tries_to_add_a_duplicate_address__bad_request_is_returned(
    authenticated_client,
    user_home_address_instance,
    get_home_address_data,
):
    assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=get_home_address_data())

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert str(response.data['non_field_errors'][0]) == 'The fields user, address must make a unique set.'

    assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)


@pytest.mark.usefixtures('home_address_instance')
def test_when_user_adds_a_new_address_which_is_already_in_database__new_address_instance_is_not_created(
    authenticated_client,
    get_home_address_data,
    authenticated_user,
):
    assert_address_and_user_address_counts(authenticated_user, 1, 0)
    home_address_data = get_home_address_data(address_two='2nd Floor, Last Name')

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=home_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_201_CREATED
    assert response.data == {'uuid': str(user_address.uuid), **home_address_data}

    assert_address_and_user_address_counts(authenticated_user, 1, 1)
