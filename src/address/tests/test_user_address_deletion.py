import pytest
from django.urls import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from address.models import Address, UserAddress
from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_work_address_second_instance(get_work_address_data, authenticated_user):
    data = get_work_address_data(address_one='Random street')
    address_two = data.pop('address_two')
    address = Address.objects.create(**data)

    return UserAddress.objects.create(
        user=authenticated_user,
        address=address,
        additional_address_data=address_two
    )


def test_when_user_is_not_authenticated__they_can_not_delete_their_addresses(api_client):
    response = api_client.delete(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_delete_an_address_by_uuid(
    authenticated_client,
    user_work_address_instance,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 1)

    response = authenticated_client.delete(
        reverse('user-addresses-detail', kwargs={'uuid': user_work_address_instance.uuid}),
        format='json',
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 0)


def test_when_user_is_authenticated__they_can_delete_multiple_addresses_by_uuid_list(
    user_work_address_instance,
    user_home_address_instance,
    user_work_address_second_instance,
    authenticated_client,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 3, 3)

    response = authenticated_client.delete(
        reverse('user-addresses-delete'),
        data={'uuids': f'{user_work_address_instance.uuid},{user_home_address_instance.uuid}'},
        format='json',
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    assert_address_and_user_address_counts(user_work_address_instance.user, 3, 1)


def test_when_user_is_authenticated__they_can_delete_all_addresses_by_sending_no_arguments(
    user_work_address_instance,
    user_home_address_instance,
    user_work_address_second_instance,
    authenticated_client,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 3, 3)

    response = authenticated_client.delete(
        reverse('user-addresses-delete'),
        format='json',
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    assert_address_and_user_address_counts(user_work_address_instance.user, 3, 0)


def test_when_user_attempts_to_delete_an_address_not_belonging_to_them__not_found_is_returned(
    authenticated_client,
    other_user_home_address_instance,
):
    assert_address_and_user_address_counts(other_user_home_address_instance.user, 1, 1)

    response = authenticated_client.delete(
        reverse('user-addresses-detail', kwargs={'uuid': other_user_home_address_instance.uuid}),
        format='json',
    )

    assert response.status_code == HTTP_404_NOT_FOUND

    assert_address_and_user_address_counts(other_user_home_address_instance.user, 1, 1)
