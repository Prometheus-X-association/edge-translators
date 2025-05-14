
import json
import streamlit as st
from model.user import User
from client.ontobridge import OntobridgeClient
from streamlit.runtime.uploaded_file_manager import UploadedFile
from i18n import FRAMEWORK_OUTPUT_LANGUAGE

def main():
    st.markdown("### AI Translator :material/network_intelligence_update:")
    st.caption("_Use the AI Translator to transform your data into meaningful quality data_")

    ontobridge_client = OntobridgeClient()

    response = ontobridge_client.get_mapping_rules()

    if response.status_code != 200:
        error_type = "MISSING_RULES"
        error_message = "You dont have any rule defined yet. Please create some transformation rules to be able to process data with the AI Translator."
        st.warning(f"**{error_type}**: _{error_message}_", icon=":material/unknown_document:")
        return

    if "raw_data" not in st.session_state:
        st.session_state.raw_data = None
    
    if not isinstance(st.session_state.raw_data, UploadedFile):
        error_type = "MISSING_INPUT_DATA"
        error_message = "Please upload some data to be able to use the AI Translator."
        st.warning(f"**{error_type}**: _{error_message}_", icon=":material/unknown_document:")
        return

    col1, col2 = st.columns([1, 3], border=True)
    
    with col1:

        if ("raw_data" in st.session_state and isinstance(st.session_state.raw_data, UploadedFile)):

            selected_framework = st.selectbox("Select the target framework", ["esco", "rome"], key="target_framework_selectbox")
            if selected_framework:
                st.selectbox("Select the source language", FRAMEWORK_OUTPUT_LANGUAGE[selected_framework], key="source_language_selectbox")
                st.selectbox("Select the target language", FRAMEWORK_OUTPUT_LANGUAGE[selected_framework], key="target_language_selectbox")
            st.button(
                label = f"Use the AI Translator",
                key = "transform_button",
                help = None,
                on_click = None,
                args = None,
                kwargs = None,
                type = "primary",
                icon = ":material/network_intelligence_update:",
                disabled = False,
                use_container_width = False
            )

    with col2:
        if "transform_button" in st.session_state and st.session_state["transform_button"]:

            with st.spinner("⏳ Processing data... Please wait.", show_time=True):
                
                response = ontobridge_client.post_transform(
                    st.session_state["target_framework_selectbox"],
                    st.session_state["source_language_selectbox"],
                    st.session_state["target_language_selectbox"],
                    json.load(st.session_state["raw_data"])
                )
                if response.status_code == 200:
                    col1.success(f"""
                        :material/check_circle: Your data has been successfully processed:
                        - **Ontologically**: JSON-LD / RDF structure, thanks to the pivot ontology
                        - **Terminologically**: the values ​​matched with **{st.session_state["target_framework_selectbox"].upper()}** in **{st.session_state["target_language_selectbox"].upper()}**
                    """)
                    st.code(json.dumps(response.json(), indent=4), language="json")
                else:
                    st.error(f"Error: {response.reason}")
main()