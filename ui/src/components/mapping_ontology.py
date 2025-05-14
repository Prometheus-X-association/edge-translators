import streamlit as st
import json
from client.ontobridge import OntobridgeClient
from objects import ObjectTypeEnum
from schemas.rule import Rule
from services.rule_service import create_rule_v2

####################### OBJECT CREATION & DISPLAY #################################

def createTab():
    l_col, r_col = st.columns([1,1])
    with l_col:
        create_item_form()
    with r_col:
        display_existing_items()

def create_item_form():
    container = st.container(border=True)
    with container:
        st.markdown("**Create and Manage Your Data with Pivotal Ontology objects**")

        # col_l = st.columns(1)
        st.selectbox(f"Select your object", [obj.value for obj in ObjectTypeEnum], index=None, placeholder="Object type", key="selectedType")

        with st.form(f"Item type", border=False, clear_on_submit=True):
            object_name = st.text_input(
                f"Name your Object",
                placeholder=f"Object Name",
                key="objectName",
            )

            item = {
                "class": st.session_state.selectedType,
                "name": st.session_state.objectName,
            }

            # Handle Experience object creation
            if item["class"] == "Experience":
                for property, values in st.session_state[st.session_state.selectedType]:
                    item[property] = st.selectbox(
                        f"Select an Experience {property}",
                        values,
                        placeholder=f"Experience {property}",
                        format_func=str.capitalize,
                        key=f"{property}_value"
                    )

            # Handle Skill object creation
            elif item["class"] == "Skill":
                item["targetExperience"] = st.selectbox(
                    f"Associated Experience",
                    [created_items["name"] for created_items in st.session_state.itemList if created_items["class"] == "Experience"],
                    index=None,
                    placeholder="Choose an option",
                    format_func=str.capitalize,
                    key=f"targetExp_value"
                )

            if st.form_submit_button(f"Create", use_container_width=True):
                st.session_state.submitted = False
                if object_name == "":
                    st.warning("Object name empty")
                    return 
                else:
                    st.session_state.itemList.append(item)
                st.rerun()


def display_existing_items():
    def delete_row(index):
        st.session_state.itemList = [obj for i, obj in enumerate(st.session_state.itemList) if i != index]

    container = st.container(border=True)
    col1_header, col2_header, col3_header, col4_header = container.columns([1, 1, 1.5, 0.5], gap="small")
    col1_header.markdown("**Object**")
    col2_header.markdown("**Name**")
    col3_header.markdown("**Properties**")

    for index, value in enumerate(st.session_state.itemList):
        line = container.container()
        line.markdown("---")
        col1_value, col2_value, col3_value, col4_value = line.columns([1, 1, 1.5, 0.5])
        col1_value.write(f"{value["class"]}")
        col2_value.write(f"{value["name"]}")
        if value["class"] == "Profile":
            col3_value.write(None)
        if value["class"] == "Experience":
            col3_value.write(f"Type: `{value["type"]}`")
            col3_value.write(f"Status: `{value["status"]}`")
        if value["class"] == "Skill":
            col3_value.write(f"Experience: `{value["targetExperience"]}`")
        if col4_value.button(":material/delete:", key=f"del_{index}", type="tertiary"):
            delete_row(index)
            st.rerun()
   
########################## RULES CREATION & DISPLAY #####################################

def matchingTab():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Map your fields to Pivotal Ontology classes and properties**",)
        create_mapping_form()
    with col2:
        st.markdown("**Your Rules**")
        display_existing_rules()

    if len(st.session_state.mappingList) > 1:
        if "result_jsonld" not in st.session_state:
            st.session_state.result_jsonld = None

def auto_assign_generateID():
    obj_names = {}

    for field in st.session_state.fieldList:
        object_info = st.session_state.get(f"object_{field}", {})
        if object_info:
            obj_name = object_info['name']
            if obj_name not in obj_names:
                obj_names[obj_name] = field  # Keep track of the first occurrence

    for obj_name, field in obj_names.items():
        generateID = st.session_state.get(f"generateID_{field}", False)
        if not generateID:  # Assign if no 'generateID' was checked
            st.session_state[f"generateID_{field}"] = True
        else:
            st.session_state[f"generateID_{field}"] = False
            
def create_mapping_form():
    if st.session_state.get('create_rules_next', False):
        auto_assign_generateID()

        st.session_state.mappingList = []
        st.session_state.mapped = []
        for field in st.session_state.fieldList:
            if st.session_state.get(f"object_{field}", {}) and st.session_state.get(f"property4{field}", {}):
                create_rule_v2(field)
                mapped = {
                    "class": st.session_state[f"object_{field}"]["class"],
                    "sourcePath": field,
                    "targetObject": st.session_state[f"object_{field}"]["name"],
                    "targetProperty": st.session_state[f"property4{field}"]
                }

                if st.session_state[f"property4{field}"] == "dateFrom" or st.session_state[f"property4{field}"] == "dateTo":
                    mapped["dateFormat"] = st.session_state[f"dateformat4{field}"]
                st.session_state.mapped.append(mapped)
        
        mapping_rules = {}
        mapping_rules["@context"] = {}
        mapping_rules["@context"]["todo"] = "https://mindmatcher.org/ontology-1.0.0.jsonld"
        mapping_rules["graph"] = st.session_state.mappingList

        post_mapping_rules(mapping_rules)
        
        st.session_state['create_rules_next'] = False

    for field in st.session_state.fieldList:
        form_mapping_properties(field)

    if 'confirm_overwrite' not in st.session_state:
        st.session_state['confirm_overwrite'] = False

    if st.button("Save Rules", use_container_width=True, key="create_rules_button"):
        st.session_state['confirm_overwrite'] = True
        st.rerun()

    if st.session_state['confirm_overwrite']:
        st.warning("This will overwrite existing rules. Do you want to proceed?")
        _, col1, _, col2, _ = st.columns(5)
        proceed = col1.button("Yes, proceed", key="confirm_overwrite_yes", use_container_width=True)
        cancel = col2.button("Cancel", key="confirm_overwrite_no", use_container_width=True)

        if proceed:
            auto_assign_generateID()
            st.session_state['create_rules_next'] = True
            st.session_state['confirm_overwrite'] = False
            st.rerun()

        elif cancel:
            st.session_state['confirm_overwrite'] = False
            st.rerun()

def form_mapping_properties(field: str):
    if f"property4{field}" in st.session_state:
        is_date_field =(st.session_state[f"property4{field}"] == "dateFrom" or st.session_state[f"property4{field}"] == "dateTo")
    else:
        is_date_field = next((m for m in st.session_state.mapped if m["sourcePath"] == field and "dateFormat" in m), None) != None

    mapped = next((m for m in st.session_state.mapped if m["sourcePath"] == field), None)
    label = f""":green[:material/check_circle: {field} :material/arrow_right_alt: {mapped["targetObject"]}.{mapped["targetProperty"]} _({mapped["class"]})_]
    """ if mapped else f":orange[:material/unpublished: {field}]"

    col_l, col_r = st.columns([9, 1])
    with col_l.expander(label, expanded=False):
        mapped_object_key = next((key for key, item in enumerate(st.session_state.itemList) if mapped and item["name"] == mapped["targetObject"]), None)
        object_selection = st.selectbox(
            f"Select Pivotal Ontology object",
            st.session_state.itemList,
            format_func=lambda x: x["name"],
            key=f"object_{field}",
            index=mapped_object_key
        )

        properties = []
        if object_selection:
            properties = st.session_state.pivotal_ontology_properties_to_map[object_selection["class"]]

        mapped_property_key = next((key for key, item in enumerate(properties) if mapped and item == mapped["targetProperty"]), None)
        st.selectbox(f"Select Pivotal Ontology property", properties, key=f"property4{field}", index=mapped_property_key)
        
        if is_date_field:
            date_format_supported = ["big-endian-no-separator", "year-only"]
            mapped_dateformat_key = next((key for key, item in enumerate(date_format_supported) if mapped and mapped["dateFormat"] and item == mapped["dateFormat"]), None)
            st.selectbox(f"Select Format",
                date_format_supported,
                key=f"dateformat4{field}",
                placeholder=f"Select a format",
                index=mapped_dateformat_key,
                help=f"""
                List of supported date formats:  
                - **big-endian-no-separator**: `YYYY-MM-DD` _(default)_  
                - **year-only**: `YYYY`
                """
            )

    if mapped:
        if col_r.button(label="", icon=":material/delete:", key=f"btn_del_mapping_{field}", type="secondary"):
            mapped_key = next((key for key, value in enumerate(st.session_state.mapped) if value["sourcePath"] == field), None)
            if mapped_key != None:
                del st.session_state.mapped[mapped_key]
                st.rerun()


def display_existing_rules():
    st.session_state.ruleFile = {
        "@context": "https://mindmatcher.org/ontology-1.0.0.jsonld",
        "graph": st.session_state.mappingList
    }

    st.code(json.dumps(st.session_state.ruleFile, indent=4), language="json")

def post_mapping_rules(mapping_rules) -> None:
    ontobridge_client = OntobridgeClient()
    ontobridge_client.post_mapping_rules(mapping_rules=mapping_rules)

########################## APP LOGIC #####################################

def main():
    st.markdown(body="### Rules configuration :material/linked_services:")
    st.caption("_Create your transformation rules by mapping objects and fields from your data to the pivotal Ontology_")

    has_file_uploaded = st.session_state.has_file_uploaded
    has_existing_mapping_rules = st.session_state.has_existing_mapping_rules
    if has_file_uploaded or has_existing_mapping_rules:
        tabs = st.tabs(["List your objects","Map your fields"])
        with tabs[0]:
            createTab()
        with tabs[1]:
            matchingTab()
    else:
        error_type = "MISSING_INPUT_DATA"
        error_message = "In order to create some transformation rules, please import some sample data and create your rules."
        st.warning(f"**{error_type}**: _{error_message}_", icon=":material/unknown_document:")
        error_type = "MISSING_RULES"
        error_message = "You dont have any rule defined yet. Please create some transformation rules to be able to process data with the AI Translator."
        st.warning(f"**{error_type}**: _{error_message}_", icon=":material/unknown_document:")

main()