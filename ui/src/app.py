import json
import streamlit as st    
from typing import Any, Dict
from dotenv import load_dotenv
import torch
# from components.login import handle_logout, set_access_token_cookie, get_access_token_cookie
from state import init_state
from client.ontobridge import OntobridgeClient
from navigation import navigation, login_pages, provider_pages
from model.user import User, RoleEnum
# from components.mapping_ontology import displaySidebar
from streamlit.runtime.uploaded_file_manager import UploadedFile
from model.tree_node import TreeNode
from components.import_file import import_file

torch.classes.__path__ = []

load_dotenv()

if 'initialized' not in st.session_state:
    st.set_page_config(layout="wide")
    init_state()


def get_existing_rules() -> None:
    if st.session_state.has_file_uploaded == False: 
        ontobridge_client = OntobridgeClient()

        mapping_rules = ontobridge_client.get_mapping_rules()
        if mapping_rules.status_code == 200 and "graph" in mapping_rules.json():
            rules = mapping_rules.json()["graph"]
            st.session_state.has_existing_mapping_rules = True
            st.session_state.mappingList = rules
            st.session_state.fieldList = list(set([rule["sourcePath"] for rule in rules]))
            st.session_state.raw_data = list(set([rule["sourcePath"] for rule in rules]))
            st.session_state.ruleFile = {
                "@context": "https://mindmatcher.org/ontology-1.0.0.jsonld",
                "graph": st.session_state.mappingList
            }
    else:
        ontobridge_client = OntobridgeClient()

        mapping_rules = ontobridge_client.get_mapping_rules()
        if mapping_rules.status_code == 200 and "graph" in mapping_rules.json():
            rules = mapping_rules.json()["graph"]
            st.session_state.has_existing_mapping_rules = True
            st.session_state.mappingList = rules
            st.session_state.ruleFile = {
                "@context": "https://mindmatcher.org/ontology-1.0.0.jsonld",
                "graph": st.session_state.mappingList
            }

def say_hello() -> None:
    if st.session_state.say_hello == True:
        st.toast(f"Welcome **{st.session_state.user.username}**", icon=":material/how_to_reg:")
        st.session_state.say_hello = False

# def guard_non_activate_users() -> None:
#     user: User = st.session_state.user
#     if not user.active:
#         handle_logout()

def build_tree(field_list):
    root = TreeNode(name=None)
    for field in field_list:
        parts = field.split('.')
        current_node = root
        for i, part in enumerate(parts):
            if part not in current_node.children:
                current_node.children[part] = TreeNode(name=part)
            current_node = current_node.children[part]
            # If it's the last part, mark as leaf
            if i == len(parts) - 1:
                current_node.is_leaf = True
    return root

def build_display_lines(node, prefix=''):
    lines = []
    children = list(node.children.values())
    for i, child in enumerate(children):
        is_last = (i == len(children) -1)
        connector = '└─ ' if is_last else '├─ '
        line = prefix + connector + child.name
        lines.append(line)
        extension = '    ' if is_last else '│   '
        # If the child has children, recurse
        if child.children:
            lines.extend(build_display_lines(child, prefix + extension))
    return lines

def displaySidebar():
    field_list = st.session_state.fieldList
    tree_root = build_tree(field_list)
    display_lines = build_display_lines(tree_root)
    tree_text = '\n'.join(display_lines)
    return tree_text

if st.session_state.is_authenticated:
    # Block connection if user status is inative
    # guard_non_activate_users()
    # Say hello post login
    say_hello()
    
    st.sidebar.write(f"Connected as **{st.session_state.user.username}** :material/account_circle:")

    pages: Dict[str, Any] = {}
    if RoleEnum.ROLE_PROVIDER in st.session_state.user.role:
        get_existing_rules()
        pages=provider_pages
        container = st.sidebar.container(border=False)
        with container:
            import_file()
            if ("raw_data" in st.session_state and isinstance(st.session_state.raw_data, UploadedFile)) and "fieldList" in st.session_state:
                st.download_button(
                    label=st.session_state.raw_data.name,
                    data=st.session_state.raw_data,
                    file_name=st.session_state.raw_data.name,
                    mime="application/json",
                    key="download_uploaded_file_btn",
                    type="tertiary",
                    icon=":material/file_download:"
                )
                st.code(displaySidebar(), language="")

    # if RoleEnum.ROLE_ADMIN in st.session_state.user.role:
    #     pages=admin_pages
    
    nav = navigation(pages)

    # has_logout = st.sidebar.button(label=":material/exit_to_app: Logout", key="logout_btn")

    # if has_logout:
    #     handle_logout()
else:
    pages=login_pages
    nav = navigation(pages)

nav.run()