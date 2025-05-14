import json
import os
from elasticsearch import Elasticsearch
import streamlit as st
import extra_streamlit_components as stx


def init_state():
    st.session_state.initialized = True

    st.session_state.app_env = os.getenv('APP_ENV', "dev")

    st.session_state.access_token = None
    st.session_state.is_authenticated = False

    st.session_state.user = None
    st.session_state.say_hello = True
    st.session_state.already_redirected_after_upload = False

    st.session_state.has_file_uploaded = False
    st.session_state.has_existing_mapping_rules = False
    st.session_state.ruleFile = None

    st.session_state.data = None
    st.session_state.raw_data = None

    st.session_state.Experience = [
        ("type", ["educational", "professional", "vocational", "personnality Test"]),
        ("status", ["past", "ongoing", "suggested"])
    ]
    st.session_state.Skill = []
    st.session_state.Polarity = []
    st.session_state.Profile = []

    st.session_state.pivotal_ontology_properties_to_map = {
        "Profile": ["name", "email", "address"],
        "Experience": ["prefLabel", "description", "dateFrom", "dateTo", "company", "location", "contractType", "family", "sourceId", "polarity"],
        "Skill": ["prefLabel", "description", "skillLevelValue", "family", "polarity"]
    }
    
    st.session_state.itemList = []
    st.session_state.mappingList = []
    st.session_state.mapped = []
    st.session_state.submitted = False
    
    st.session_state.translator_api_url = os.getenv('TRANSLATOR_API_URL', "http://ontobridge-api:8000")
    
    es_api_keys = (os.getenv('ES_API_KEY_1', "apikeyId"), os.getenv('ES_API_KEY_2', "apikeySecret"))
    es_connection_string = os.getenv("ES_CONNECTION_STRING", "http://elasticsearch:9200")
    if st.session_state.app_env == "prod":
        st.session_state.ES = Elasticsearch(
            cloud_id = es_connection_string,
            api_key=es_api_keys
        )
    else:
        st.session_state.ES = Elasticsearch(
            hosts = es_connection_string,
            api_key = es_api_keys
        )

    st.session_state.rome_names = json.load(open("data/ROME/ROME_names.json", "rb"))
    
