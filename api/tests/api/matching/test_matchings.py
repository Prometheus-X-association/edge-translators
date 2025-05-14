import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.user.model import User, StatusEnum, RoleEnum
from src.user.service import UserService
from src.auth.model import Token
from src.auth.dependencies import get_current_user

TEST_ROUTE_AUTH_TOKEN = "/auth/token"
TEST_ROUTE_MATCHING = "/matching"

TEST_DATA_FOLDER = Path(__file__).parent

def load_mock_data(file_name):
    with open(f'{TEST_DATA_FOLDER}/matching-{file_name}.json') as f:
        mock_data = json.load(f)
    return mock_data

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
        role=RoleEnum.ROLE_PROVIDER,
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

def test_get_matching_experience_validated_true(client: TestClient, mocker):
    fake_es_response = load_mock_data("esco_experiences_validated")
    mocked_es_client = mocker.patch("src.matching.service.ElasticsearchClient").return_value.client
    mocked_es_client.search.return_value = fake_es_response
    response = client.get(TEST_ROUTE_MATCHING, params={"validated": True, "concept_type": "experience", "framework": "esco"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [v['_source'] for v in fake_es_response['hits']['hits']]

def test_get_matching_experience_validated_false(client: TestClient, mocker):
    fake_es_response = load_mock_data("esco_experiences_not_validated")
    mocked_es_client = mocker.patch("src.matching.service.ElasticsearchClient").return_value.client
    mocked_es_client.search.return_value = fake_es_response
    response = client.get(TEST_ROUTE_MATCHING, params={"validated": False, "concept_type": "experience", "framework": "esco"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [v['_source'] for v in fake_es_response['hits']['hits']]

def test_get_matching_skill_validated_false(client: TestClient, mocker):
    fake_es_response = load_mock_data("esco_skills_not_validated")
    mocked_es_client = mocker.patch("src.matching.service.ElasticsearchClient").return_value.client
    mocked_es_client.search.return_value = fake_es_response
    response = client.get(TEST_ROUTE_MATCHING, params={"validated": False, "concept_type": "experience", "framework": "esco"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [v['_source'] for v in fake_es_response['hits']['hits']]