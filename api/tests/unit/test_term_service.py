import json
from pathlib import Path
import pytest
from src.user.model import User
from src.term.service import TermService
from src.auth.dependencies import CurrentUserdep


collection_id = 'test:fake/collection/1'
collection_label = 'Test fake collection'
collection_language = 'en'

concepts = [
    {
        'concept_id': 'test:fake/concept/1',
        'concept_pref_label': 'Test fake concept 2',
    },
    {
        'concept_id': 'test:fake/concept/2',
        'concept_pref_label': 'Test fake concept 2',
    }
]

TEST_DATA_FOLDER = Path(__file__).parent / "mocks" / "term_service"

current_user = User(username="test", email="test@test.io", password="changeme")


def load_mock_data(file_name):
    with open(f'{TEST_DATA_FOLDER}/{file_name}-input.json') as f:
        input_data = json.load(f)
    with open(f'{TEST_DATA_FOLDER}/{file_name}-expected.json') as f:
        expected_data = json.load(f)
    return [input_data, expected_data]

@pytest.fixture(scope="module")
def term_service() -> TermService:
    return TermService(current_user)

def test_create_collection(term_service: TermService):
    generated_data = term_service.create_collection(collection_id, collection_label)
    
    assert generated_data['id'] == collection_id

def test_create_concept(term_service: TermService):
    # 1/ create a concept associated with the previous collection
    for cp in concepts: 
        term_service.create_concept(cp['concept_id'], cp['concept_pref_label'], collection_id)
        
    # 2/ test that the collection has 2 members
    collection = term_service.get_collection(collection_id)
    assert collection != None
    assert len(collection['member']) == 2
    
    # 3/ update the first concept 
    cp = concepts[0]
    term_service.create_concept(cp['concept_id'], cp['concept_pref_label'], collection_id)
    
    # 4/ test that the collection still have 2 members (no duplicates after update)
    collection = term_service.get_collection(collection_id)
    assert collection != None
    assert len(collection['member']) == 2

def test_delete_concept(term_service: TermService):
    term_service.delete_concept(concepts[0]["concept_id"])
    assert term_service.get_concept(concepts[0]['concept_id']) is None
    
def test_delete_collection(term_service: TermService):
    term_service.delete_collection(collection_id)
    assert term_service.get_collection(collection_id) is None

@pytest.mark.parametrize(
    ("type"),
    [
        ("skill_value_to_scale_mapping"),
        ("polarity_mapping"),
        ("family_mapping")
    ]
)
def test_generate(term_service: TermService, type: str):
    input_data, expected_data = load_mock_data(f"term_service-{type}")
    generated_data = term_service.generate(input_data)
    assert generated_data == expected_data 

