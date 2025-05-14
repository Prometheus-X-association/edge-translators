import json
from typing import Generator
import pytest
from pathlib import Path
from src.user.model import User
from src.rules.service import RuleService
from src.rules.model import Rule

TEST_DATA_FOLDER = Path(__file__).parent / "mocks" / "rule_service"
TEST_PROVIDER = "test"
current_user = User(username="test", email="test@test.io", password="changeme")

def load_mock_data(file_name, type):
    with open(f'{TEST_DATA_FOLDER}/{file_name}-{type}.json') as f:
        mock_data = json.load(f)
    return mock_data


@pytest.fixture(scope="function")
def rule_service() -> Generator[RuleService, None, None]:

    rule_service =  RuleService(current_user)

    yield rule_service
    
    rule_service.delete(refresh=True)

def test_find_success(rule_service: RuleService):
    payload = {
        "graph": [
            {"id": "mmr:rule-0"},
            {"id": "mmr:rule-1"},
            {"id": "mmr:rule-2"},
        ]
    }
    rule_service.upsert(payload, True)
    result = rule_service.find()
    assert result == payload

def test_find_not_found(rule_service: RuleService):
    result = rule_service.find()
    assert result == None

def test_upsert(rule_service: RuleService):
    payload = {
        "graph": [
            {"id": "mmr:rule-0"},
            {"id": "mmr:rule-1"},
            {"id": "mmr:rule-2"},
        ]
    }
    rule_service.upsert(payload, True)
    result = rule_service.find()
    assert result == payload

def test_delete(rule_service: RuleService):
    # First create and check initial state
    payload = {
        "graph": [
            {"id": "mmr:rule-0"},
            {"id": "mmr:rule-1"},
            {"id": "mmr:rule-2"},
        ]
    }
    rule_service.upsert(payload, True)
    result = rule_service.find()
    assert result == payload

    # Second delete and check result
    rule_service.delete(True)
    result = rule_service.find()
    assert result == None

# def test_apply():
#     pass

def test_browse_rules_tree():
    rule1 = Rule(
        id="mmr:rule-1",
        sourcePath="object.property1"
    )
    rule2 = Rule(
        id="mmr:rule-2",
        sourcePath="object.property2"
    )
    rule3 = Rule(
        id="mmr:rule-3",
        sourcePath="object.property3"
    )
    rules = [rule1, rule2, rule3]
    rules_tree = RuleService.generate_rules_tree(rules)
    result = RuleService.display_rules_tree(rules_tree)
    expected = "object\n\tproperty1\n\tproperty2\n\tproperty3"
    
    assert result == expected

def test_display_rules_tree():    
    rule1 = Rule(
        id="mmr:rule-1",
        sourcePath="object.property1"
    )
    rule2 = Rule(
        id="mmr:rule-2",
        sourcePath="object.property2"
    )
    rule3 = Rule(
        id="mmr:rule-3",
        sourcePath="object.property3"
    )
    rules = [rule1, rule2, rule3]
    rules_tree = RuleService.generate_rules_tree(rules)
    result = RuleService.display_rules_tree(rules_tree)
    expected = "object\n\tproperty1\n\tproperty2\n\tproperty3"
    
    assert result == expected

# def test_generate_rules_tree():
#     pass

def test_set_id(rule_service: RuleService):
    result = rule_service.set_id()
    expected = f"rule:provider/{TEST_PROVIDER}"
    assert result == expected

def test_generate_id(rule_service: RuleService):
    instance = {
        "type": "soo:Test",
        "__counter__": "1"
    }
    value = "testvalue"
    result = rule_service.generate_id(instance, value)
    expected = f"test:provider/{current_user.username}/value/{value}"
    assert result == expected

# def test_check_instance():
#     pass

# def test_get_last_instance():
#     pass

# def test_get_instance():
#     pass

# def test_get_documents_from_files():
#     pass

def test_get_field_name(rule_service: RuleService):
    field = "soo:hasfield1"
    result = rule_service.get_field_name(field)
    expected = "field1"
    assert result == expected
    
    field = "soo:field2"
    result = rule_service.get_field_name(field)
    expected = "field2"
    assert result == expected
    
    field = "skos:field3"
    result = rule_service.get_field_name(field)
    expected = "field3"
    assert result == expected

# def test_fill_with_document():
#     pass

# def test_generate_instances_by_tree():
#     pass

# def test_apply_tree_rules_to_document():
#     pass
