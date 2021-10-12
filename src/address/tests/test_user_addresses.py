import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from address.models import Address, UserAddress

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_home_address_data():
    def _get_home_address_data(address_two='3rd floor'):
        return {
            'country': 'Croatia',
            'state': '',
            'city': 'Split',
            'zip_code': '21000',
            'address_one': 'Home Address 15',
            'address_two': address_two,
        }
    return _get_home_address_data


@pytest.fixture
def get_work_address_data():
    def _get_work_address_data(address_one='Work Address 22A'):
        return {
            'country': 'Croatia',
            'state': 'Croatia',
            'city': 'Split',
            'zip_code': '21000',
            'address_one': address_one,
            'address_two': 'Ground Floor, Doe',
        }
    return _get_work_address_data


@pytest.fixture
def home_address_instance(get_home_address_data):
    address_data = dict(get_home_address_data())
    address_data.pop('address_two')
    return Address.objects.create(**address_data)


@pytest.fixture
def work_address_instance(get_work_address_data):
    address_data = dict(get_work_address_data())
    address_data.pop('address_two')
    return Address.objects.create(**address_data)


@pytest.fixture
def user_home_address_instance(authenticated_user, home_address_instance, get_home_address_data):
    return UserAddress.objects.create(
        user=authenticated_user,
        address=home_address_instance,
        additional_address_data=get_home_address_data()['address_two']
    )


@pytest.fixture
def user_work_address_instance(authenticated_user, work_address_instance, get_work_address_data):
    return UserAddress.objects.create(
        user=authenticated_user,
        address=work_address_instance,
        additional_address_data=get_work_address_data()['address_two']
    )


@pytest.fixture
def authenticated_user(django_user_model):
    return django_user_model.objects.create(username='authenticated_user', password='authenticated_password')


@pytest.fixture
def other_user(django_user_model):
    return django_user_model.objects.create(username='other_user', password='other_password')


@pytest.fixture
def other_user_home_address_instance(other_user, home_address_instance, get_home_address_data):
    return UserAddress.objects.create(
        user=other_user,
        address=home_address_instance,
        additional_address_data=get_home_address_data()['address_two']
    )


@pytest.fixture
def authenticated_client(authenticated_user, api_client):
    api_client.force_authenticate(authenticated_user)
    return api_client


def test_when_user_is_not_authenticated__all_address_views_are_inaccessible(api_client):
    response = api_client.get(reverse('user-addresses-list'), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED

    response = api_client.post(reverse('user-addresses-list'), format='json', data={})
    assert response.status_code == HTTP_401_UNAUTHORIZED

    response = api_client.put(reverse('user-addresses-detail', kwargs={'uuid': 'abc'}), format='json', data={})
    assert response.status_code == HTTP_401_UNAUTHORIZED

    response = api_client.get(reverse('user-addresses-list'), kwargs={'uuid': 'abc'}, format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_when_user_is_authenticated__they_can_create_multiple_addresses(
    authenticated_client,
    get_home_address_data,
    get_work_address_data,
    authenticated_user,
):
    _assert_address_and_user_address_counts(authenticated_user, 0, 0)

    for address_data in (get_home_address_data(), get_work_address_data()):
        response = authenticated_client.post(
            reverse('user-addresses-list'),
            format='json',
            data=address_data
        )
        user_address = UserAddress.objects.filter(user=authenticated_user).latest()

        assert response.status_code == HTTP_201_CREATED
        assert response.data == {
            'uuid': str(user_address.uuid),
            **address_data
        }

    _assert_address_and_user_address_counts(authenticated_user, 2, 2)


def test_when_user_tries_to_add_a_duplicated_address__bad_request_is_returned(
    authenticated_client,
    user_home_address_instance,
    get_home_address_data,
):
    _assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)

    response = authenticated_client.post(reverse('user-addresses-list'), format='json', data=get_home_address_data())

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert str(response.data['non_field_errors'][0]) == 'The fields user, address must make a unique set.'

    _assert_address_and_user_address_counts(user_home_address_instance.user, 1, 1)


@pytest.mark.usefixtures('home_address_instance')
def test_when_address_is_already_in_database__new_one_is_not_created(
    authenticated_client,
    get_home_address_data,
    authenticated_user,
):
    _assert_address_and_user_address_counts(authenticated_user, 1, 0)
    home_address_data = get_home_address_data('2nd Floor, Last Name')

    response = authenticated_client.post(
        reverse('user-addresses-list'),
        format='json',
        data=home_address_data
    )
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_201_CREATED
    assert response.data == {
        'uuid': str(user_address.uuid),
        **home_address_data
    }

    _assert_address_and_user_address_counts(authenticated_user, 1, 1)


def test_when_user_is_authenticated__they_can_retrieve_all_their_addresses(
    user_work_address_instance,
    get_work_address_data,
    user_home_address_instance,
    get_home_address_data,
    authenticated_client,
    other_user_home_address_instance,
):
    _assert_address_and_user_address_counts(user_home_address_instance.user, 2, 2)
    _assert_address_and_user_address_counts(other_user_home_address_instance.user, 2, 1)

    response = authenticated_client.get(reverse('user-addresses-list'), format='json')

    assert response.status_code == HTTP_200_OK
    assert response.data == [
        {'uuid': str(user_work_address_instance.uuid), **get_work_address_data()},
        {'uuid': str(user_home_address_instance.uuid), **get_home_address_data()}
    ]


def test_when_user_updates_a_main_part_of_the_address__a_new_address_is_created(
    authenticated_client,
    get_work_address_data,
    user_work_address_instance,
    authenticated_user
):
    _assert_address_and_user_address_counts(user_work_address_instance.user, 1, 1)
    work_address_data = get_work_address_data('New York Address 55')

    response = authenticated_client.put(
        reverse('user-addresses-detail', kwargs={'uuid': user_work_address_instance.uuid}),
        format='json',
        data=work_address_data
    )
    user_address = UserAddress.objects.get(user=authenticated_user)

    assert response.status_code == HTTP_200_OK
    assert response.data['uuid'] == str(user_work_address_instance.uuid)
    assert response.data == {
        'uuid': str(user_address.uuid),
        **work_address_data
    }

    _assert_address_and_user_address_counts(user_work_address_instance.user, 2, 1)


def _assert_address_and_user_address_counts(user, address_count, user_address_count):
    assert Address.objects.count() == address_count
    assert UserAddress.objects.filter(user=user).count() == user_address_count
