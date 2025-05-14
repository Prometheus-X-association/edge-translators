import streamlit as st
from typing import Any, Dict, List
import requests
from requests import Response, models



class OntobridgeClient:

    def __init__(self):
        pass

    def call(
        self,
        path: str = "",
        method: str = 'GET',
        query_params: Dict[str, str] | None = None,
        json: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None
    ) -> Response :
        url = f"{st.session_state.translator_api_url}{path}"

        return requests.request(
            method=method.upper(),
            url=url,
            params=query_params,
            json=json,
            data=data,
            headers=headers
        )

    def login(self, username: str, password: str) -> Response:
        headers = {}
        headers["accept"] = "application/json"
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {}
        data["grant_type"] = "password"
        data["username"] = username
        data["password"] = password

        return self.call(
            path=f"/auth/token",
            method='POST',
            data=data,
            headers=headers
        )

    def get_me(self) -> Response:
        headers = {}
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        headers["Content-Type"] = "application/json"
        headers["accept"] = "application/json"

        return self.call(
            path=f"/users/me",
            method='GET',
            headers=headers
        )

    def get_mapping_rules(self) -> Response:
        headers = {}
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        headers["Content-Type"] = "application/json"
        headers["accept"] = "application/json"

        return self.call(
            path=f"/rules",
            method='GET',
            headers=headers
        )
    
    def post_mapping_rules(self, mapping_rules: Dict) -> Response:

        headers = {}
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        headers["Content-Type"] = "application/json"
        headers["accept"] = "application/json"

        json = {}
        json["rules"] = mapping_rules
        return self.call(
            path=f"/rules",
            method='POST',
            json=json,
            headers=headers
        )

    def get_matchings(
        self,
        validated: bool | None = None,
        concept_type: str | None = "jobs",
        framework: str | None = "esco",
    ) -> Response:

        headers = {}
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        headers["Content-Type"] = "application/json"
        headers["accept"] = "application/json"

        query_params = {}
        query_params["validated"] = validated
        query_params["concept_type"] = concept_type
        query_params["framework"] = framework
        
        return self.call(
            path=f"/matching",
            method='GET',
            query_params=query_params,
            headers=headers
        )

    def post_transform(
        self,
        target_framework: str,
        lang_source: str,
        lang_target: str,
        data: Dict
    ) -> requests.Response:

        headers = {}
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        headers["Content-Type"] = "application/json"
        headers["accept"] = "application/json"

        query_params = {}
        query_params["target_framework"] = target_framework
        query_params["language_source"] = lang_source
        query_params["language_target"] = lang_target
        
        json = {}
        json["document"] = data

        return self.call(
            path="/transform",
            method='POST',
            query_params=query_params,
            json=json,
            headers=headers
        )