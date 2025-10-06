import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def user():
    User = get_user_model()
    u = User.objects.create_user(
        phone="+79990000001",
        username="max1",
        password="S3cure_pass!",
    )
    u.is_active = True
    u.save(update_fields=["is_active"])
    return u


def test_obtain_token_success(api, user):
    url = reverse("auth")
    response = api.post(
        url, {"phone": user.phone, "password": "S3cure_pass!"}, format="json"
    )
    assert response.status_code == 200, response.content
    data = response.json()
    assert "access" in data and "refresh" in data


def test_obtain_token_bad_credentials(api, user):
    url = reverse("auth")
    response = api.post(url, {"phone": user.phone, "password": "wrong"}, format="json")
    assert response.status_code in (400, 401), response.content


def test_refresh_token_success(api, user):
    obtain_url = reverse("auth")
    tokens = api.post(
        obtain_url, {"phone": user.phone, "password": "S3cure_pass!"}, format="json"
    ).json()

    refresh_url = reverse("auth_refresh")
    response = api.post(refresh_url, {"refresh": tokens["refresh"]}, format="json")
    assert response.status_code == 200, response.content
    assert "access" in response.json()
