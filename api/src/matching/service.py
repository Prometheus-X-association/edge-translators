from typing import Dict, List
from elasticsearch import NotFoundError

from ..esco_helper.client import EscoHelperClient
from ..elasticsearch.client import ElasticsearchClient
from ..transform.model import TransformConfig
from .suggestion_service import SuggestionService
from ..utils.md5 import md5
from ..user.model import User
from ..matching.model import Matching, PrefLabel, Suggestion

class MatchingService:

    ELASTICSEARCH_INDEX_MATCHING = "edge_matchings"

    STATUS_NOT_VALIDATED = 0
    STATUS_VALIDATED = 1

    def __init__(self, current_user: User):
        self.current_user = current_user
        self.es_client = ElasticsearchClient().client
        self.esco_helper_client = EscoHelperClient()
        self.transform_config = TransformConfig()
        # self.suggestion_service = SuggestionService(self.transform_config)

    def find(self, id) -> dict|None:
        try:
            res = self.es_client.get(index=self.ELASTICSEARCH_INDEX_MATCHING, id=id)
            if res == None:
                return None
        except NotFoundError:
            return None

        return res['_source']

    def update(self, id, new_doc, refresh=None):
        try:
            self.es_client.update(index=self.ELASTICSEARCH_INDEX_MATCHING, id=id, doc=new_doc, refresh=refresh)
        except Exception as e:
            raise Exception(f"Error: {e}")

    def find_all(self):
        query = {
            "term": {
                "provider": self.current_user.username
            }
        }

        res = self.es_client.search(index=self.ELASTICSEARCH_INDEX_MATCHING, query=query)
        nb_result = res['hits']['total']['value']
        if nb_result == 0:
            return []

        values = res['hits']['hits']

        response = []
        for v in values:
            matchings = v['_source']
            matchings["_id"] = v["_id"]
            response.append(matchings)

        return response

    def find_some(
        self,
        validated: bool | None = None,
        concept_type: str | None = None,
        framework: str | None = None
    ):
        query = {}
        query["bool"] = {}
        query["bool"]["must"] = []
        query["bool"]["must"].append({"term": {"provider": self.current_user.username}})

        if validated is not None:
            query["bool"]["must"].append({"term": {"match.validated": int(validated)}})
        if concept_type is not None:
            query["bool"]["must"].append({"term": {"type.keyword": concept_type}})
        if framework is not None:
            query["bool"]["must"].append({"term": {"framework.keyword": framework}})

        res = self.es_client.search(index=self.ELASTICSEARCH_INDEX_MATCHING, query=query, size=1000, request_cache=False)

        nb_result = res['hits']['total']['value']
        if nb_result == 0:
            return []

        values = res['hits']['hits']

        response = []
        for v in values:
            matchings = v['_source']
            matchings["_id"] = v["_id"]
            response.append(matchings)

        return response

    def create(self, id, payload, refresh=None):
        self.es_client.index(index=self.ELASTICSEARCH_INDEX_MATCHING, document=payload, id=id, refresh=refresh)

    def delete(self, id, refresh=None): 
        try :
            self.es_client.delete(index=self.ELASTICSEARCH_INDEX_MATCHING, id=id, refresh=refresh)
        except Exception as e:
            raise Exception(f"ERROR: {e}")
    
    def delete_all(self, refresh=None):
        query = {
            "bool": {
                "must": [
                    {"term": {
                        "provider": self.current_user.username
                    }},
                ]
            }
        }
        try :
            self.es_client.delete_by_query(index=self.ELASTICSEARCH_INDEX_MATCHING, query=query, refresh=refresh)
        except Exception as e:
            raise Exception(f"Error: {e}")

    def exists(self, id) -> bool:
        exist = self.find(id)
        return exist is not None

    def set_es_id(self, concept_pref_label):
        prefix = "match:"
        provider = f"provider/{self.current_user.username}/"
        framework = f"framework/{self.transform_config.framework}/"
        pref_label = f"label/{md5(concept_pref_label)}/"
        language_source = f"slang/{self.transform_config.language_source}/"
        language_target = f"tlang/{self.transform_config.language_target}"

        matching_id = prefix + provider + framework + pref_label + language_source + language_target
        return matching_id

    def set_object(self, concept_type: str, concept_pref_label: str, concept_pref_description: str, id: str, suggestions: List):
        match = list(filter(lambda x : x['validated'] == 1, suggestions))
        if len(match) == 1 : 
            match = match[0]
            suggestions = list(filter(lambda x : x['validated'] != 1, suggestions))
        else : 
            match = suggestions.pop(0)

        match_object = Suggestion(**match)
        suggestion_objects = [Suggestion(**suggestion) for suggestion in suggestions]
        pref_label_object = PrefLabel(
            value = concept_pref_label,
            language = self.transform_config.language_source,
        )
        matching_object = Matching(
            id = id,
            prefLabel = pref_label_object,
            description = concept_pref_description,
            type = concept_type,
            framework = self.transform_config.framework,
            provider = self.current_user.username,
            match = match_object,
            suggestions = suggestion_objects
            # match = None,
            # suggestions = []
        )

        
        return matching_object.dict()
    
    def generate(self, documents: Dict, transform_config: TransformConfig, refresh=None) -> Dict:
        self.transform_config = transform_config
        instances = {}
        for doc in documents["graph"]:
            if "__matching__" in doc:
                matching_marker = doc["__matching__"]
                concept_pref_label = matching_marker["sourceValue"]
                concept_pref_description = matching_marker["parameter"] if "parameter" in matching_marker else ""
                concept_pref_description = doc["description"] if "description" in doc else ""
                concept_type = matching_marker["subtype"]

                matching_id = self.set_es_id(concept_pref_label)
                matching_already_exists = self.exists(id=matching_id)
                matching = None
                if matching_already_exists:
                    matching = self.find(matching_id)
                
                concept_id = f"term:{self.current_user.username}/{concept_type}/{transform_config.framework}/value/{md5(concept_pref_label)}"

                if (matching is None) and (not concept_id in instances):
                    suggestion_service = SuggestionService(transform_config)
                    suggestions = suggestion_service.generate(
                        concept_type=concept_type,
                        framework=transform_config.framework,
                        concept_label=concept_pref_label,
                        concept_description=concept_pref_description
                    )

                    matching = self.set_object(doc["type"], concept_pref_label, concept_pref_description, doc["id"], suggestions)
                    self.create(matching_id, matching, refresh)
                    instances[concept_id] = matching
                doc.update(matching)
                del doc["__matching__"]
        
        return documents