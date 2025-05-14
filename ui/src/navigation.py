from typing import Any, Dict
import streamlit as st
from streamlit.navigation.page import StreamlitPage
from components.login import login

#### HOME PAGE ####
dashboard_page = st.Page(
    page="components/dashboard.py",
    title="Welcome page",
    icon=":material/dashboard:",
    default=True
)

#### RULES CONFIGURATION PAGES ####
mapping_ontology_page = st.Page(
    page="components/mapping_ontology.py",
    title="Rules configuration",
    icon=":material/linked_services:",
    default=False
)
mapping_rules_page = st.Page(
    page="components/mapping_rules.py",
    title="Verify your rules",
    icon=":material/search:",
    default=False
)

#### TRANSLATOR PAGES ####
transform_page = st.Page(
    page="components/transform.py",
    title="AI Translator",
    icon=":material/network_intelligence_update:",
    default=False
)
matching_page = st.Page(
    page="components/matching_tool.py",
    title="Suggestions validation",
    icon=":material/rule:",
    default=False
)
enhancement_courses_page = st.Page(
    page="components/enhancement_courses.py",
    title="Enhancement Courses (WIP)",
    icon=":material/school:",
    default=False
)

#### LOGIN PAGE ####
login_page = st.Page(
    page=login,
    title="Login",
    icon=":material/admin_panel_settings:",
)

login_pages: Dict[str, Any] = {}
login_pages[""] = [login_page]

provider_pages: Dict[str, Any] = {}
provider_pages[""] = [
    dashboard_page,
    mapping_ontology_page,
    mapping_rules_page,
    transform_page,
    matching_page,
]


def navigation(pages: Dict[str, Any]) -> StreamlitPage:
    return st.navigation(pages=pages, position="sidebar", expanded=False)