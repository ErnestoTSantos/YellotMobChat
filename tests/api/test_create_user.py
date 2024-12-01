import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
def test_create_user_success(client):
    data = {
        "username": "usertest",
        "email": "usertest@example.com",
        "first_name": "Test",
        "last_name": "LastName",
        "password": "Password@123",
        "password_confirm": "Password@123",
    }

    response = client.post("/api/v1/register/", data)

    assert response.status_code == status.HTTP_201_CREATED

    created_user = User.objects.get(username="usertest")

    assert created_user.email == "usertest@example.com"
    assert created_user.first_name == "Test"
    assert created_user.last_name == "LastName"


@pytest.mark.django_db
def test_create_user_failure_missing_fields(client):
    data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "first_name": "Test2",
        "last_name": "User2",
    }

    response = client.post("/api/v1/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["password"][0] == "This field is required."
    assert response.data["password_confirm"][0] == "This field is required."


@pytest.mark.django_db
def test_create_user_failure_invalid_email(client):
    data = {
        "username": "testuser3",
        "email": "invalidemail",
        "first_name": "Test3",
        "last_name": "User3",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
    }

    response = client.post("/api/v1/register/", data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0] == "Enter a valid email address."


@pytest.mark.django_db
def test_create_user_failure_weak_password(client):
    data = {
        "username": "userweakpassword",
        "email": "weakpassword@example.com",
        "first_name": "Weak",
        "last_name": "Password",
        "password": "123",
        "password_confirm": "123",
    }

    response = client.post("/api/v1/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_failure_username_exists(client):
    User.objects.create_user(
        username="existinguser", email="existing@example.com", password="Password@123"
    )

    data = {
        "username": "existinguser",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "Password@123",
        "password_confirm": "Password@123",
    }

    response = client.post("/api/v1/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["username"][0] == "A user with that username already exists."
