import time
from typing import List
import pytest
from src.user.model import User
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch
from src.user.model import User, StatusEnum, RoleEnum
from src.user.service import UserService
from src.auth.model import Token
from src.auth.dependencies import get_current_user

@pytest.fixture(autouse=True)
def mock_auth(mocker):
    fake_token = Token(
        access_token="faketoken",
        expires_in=3600,
        token_type="bearer",
    )
    mocker.patch("src.auth.service.AuthService.authenticate", return_value=fake_token)

    fake_user = User(
        id=1,
        username="test",
        email="test@email.io",
        role=RoleEnum.ROLE_ADMIN,
        password=UserService.get_password_hash("changeme"),
        status=StatusEnum.ACTIVE
    )

    async def fake_get_current_user():
        return fake_user

    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    with TestClient(app) as client:
        client.headers = {"Authorization": "Bearer faketoken"}
        yield client

def test_get_me(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_user(client: TestClient, mocker):
    fake_user = {
        "id": 1,
        "username": "test",
        "email": "test@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }

    mocker.patch("src.user.repository.UserRepository.find", return_value=User(**fake_user))

    response = client.get("/users/1")
    assert response.status_code == 200
    assert fake_user == response.json()

def test_get_user_not_found(client: TestClient, mocker):
    mocker.patch("src.user.repository.UserRepository.find", return_value=None)
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_users(client: TestClient, mocker):
    fake_users = [{
        "id": 1,
        "username": "test",
        "email": "test@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    },{
        "id": 2,
        "username": "test2",
        "email": "test2@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }]
    mocker.patch("src.user.repository.UserRepository.find_all", return_value=(2, [User(**fake_user) for fake_user in fake_users]))
    response = client.get("/users?page=1&per_page=5&sort=id&order=ASC")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    assert len(response.json()) == 2
    assert response.json() == fake_users

def test_create_user(client: TestClient, mocker):
    fake_user = {
        "id": 1,
        "username": "test",
        "email": "test@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }

    mocker.patch("src.user.repository.UserRepository.create", return_value=User(**fake_user))
    response = client.post("/users", json=fake_user)
    assert response.status_code == 200
    assert response.json() == fake_user

def test_update_user(client: TestClient, mocker):
    fake_user = {
        "id": 1,
        "username": "test",
        "email": "test_modified@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }
    mocker.patch("src.user.repository.UserRepository.find", return_value=User(**fake_user))
    mocker.patch("src.user.repository.UserRepository.update", return_value=User(**fake_user))
    response = client.patch("/users/3", json=fake_user)
    assert response.status_code == 200
    assert response.json() == fake_user

def test_delete_user(client: TestClient, mocker):
    fake_user = {
        "id": 1,
        "username": "test",
        "email": "test_modified@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }
    mocker.patch("src.user.repository.UserRepository.find", return_value=User(**fake_user))
    mocker.patch("src.user.repository.UserRepository.delete", return_value=User(**fake_user))
    response = client.delete("/users/24")
    assert response.status_code == 200
    assert response.json() == True

def test_delete_user_not_found(client: TestClient, mocker):
    fake_user = {
        "id": 1,
        "username": "test",
        "email": "test_modified@example.io",
        "role": "ROLE_PROVIDER",
        "password": UserService.get_password_hash("changeme"),
        "failed_login_attempts": 0,
        "status": 1,
        "logged_in": False,
        "created_at": "2025-04-28T15:50:17.405786",
        "updated_at": "2025-04-28T15:50:17.405790",
        "deleted_at": None
    }
    mocker.patch("src.user.repository.UserRepository.find", return_value=None)
    mocker.patch("src.user.repository.UserRepository.delete", return_value=User(**fake_user))
    response = client.delete("/users/24")
    assert response.status_code == 404
