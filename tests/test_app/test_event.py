import pytest
from rest_framework import status
from rest_framework.test import APIClient

from event_manager_test.app.models import Event

# These tests are missing the error handling tests, cause: lack of time.

@pytest.mark.django_db
def test_create(
    logged_api_client: APIClient,
    event_dict: dict
):
    response = logged_api_client.post(
        '/api/events/',
        event_dict,
        format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_get_all(logged_api_client: APIClient):
    response = logged_api_client.get('/api/events/')

    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert len(json_response) == 1
    assert json_response[0].get('id') == 1

@pytest.mark.django_db
def test_get_by_id(logged_api_client: APIClient):
    first_event = Event.objects.all().first()
    response = logged_api_client.get(f'/api/events/{first_event.id}/')

    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert json_response
    assert json_response.get('id') == 1

@pytest.mark.django_db
def test_get_filters(logged_api_client: APIClient, event_dict: dict):
    # NICE TO HAVE:
    # Increase test granularity by checking the result of each filter
    filters = {
        'user_only': True,
        'past_event_only': True,
        'future_event_only': True,
        'date': event_dict.get('start_datetime'),
        'e_type': Event.Type.MEETUP.value,
        'status': Event.Status.CONFIRMED.value
    }

    for key, value in filters.items():
        response = logged_api_client.get(f'/api/events/?{key}={value}')

        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_put(logged_api_client: APIClient, event_dict: dict):
    event_dict['owner'] = 1
    event_dict['name'] = 'new name test'

    first_event = Event.objects.all().first()

    response = logged_api_client.put(
        f'/api/events/{first_event.id}/',
        event_dict,
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK

    first_event = Event.objects.all().first()

    assert first_event.name == event_dict.get('name')

@pytest.mark.django_db
def test_patch(logged_api_client: APIClient, event_dict: dict):
    first_event = Event.objects.all().first()

    response = logged_api_client.patch(
        f'/api/events/{first_event.id}/',
        {
            'name': 'updated by patch'
        },
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK

    first_event = Event.objects.all().first()

    assert first_event.name == 'updated by patch'

@pytest.mark.django_db
def test_delete(logged_api_client: APIClient, event_dict: dict):
    first_event = Event.objects.all().first()

    response = logged_api_client.delete(f'/api/events/{first_event.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Event.objects.all().first()
