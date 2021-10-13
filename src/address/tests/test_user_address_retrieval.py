import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from address.tests.conftest import assert_address_and_user_address_counts

pytestmark = pytest.mark.django_db


def test_when_user_is_not_authenticated__they_can_not_retrieve_their_addresses(api_client):
    response = api_client.get(reverse('user-addresses-list'), format='json', data={})
    assert response.status_code == HTTP_401_UNAUTHORIZED

    response = api_client.get(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_retrieve_all_their_addresses(
    user_work_address_instance,
    get_work_address_data,
    user_home_address_instance,
    get_home_address_data,
    authenticated_client,
    other_user_home_address_instance,
):
    assert_address_and_user_address_counts(user_home_address_instance.user, 2, 2)
    assert_address_and_user_address_counts(other_user_home_address_instance.user, 2, 1)

    response = authenticated_client.get(reverse('user-addresses-list'), format='json')

    assert response.status_code == HTTP_200_OK
    assert response.data == {
        'count': 2,
        'next': None,
        'previous': None,
        'results': [
            {'uuid': str(user_work_address_instance.uuid), **get_work_address_data()},
            {'uuid': str(user_home_address_instance.uuid), **get_home_address_data()}
        ]
    }


def test_when_the_number_of_addresses_exceeds_page_limit__result_is_paginated(
    user_work_address_instance,
    get_work_address_data,
    user_home_address_instance,
    get_home_address_data,
    authenticated_client,
):
    response = authenticated_client.get(reverse('user-addresses-list'), data={'page_size': 1}, format='json')

    assert response.status_code == HTTP_200_OK
    response_data_copy = dict(response.data)
    results = response_data_copy.pop('results')
    assert response_data_copy == {
        'count': 2,
        'next': 'http://testserver/user-addresses/?page=2&page_size=1',
        'previous': None,
    }
    assert len(results) == 1


def test_when_user_is_authenticated__they_can_retrieve_an_address_by_its_uuid(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
):
    response = authenticated_client.get(
        reverse('user-addresses-detail', kwargs={'uuid': user_work_address_instance.uuid}),
        format='json',
    )

    assert response.status_code == HTTP_200_OK
    assert response.data == {'uuid': str(user_work_address_instance.uuid), **get_work_address_data()}


def test_when_user_attempts_to_retrieve_an_address_not_belonging_to_them__not_found_is_returned(
    authenticated_client,
    other_user_home_address_instance,
):
    response = authenticated_client.get(
        reverse('user-addresses-detail', kwargs={'uuid': other_user_home_address_instance.uuid}),
        format='json',
    )

    assert response.status_code == HTTP_404_NOT_FOUND
