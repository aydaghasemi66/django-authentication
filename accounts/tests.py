from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, TrainerProfile, StudentProfile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRegistration:
    def test_register_creates_user(self, api_client):
        url = reverse("register")
        response = api_client.post(url, {
            "email": "newuser@example.com",
            "password": "strongpass123",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_register_fails_without_email(self, api_client):
        url = reverse("register")
        response = api_client.post(url, {"password": "strongpass123"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_fails_with_short_password(self, api_client):
        url = reverse("register")
        response = api_client.post(url, {
            "email": "user2@example.com",
            "password": "123",  # کمتر از min_length=8
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_tokens(self, api_client):
        User.objects.create_user(email="login@example.com", password="pass12345")
        url = reverse("login")
        response = api_client.post(url, {
            "email": "login@example.com",
            "password": "pass12345",
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_fails_with_wrong_password(self, api_client):
        User.objects.create_user(email="login2@example.com", password="pass12345")
        url = reverse("login")
        response = api_client.post(url, {
            "email": "login2@example.com",
            "password": "wrongpass",
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCompleteProfile:
    def test_complete_profile_as_student(self, api_client):
        user = User.objects.create_user(email="student@example.com", password="pass12345")
        api_client.force_authenticate(user=user)

        url = reverse("complete_profile")
        response = api_client.patch(url, {
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "role": "student",
        })

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.is_profile_complete is True
        assert StudentProfile.objects.filter(user=user).exists()

    def test_complete_profile_as_trainer(self, api_client):
        user = User.objects.create_user(email="trainer@example.com", password="pass12345")
        api_client.force_authenticate(user=user)

        url = reverse("complete_profile")
        response = api_client.patch(url, {
            "first_name": "Ali",
            "last_name": "Rezaei",
            "role": "trainer",
        })

        assert response.status_code == status.HTTP_200_OK
        assert TrainerProfile.objects.filter(user=user).exists()

    def test_complete_profile_requires_authentication(self, api_client):
        url = reverse("complete_profile")
        response = api_client.patch(url, {"role": "student"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestIsProfileComplete:
    def test_incomplete_profile_returns_false(self, api_client):
        user = User.objects.create_user(email="incomplete@example.com", password="pass12345")
        api_client.force_authenticate(user=user)

        url = reverse("me")
        response = api_client.get(url)

        assert response.data["is_profile_complete"] is False