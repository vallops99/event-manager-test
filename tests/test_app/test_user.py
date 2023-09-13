import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_signup(api_client: APIClient, user_dict: dict):
    response = api_client.post('/api/signup/', user_dict, format='json')
    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED

    db_user = User.objects.all().first()

    assert db_user.username == user_dict.get('username')
    assert db_user.email == user_dict.get('email')

@pytest.mark.django_db
def test_login(api_client: APIClient, user_dict: dict, loaded_db):
    response = api_client.post('/api/login/', {
        'username': user_dict['username'],
        'password': user_dict['password']
    })

    assert response.status_code == status.HTTP_200_OK

# FYI: Next tests will check for error handling.

@pytest.mark.django_db
def test_signup_bad_password(api_client: APIClient, user_dict: dict):
    # Test bad password copy
    user_dict['password_copy'] = user_dict['password_copy'] + '1'

    response = api_client.post('/api/signup/', user_dict, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_signup_bad_email(api_client: APIClient, user_dict: dict):
    # Test bad email
    user_dict['email'] = 'test@testcom'

    response = api_client.post('/api/signup/', user_dict, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_signup_bad_username_unique(
    api_client: APIClient,
    user_dict: dict,
    loaded_db
):
    response = api_client.post('/api/signup/', user_dict, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_signup_bad_password_length(api_client: APIClient, user_dict: dict):
    user_dict['password'] = 'small'
    user_dict['password_copy'] = 'small'
    response = api_client.post('/api/signup/', user_dict, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_bad_credentials(api_client: APIClient, user_dict: dict):
    response = api_client.post('/api/login/', {
        'username': 'will_not_work',
        'password': '12345'
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
