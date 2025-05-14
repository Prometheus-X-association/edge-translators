import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.auth.model import Token

TEST_ROUTE_AUTH_TOKEN="/auth/token"

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_auth_token_success(client: TestClient, mocker):
    fake_token = Token(
        access_token="faketoken",
        expires_in=3600,
        token_type="bearer",
    )
    mocker.patch("src.auth.service.AuthService.authenticate", return_value=fake_token)
    response = client.post(
        TEST_ROUTE_AUTH_TOKEN,
        data={
            "grant_type": "password",
            "username": "test",
            "password": "changeme",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert isinstance(response.json()["access_token"], str)
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 3600

def test_auth_token_unauthorized(client: TestClient, mocker):
    mocker.patch("src.auth.service.AuthService.authenticate", return_value=False)
    response = client.post(
        TEST_ROUTE_AUTH_TOKEN,
         data={
            "grant_type": "password",
            "username": "wronguser",
            "password": "wrongpassword",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Unauthorized access'}
