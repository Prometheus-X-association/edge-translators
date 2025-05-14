import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.auth.model import Token
from src.user.model import User, StatusEnum, RoleEnum
from src.user.service import UserService
from src.auth.dependencies import get_current_user

TEST_ROUTE_AUTH_TOKEN="/auth/token"
TEST_ROUTE_TRANSFORM="/transform"

TEST_DATA_FOLDER = Path(__file__).parent

def load_mock_data(file_name):
    with open(f'{TEST_DATA_FOLDER}/{file_name}.json') as f:
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

def test_transform_success(client: TestClient, mocker):
    input_data = load_mock_data("input_data")
    output_data = load_mock_data("output_data")

    mocked_es_client = mocker.patch("src.rules.service.ElasticsearchClient").return_value.client
    mocked_es_client.get.return_value = {"_source": load_mock_data("rules")}

    mocked_es_client = mocker.patch("src.matching.service.ElasticsearchClient").return_value.client
    mocked_es_client.get.return_value = None
    mocked_es_client.index.return_value = None



    mocked_es_client = mocker.patch("src.matching.suggestion_service.ElasticsearchClient").return_value.client

    mocked_es_client.search.side_effect = [
        load_mock_data("search_job_developpeur-full-stack"),
        load_mock_data("search_job_ingenieur-en-machine-learning"),
        load_mock_data("search_job_specialiste-en-cybersecurite"),
        load_mock_data("search_skill_analyse"),
        load_mock_data("search_skill_collaboration"),
        load_mock_data("search_skill_communication"),
        load_mock_data("search_skill_curiosite"),
        load_mock_data("search_skill_esprit-d-equipe"),
        load_mock_data("search_skill_firewall"),
        load_mock_data("search_skill_gestion-du-temps"),
        load_mock_data("search_skill_javascript"),
        load_mock_data("search_skill_kali-linux"),
        load_mock_data("search_skill_node-js"),
        load_mock_data("search_skill_pensee-critique"),
        load_mock_data("search_skill_python"),
        load_mock_data("search_skill_react"),
        load_mock_data("search_skill_scikit-learn"),
        load_mock_data("search_skill_tensorflow"),
        load_mock_data("search_skill_travail-d-equipe"),
        load_mock_data("search_skill_vigilance"),
        load_mock_data("search_skill_wireshark")
    ]


    response = client.post(
        TEST_ROUTE_TRANSFORM,
        json={"document": input_data},
        params={"target_framework": "esco", "language_source": "fr", "language_target": "en"},
    )
    assert response.status_code == 200
    assert response.json() == output_data

def test_transform_invalid_document(client: TestClient):
    response = client.post(
        TEST_ROUTE_TRANSFORM,
        json={},
        params={"target_framework": "esco", "language_source": "fr", "language_target": "en"},
    )
    assert response.status_code == 422

def test_transform_missing_document(client: TestClient):
    response = client.post(
        TEST_ROUTE_TRANSFORM,
        params={"target_framework": "esco", "language_source": "fr", "language_target": "en"},
    )
    assert response.status_code == 422

def test_transform_rules_not_found(client: TestClient, mocker):
    input_data = load_mock_data("input_data")

    mocked_es_client = mocker.patch("src.rules.service.ElasticsearchClient").return_value.client
    mocked_es_client.get.return_value = None

    response = client.post(
        TEST_ROUTE_TRANSFORM,
        json={"document": input_data},
        params={"target_framework": "esco", "language_source": "fr", "language_target": "en"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Missing rules"}
