import json
import time
from typing import Dict
from elasticsearch import BadRequestError
from slugify import slugify

from ..esco_helper.client import EscoHelperClient
from ..elasticsearch.client import ElasticsearchClient
from ..transform.model import TransformConfig
from ..embedding.service import EmbeddingService
from ..utils.md5 import md5

class SuggestionService:

    ELASTICSEARCH_INDEX_SEARCH = "search-ariane-jobs-and-skills"
    
    LIMIT_SUGGESTIONS = 5

    FRAMEWORK_NAME_ROME = "rome"
    SOURCE_FIELDS_ROME = ["id", "pref_label__value", "pref_label__language", "broader"]
    TYPE_ENUMS_SKILL_ROME = ["rome:onto/Competency", "rome:onto/KnowHowDomain"]
    TYPE_ENUMS_JOB_ROME = ["rome:onto/Employment/Position"]

    FRAMEWORK_NAME_ESCO = "esco"
    SOURCE_FIELDS_ESCO = ["id", "pref_label__value", "pref_label__language"]
    TYPE_ENUMS_SKILL_ESCO = ["esco:Skill"]
    TYPE_ENUMS_JOB_ESCO = ["esco:Occupation"]

    FRAMEWORKS_CONFIG = {
        FRAMEWORK_NAME_ROME: {
            "source_fields": SOURCE_FIELDS_ROME,
            "type_enums": {
                "skill": TYPE_ENUMS_SKILL_ROME,
                "job": TYPE_ENUMS_JOB_ROME
            }
        },
        FRAMEWORK_NAME_ESCO: {
            "source_fields": SOURCE_FIELDS_ESCO,
            "type_enums": {
                "skill": TYPE_ENUMS_SKILL_ESCO,
                "job": TYPE_ENUMS_JOB_ESCO
            }
        }
    }

    def __init__(self, transform_config: TransformConfig):
        self.es_client = ElasticsearchClient().client
        self.embedding_service = EmbeddingService()
        self.esco_helper_client = EscoHelperClient()
        self.transform_config = transform_config


    def generate(self, concept_type: str, framework:str, concept_label: str, concept_description: str):
        embeddings = self.embedding_service.generate(
            label=concept_label,
            description=concept_description
        )

        terms = self.FRAMEWORKS_CONFIG[framework]["type_enums"][concept_type] 
        query = self.set_query(terms, embeddings)

        source_fields = self.FRAMEWORKS_CONFIG[framework]["source_fields"]

        try:
            response = self.es_client.search(
                index=self.ELASTICSEARCH_INDEX_SEARCH,
                query=query,
                _source=source_fields,
                size=self.LIMIT_SUGGESTIONS
            )
        except BadRequestError as e :
            try:
                if e.body['error']['failed_shards'][0]['reason']['caused_by']['reason'] == "A document doesn't have a value for a vector field!":
                    raise IndexError(f'Entities of types: "{','.join(terms)}" do not have vector field')
            except KeyError:
                pass
            raise e

        if len(response["hits"]["hits"]) == 0:
            raise NotImplementedError('Empty case to be coded')

        formated_response = self.format_response(concept_label, response["hits"]["hits"])
        return formated_response

    @staticmethod
    def set_query(terms, embeddings) -> Dict:
        query = {
            "bool": {
                "must": [
                    {"terms": {"type.enum": terms}},
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": embeddings}
                            }
                        }
                    }
                ]
            }
        }

        return query
    
    def format_response(self, concept_label, docs):
        suggestions = []
        for doc in docs:
            if not doc["_source"].get('id', None):
                print('WARN: there is no id in elastic search for this entity:', doc)
                continue

            # deserialisation
            entity = doc["_source"]
            if entity['pref_label__value']:
                if self.transform_config.framework == "esco":
                    translated_pref_label = self.esco_helper_client.translate_label(
                        uri=entity['id'].split("/")[1],
                        target_language=self.transform_config.language_target
                    )
                    entity['prefLabel'] = {'value': translated_pref_label}
                    entity['prefLabel']['language'] = self.transform_config.language_target
                else:
                    entity['prefLabel'] = {'value': entity['pref_label__value']}
                    entity['prefLabel']['language'] = entity['pref_label__language']
                del entity['pref_label__value']
                del entity['pref_label__language']

            id = f"match:suggestion/id_source/{md5(concept_label)}/id_target/{entity['id']}"
            suggestion = {
                "id": id,
                "type": "match:suggestion",
                "target": entity,
                "score": doc["_score"],
                "validated": 0,
                "framework": self.transform_config.framework,
                "mappingType": "skos:exactMatch",  # @TODO: make it dynamic ?
            }
            suggestions.append(suggestion)

        return suggestions