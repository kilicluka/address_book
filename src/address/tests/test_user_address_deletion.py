import pytest
from django.urls import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__they_can_not_delete_their_addresses(api_client):
    response = api_client.delete(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_delete_an_address_by_uuid(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
):
    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 1)

    response = authenticated_client.delete(
        reverse('user-addresses-detail', kwargs={'uuid': user_work_address_instance.uuid}),
        format='json',
    )

    assert response.status_code == HTTP_204_NO_CONTENT

    assert_address_and_user_address_counts(user_work_address_instance.user, 1, 0)


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
