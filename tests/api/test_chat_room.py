import pytest
from tests.factory import ChatRoomFactory


@pytest.mark.django_db
def test_list_chat_rooms(user, client):
    login = client.post(
        "/api/v1/login/", {"username": user.username, "password": "password"}
    )

    ChatRoomFactory.create_batch(3)

    response = client.get(
        "/api/v1/rooms/", headers={"Authorization": f"Bearer {login.data['access']}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.django_db
def test_create_chat_room(user, client):
    login = client.post(
        "/api/v1/login/", {"username": user.username, "password": "password"}
    )
    rooms = client.get(
        "/api/v1/rooms/", headers={"Authorization": f"Bearer {login.data['access']}"}
    )

    assert rooms.status_code == 200
    assert len(rooms.data) == 0

    response = client.post(
        "/api/v1/rooms/",
        {"name": "TestRoom"},
        headers={"Authorization": f"Bearer {login.data['access']}"},
    )

    assert response.status_code == 201
    assert response.data["name"] == "TestRoom"

    rooms = client.get(
        "/api/v1/rooms/", headers={"Authorization": f"Bearer {login.data['access']}"}
    )

    assert len(rooms.data) == 1


@pytest.mark.django_db
def test_create_chat_room_unauthenticated(client):
    response = client.post("/api/v1/rooms/", {"name": "TestRoom"})

    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_delete_chat_room(user, client):
    login = client.post(
        "/api/v1/login/", {"username": user.username, "password": "password"}
    )
    room = ChatRoomFactory()

    response = client.delete(
        f"/api/v1/rooms/{room.id}/",
        headers={"Authorization": f"Bearer {login.data['access']}"},
    )

    assert response.status_code == 204

    rooms = client.get(
        "/api/v1/rooms/", headers={"Authorization": f"Bearer {login.data['access']}"}
    )

    assert len(rooms.data) == 0
