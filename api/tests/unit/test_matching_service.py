import json
from typing import Generator
import pytest
from pathlib import Path
from src.user.model import User
from src.transform.model import TransformConfig
from src.matching.service import MatchingService
from src.utils.md5 import md5

TEST_DATA_FOLDER = Path(__file__).parent / "mocks" / "matching_service"

current_user = User(username="test", email="test@test.io", password="changeme")
transform_config = TransformConfig(
    framework="esco",
    language_source="fr",
    language_target="en"
)
def load_mock_data(file_name, type):
    with open(f'{TEST_DATA_FOLDER}/{file_name}-{type}.json') as f:
        mock_data = json.load(f)
    return mock_data

@pytest.fixture(scope="function")
def matching_service() -> Generator[MatchingService, None, None]:
    matching_service =  MatchingService(current_user)

    yield matching_service
    
    matching_service.delete_all(True)

def test_find(matching_service: MatchingService):
    id = "test_id"
    payload = {"id": id, "provider": current_user.username}
    matching_service.create(id, payload, True)
    result = matching_service.find(id)
    assert result == payload

def test_find_not_found(matching_service: MatchingService):
    id = "test_id"
    result = matching_service.find(id)
    assert result is None

def test_update_success(matching_service: MatchingService):
    id = "test_id"
    initial_payload = {"id": id, "provider": current_user.username, "test": "intial value"}
    matching_service.create(id, initial_payload, True)
    result = matching_service.find(id)
    assert result == initial_payload
    
    changes = {"test": "some dummy changes"}
    matching_service.update(id, changes, True)
    result = matching_service.find_all()
    new_document = {'_id': 'test_id', **initial_payload, **changes}
    assert result == [new_document]

def test_update_exception(matching_service: MatchingService):
    with pytest.raises(Exception):
        matching_service.update(None, {})

def test_find_validated(matching_service: MatchingService):
    id = "test_id"
    payload = {"id": id, "provider": current_user.username, "match": {"validated": 1}}
    matching_service.create(id, payload, True)
    result = matching_service.find_some()
    payload["_id"] = id
    assert result == [payload]

def test_find_not_validated(matching_service: MatchingService):
    id = "test_id"
    payload = {
        "id": id,
        "provider": current_user.username,
        "match": {"validated": 0},
        "suggestions": [
            {"validated": 0},
            {"validated": 0}
        ]
    }
    matching_service.create(id, payload, True)
    result = matching_service.find_some()
    payload["_id"] = id
    assert result == [payload]

def test_find_all(matching_service: MatchingService):
    expected_result = []
    for i in range(1, 10):
        id = f"test_id_{i}"
        payload = {"id": id, "provider": current_user.username}
        matching_service.create(id, payload, True)
        payload["_id"] = id
        expected_result.append(payload)
    
    result = matching_service.find_all()

    assert sorted(result, key=lambda x: x['id']) == sorted(expected_result, key=lambda x: x['id'])

def test_create(matching_service: MatchingService):
    id = "test_id"
    payload = {"id": id, "provider": current_user.username}
    matching_service.create(id, payload, True)
    result = matching_service.find(id)
    assert result == payload

def test_delete_success(matching_service: MatchingService):
    id = "test_id"
    initial_payload = {"id": id, "provider": current_user.username, "test": "intial value"}
    matching_service.create(id, initial_payload, True)
    result = matching_service.find(id)
    assert result == initial_payload
    
    matching_service.delete(id, True)
    result = matching_service.find_all()
    assert result == []

def test_delete_exception(matching_service: MatchingService):
    with pytest.raises(Exception):
        matching_service.delete(None, True)

def test_delete_all_success(matching_service: MatchingService):
    expected_result = []
    for i in range(1, 10):
        id = f"test_id_{i}"
        payload = {"id": id, "provider": current_user.username}
        matching_service.create(id, payload, True)
        payload["_id"] = id
        expected_result.append(payload)
    
    result = matching_service.find_all()

    assert sorted(result, key=lambda x: x['id']) == sorted(expected_result, key=lambda x: x['id'])
    
    matching_service.delete_all(True)
    result = matching_service.find_all()
    assert result == []

def test_delete_all_exception(matching_service: MatchingService):
    with pytest.raises(Exception):
        matching_service.delete_all("bad_parameter_value")

def test_exists_true(matching_service: MatchingService):
    id = "test_id"
    payload = {"id": id, "provider": current_user.username}
    
    result = matching_service.exists(id)
    assert result == False

    matching_service.create(id, payload, True)
    result = matching_service.exists(id)
    assert result == True

def test_exists_false(matching_service: MatchingService):
    id = "test_id"
    result = matching_service.exists(id)
    assert result == False

def test_set_id(matching_service: MatchingService):

    concept_pref_label=f"concept_pref_label"
    result = matching_service.set_es_id(concept_pref_label)


    prefix = "match:"
    provider = f"provider/{current_user.username}/"
    framework = f"framework/{transform_config.framework}/"
    pref_label = f"label/{md5(concept_pref_label)}/"
    language_source = f"slang/{transform_config.language_source}/"
    language_target = f"tlang/{transform_config.language_target}"
    expected_result = prefix + provider + framework + pref_label + language_source + language_target

    assert result == expected_result

def test_set_object_with_one_validated(matching_service: MatchingService):
    id=f"test_id"
    concept_type = "soo:Experience"
    concept_pref_label = "Développeur web"
    concept_pref_description = "Conçoit et développe des application web en PHP (backend) et Javascript (frontend)."
    suggestions = []
    suggestion1 = {
        "id": "test_id_suggestion_1",
        "type": "match:suggestion",
        "target": {},
        "score": 3.3740309,
        "validated": MatchingService.STATUS_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestion2 = {
        "id": "test_id_suggestion_2",
        "type": "match:suggestion",
        "target": {},
        "score": 2.2040242,
        "validated": MatchingService.STATUS_NOT_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestion3 = {
        "id": "test_id_suggestion_3",
        "type": "match:suggestion",
        "target": {},
        "score": 1.6740303,
        "validated": MatchingService.STATUS_NOT_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestions.append(suggestion1)
    suggestions.append(suggestion2)
    suggestions.append(suggestion3)
    
    result = matching_service.set_object(
        concept_type,
        concept_pref_label,
        concept_pref_description,
        id,
        suggestions
    )
    expected = load_mock_data("test_set_object_with_one_validated", "expected")

    result.pop('date', None)

    assert result == expected

def test_set_object_without_validated(matching_service: MatchingService):
    id=f"test_id"
    concept_type = "soo:Experience"
    concept_pref_label = "Développeur web"
    concept_pref_description = "Conçoit et développe des application web en PHP (backend) et Javascript (frontend)."
    suggestions = []
    suggestion1 = {
        "id": "test_id_suggestion_1",
        "type": "match:suggestion",
        "target": {},
        "score": 3.3740309,
        "validated": MatchingService.STATUS_NOT_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestion2 = {
        "id": "test_id_suggestion_2",
        "type": "match:suggestion",
        "target": {},
        "score": 2.2040242,
        "validated": MatchingService.STATUS_NOT_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestion3 = {
        "id": "test_id_suggestion_3",
        "type": "match:suggestion",
        "target": {},
        "score": 1.6740303,
        "validated": MatchingService.STATUS_NOT_VALIDATED,
        "framework": transform_config.framework,
        "mappingType": "skos:exactMatch",
    }
    suggestions.append(suggestion1)
    suggestions.append(suggestion2)
    suggestions.append(suggestion3)
    
    result = matching_service.set_object(
        concept_type,
        concept_pref_label,
        concept_pref_description,
        id,
        suggestions
    )

    expected = load_mock_data("test_set_object_without_validated", "expected")

    result.pop('date', None)

    assert result == expected

def test_generate_new_matching(matching_service: MatchingService, mocker):
    concept_pref_label = "Ingénieur informatique"
    id = matching_service.set_es_id(concept_pref_label)

    assert matching_service.find(id) == None
    assert matching_service.find_all() == []

    payload = {
        "graph": [
            {
                "id": "test_id",
                "type": "soo:Experience",
                "__matching__": {
                    "sourceValue": concept_pref_label,
                    "provider": current_user.username,
                    "subtype": "job",
                    "language": "en"
                },
            },
        ]
    }

    mocked_es_client = mocker.patch("src.matching.suggestion_service.ElasticsearchClient").return_value.client
    mocked_es_client.search.return_value = load_mock_data("test_generate_new_matching_es_search", "expected")

    result = matching_service.generate(payload, transform_config, True)
    inserted = matching_service.find_all()
    expected = load_mock_data("test_generate_new_matching", "expected")
    
    assert inserted == expected
    del expected[0]["_id"] # workaround, but later id and _id need to be better handle
    assert result["graph"] == expected


def test_generate_matching_already_exists(matching_service: MatchingService):
    concept_pref_label = "Ingénieur informatique"
    id = matching_service.set_es_id(concept_pref_label)

    assert matching_service.find(id) == None
    assert matching_service.find_all() == []

    payload = {"id": id, "provider": current_user.username}
    matching_service.create(id, payload, True)

    payload = {
        "graph": [
            {
                "id": "test_id",
                "provider": "test",
                "__matching__": {
                    "sourceValue": concept_pref_label,
                    "provider": current_user.username,
                    "subtype": "job",
                    "language": "fr"
                },
            },
        ]
    }

    result = matching_service.generate(payload, transform_config, True)
    inserted = matching_service.find_all()

    expected = load_mock_data("test_generate_matching_already_exists", "expected")
    assert inserted ==  expected
    del expected[0]["_id"] # workaround, but later id and _id need to be better handle
    assert result["graph"] == expected
