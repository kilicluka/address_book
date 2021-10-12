import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from address.models import UserAddress
from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__they_can_not_update_their_addresses(api_client):
    response = api_client.put(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json', data={})
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_updates_a_main_part_of_the_address_to_a_non_existing_one__a_new_address_is_created(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
    authenticated_user
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 1)
    work_address_data = get_work_address_data('New York Address 55')

    response = authenticated_client.put(
        reverse('user-addresses-detail', kwargs={'uuid': user_work_address_instance.uuid}),
        format='json',
        data=work_address_data
    )
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_200_OK
    assert response.data['uuid'] == str(user_work_address_instance.uuid)
    assert response.data == {'uuid': str(user_address.uuid), **work_address_data}

    assert_address_and_user_address_counts(user_work_address_instance.user, 2, 1)
