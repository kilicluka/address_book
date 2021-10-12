import pytest
from rest_framework.test import APIClient

from address.models import Address, UserAddress


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
def authenticated_user(django_user_model):
    return django_user_model.objects.create(username='authenticated_user', password='authenticated_password')


@pytest.fixture
def authenticated_client(authenticated_user, api_client):
    api_client.force_authenticate(authenticated_user)
    return api_client


@pytest.fixture
def home_address_instance(get_home_address_data):
    address_data = dict(get_home_address_data())
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
def work_address_instance(get_work_address_data):
    address_data = dict(get_work_address_data())
    address_data.pop('address_two')
    return Address.objects.create(**address_data)


@pytest.fixture
def user_work_address_instance(authenticated_user, work_address_instance, get_work_address_data):
    return UserAddress.objects.create(
        user=authenticated_user,
        address=work_address_instance,
        additional_address_data=get_work_address_data()['address_two']
    )


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


def assert_address_and_user_address_counts(user, address_count, user_address_count):
    assert Address.objects.count() == address_count
    assert UserAddress.objects.filter(user=user).count() == user_address_count
