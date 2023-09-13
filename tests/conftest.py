import pytest
from datetime import datetime, timedelta
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from event_manager_test.app.models import Event


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_dict():
    return {
        "username": "test",
        "password": "test12345",
        "password_copy": "test12345",
        "email": "test@test.it"
    }

@pytest.fixture
def event_dict():
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return {
        "name": "test",
        "start_datetime": now + timedelta(days=1),
        "end_datetime": now + timedelta(days=2),
        "capacity": 10
    }

@pytest.fixture
def loaded_db(user_dict, event_dict):
    del user_dict['password_copy']

    user = User.objects.create(**user_dict)
    user.set_password(user_dict.get('password'))
    user.save()

    event = Event.objects.create(**event_dict, owner_id=user.id)

    yield
    user.delete()
    event.delete()

@pytest.fixture
def logged_api_client(api_client: APIClient, user_dict: dict, loaded_db):
    refresh = RefreshToken.for_user(
        User.objects.get(username=user_dict.get('username'))
    )

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return api_client
