from elasticsearch import Elasticsearch
import os
from ..config import settings, Environment

class ElasticsearchClient:
    def __init__(self):
        self.es_connection_string = os.getenv("ES_CONNECTION_STRING", "http://elasticsearch:9200")
        self.credentials = (os.getenv('ES_API_KEY_1', "apikeyId"), os.getenv('ES_API_KEY_2', "apikeySecret"))
        
        if settings.environment is Environment.prod:
            self.client = Elasticsearch(
                cloud_id = self.es_connection_string,
                api_key=self.credentials,
            )
        else:
            self.client = Elasticsearch(
                hosts = self.es_connection_string,
                api_key = self.credentials,
            )
    
    def index(self):
        pass
    
    def search(self):
        pass