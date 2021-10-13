import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from address.models import UserAddress
from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__they_can_not_update_their_addresses(api_client):
    response = api_client.put(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json', data={})
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_updates_a_main_part_of_the_address_to_something_completely_new__a_new_address_is_created(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
    authenticated_user,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 1)
    work_address_data = get_work_address_data(address_one='New York Address 55')

    response = _send_update_request(authenticated_client, user_work_address_instance.uuid, work_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_200_OK
    assert response.data['uuid'] == str(user_work_address_instance.uuid)
    assert response.data == {'uuid': str(user_address.uuid), **work_address_data}

    assert_address_and_user_address_counts(user_work_address_instance.user, 2, 1)


def test_when_user_updates_the_address_two_field__new_address_is_not_created(
    authenticated_client,
    get_home_address_data,
    user_home_address_instance,
    authenticated_user,
):
    assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)
    home_address_data = get_home_address_data(address_two='Second Floor, first door to the right')

    response = _send_update_request(authenticated_client, user_home_address_instance.uuid, home_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_200_OK
    assert response.data['uuid'] == str(user_home_address_instance.uuid)
    assert response.data == {'uuid': str(user_address.uuid), **home_address_data}

    assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)


def test_when_user_updates_a_main_part_of_the_address_to_an_existing_address__that_address_is_reused(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
    home_address_instance,
    authenticated_user,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 2, 1)
    work_address_data = get_work_address_data(state='', address_one='Home Address 15')

    response = _send_update_request(authenticated_client, user_work_address_instance.uuid, work_address_data)
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_200_OK
    assert response.data['uuid'] == str(user_work_address_instance.uuid)
    assert response.data == {'uuid': str(user_address.uuid), **work_address_data}

    assert_address_and_user_address_counts(user_work_address_instance.user, 2, 1)


def test_when_user_attempts_to_update_an_address_not_belonging_to_them__not_found_is_returned(
    authenticated_client,
    other_user_home_address_instance,
    get_work_address_data,
):
    response = _send_update_request(
        authenticated_client,
        other_user_home_address_instance.uuid,
        get_work_address_data(address_one='Berlin Street 12')
    )

    assert response.status_code == HTTP_404_NOT_FOUND


def _send_update_request(client, uuid, update_data):
    return client.put(reverse('user-addresses-detail', kwargs={'uuid': uuid}), format='json', data=update_data)
