from typing import List
from elasticsearch import NotFoundError
from slugify import slugify 
from ..elasticsearch.client import ElasticsearchClient
from ..config import get_api_settings
from ..utils.md5 import md5
from ..user.model import User

class TermService():
    
    def __init__(self, current_user: User) -> None:
        self.current_user = current_user
        settings = get_api_settings()
        self.es_client = ElasticsearchClient()
        self.index_name = settings.indice_mapping
        
    def get_by_id(self, item_id):
        """ Get a Concept by exact id, return None if not found """
        try:
            res = self.es_client.client.get(index=self.index_name, id=item_id)
        except NotFoundError:
            return None
        return res['_source']
    
    def create_collection(self, collection_id, collection_label):
        payload = {
            'id': collection_id, 
            'type':'skos:Collection', 
            'prefLabel': [{'value': collection_label}],
            'member': []
            }
        id = collection_id
        self.es_client.client.index(index=self.index_name, document=payload, id=id)
        return payload
    
    def update_collection(self, collection_id, updated_field):
        self.es_client.client.update(doc=updated_field, id=collection_id, index=self.index_name)

    def get_collection(self, collection_id):
        return self.get_by_id(collection_id)

    def delete_collection(self, collection_id):
        collection = self.get_by_id(collection_id)
        if collection is not None : 
            if collection.get('member', None) is not None:
                for member in collection['member']:
                    self.delete_concept(member)
            else:
                print('This collection has not .member property', collection['id'])
                
        self.es_client.client.delete(index=self.index_name, id=collection_id) 
        pass 
    
    def create_concept(self, concept_id, concept_pref_label, collection_id):
        concept = {"id": concept_id, 'type': 'skos:Concept', "prefLabel": [{"value": concept_pref_label}], "memberOf": collection_id}
        id = concept_id
        self.es_client.client.index(index=self.index_name, document=concept, id=id)
        collection = self.get_collection(collection_id)

        if collection is None:
            raise ValueError(f'The collection with id {collection_id} do not exist for the creation of concept with id {concept_id}')
        
        if collection.get('member', None) is None: 
            collection['member'] = [concept_id]
            self.update_collection(collection_id,{'member': collection['member']})
            return [concept, collection]
        
        if concept_id in collection['member']:
             return [concept, collection]
        else:
            collection['member'].append(concept_id)
            self.update_collection(collection_id,{'member': collection['member']})
            return [concept, collection]
    
    def delete_concept(self, concept_id):
        try:
            self.es_client.client.delete(index=self.index_name, id=concept_id)
        except NotFoundError:
            return None
        pass
    
    def get_concept(self, concept_id):
        """ Get a Concept by exact id, return None if not found """
        return self.get_by_id(concept_id)
    
    def create_or_find_term(
        self,
        concept_id: str,
        collection_id: str,
        concept_pref_label: str,
        collection_pref_label: str,
        path: str = ''
    ) -> List[dict]:    
        # uncomment to delete the collection and associated concept before running this function
        # self.delete_collection(collection_id)
    
        # Find or create the concept
        concept = self.get_concept(concept_id)
        
        if not concept:
            collection = self.get_collection(collection_id)
            if not collection:
                collection_label = f"{self.current_user.username} collection for {collection_pref_label} in {path}"
                collection = self.create_collection(collection_id, collection_label)
            concept, collection = self.create_concept(concept_id, concept_pref_label, collection_id)
        else: 
            collection = self.get_collection(collection_id)
        return [concept, collection]

    def generate(self, documents: dict, by_tree: bool = True) -> dict:
        instances = {}

        for instance in documents["graph"]:
            if "__family__" in instance: 
                concept_pref_label = instance["__family__"]["str_value"]  # 0.8
                collection_pref_label = instance["__family__"]["scale"]  # skill
                familyId = f'term:{slugify(self.current_user.username)}/{str.lower(collection_pref_label)}/{md5(instance["__family__"]["scale_path"])}/{slugify(concept_pref_label)}'
                familyCollection = f'term:{slugify(self.current_user.username)}/{str.lower(collection_pref_label)}/{md5(instance["__family__"]["scale_path"])}'
                if not familyId in instances:
                    term,collection = self.create_or_find_term(
                        familyId,
                        familyCollection,
                        concept_pref_label,
                        'family',
                        instance["__family__"]["scale_path"],
                    )
                    instances[familyId] = term
                    term_in_document = term
                    
                    # keep the notation as "direct injection" to be able to keep the source type (string, int or float) "as is",
                    # because Elastic required to fix the type (string mostly)
                    term_in_document["notation"] = instance["__family__"]["value"]
                    documents["graph"].append(term_in_document)
                    
                    instances[familyCollection] = collection # collection_in_document
                    # override the collection item in the graph
                    self.add_or_update_in_graph(documents, collection)
                    
                instance["family"] = familyId
                del instance["__family__"] # delete the marker from the instance
            
            if "__term__" in instance:
                concept_pref_label = instance["__term__"]["str_value"]  # 0.8
                collection_pref_label = instance["__term__"]["scale"]  # skill
                collection_category = 'skill'
                
                if instance["__term__"]["targetFunction"] == 'fno:get-polarity-value':
                    collection_category = 'polarity'
                    
                if instance["__term__"]["targetFunction"] == 'no:find-or-create-term':
                    collection_category = 'term'

                skill_level_identifier = f'term:{slugify(self.current_user.username)}/{str.lower(collection_pref_label)}/{md5(instance["__term__"]["scale_path"])}'
                skill_level_value = f'{skill_level_identifier}/value/{concept_pref_label}'
                skill_level_scale = f'{skill_level_identifier}/scale'
                
                concept_id = skill_level_value
                collection_id = skill_level_scale

                if not concept_id in instances:
                    term, collection = self.create_or_find_term(
                        concept_id,
                        collection_id,
                        concept_pref_label,
                        collection_category,
                        instance["__term__"]["scale_path"],
                    )
                    instances[concept_id] = term
                    instances[collection_id] = collection
                    
                    term_in_document = term
                    # keep the notation as "direct injection" to be able to keep the source type (string, int or float) "as is",
                    # because Elastic required to fix the type (string mostly)
                    term_in_document["notation"] = instance["__term__"]["value"]
                    
                    documents["graph"].append(term_in_document)
                    self.add_or_update_in_graph(documents,collection)
                    # documents["graph"].append(collection)
                if instance["__term__"]["targetFunction"] == 'fno:get-polarity-value': 
                    instance["polarityValue"] = skill_level_value
                    instance["polarityScale"] = skill_level_scale
                else:
                    instance["skillLevelValue"] = skill_level_value
                    instance["skillLevelScale"] = skill_level_scale
                    
                del instance["__term__"] # delete the marker in the instance

        return documents

    def add_or_update_in_graph(self, documents, item):
        graph = documents['graph']
        for i in range(len(graph)):
            if graph[i].get('id', None) == item['id'] : 
                graph[i] = item
                return 
            
        graph.append(item)
        pass