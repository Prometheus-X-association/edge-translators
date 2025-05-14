import json
import streamlit as st

def parseField(item, field, stringPath=""):
    value = item[field]
    if isinstance(value, list) and len(value) > 0:
        if isinstance(value[0], dict):
            fieldList = value[0].keys()
            for nestedField in fieldList:
                newStringPath = f"{stringPath}.{field}" if stringPath else field
                parseField(value[0], nestedField, newStringPath)
        else:
            newStringPath = f"{stringPath}.{field}" if stringPath else field
            st.session_state.fieldList.append(newStringPath)
    elif isinstance(value, dict):
        fieldList = value.keys()
        for nestedField in fieldList:
            newStringPath = f"{stringPath}.{field}" if stringPath else field
            parseField(value, nestedField, newStringPath)
    else:
        newStringPath = f"{stringPath}.{field}" if stringPath else field
        st.session_state.fieldList.append(newStringPath)

def parseFile():
    try:
        st.session_state.data = json.load(st.session_state.raw_data)
    except:
        st.error("File error")
        st.session_state.already_redirected_after_upload = False
        del st.session_state.raw_data
        st.session_state.has_file_uploaded = False
        st.stop()
    st.session_state.fieldList = []
    first_item = st.session_state.data[0] if isinstance(st.session_state.data, list) else st.session_state.data
    fieldList = [key for key in first_item.keys()]
    for field in fieldList:
        with st.container():
            parseField(first_item,field)
    return fieldList

def load_custom_css():
    css = '''
    <style>
        [data-testid='stFileUploader'] {
            width: max-content;
        }
        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }
        [data-testid='stFileUploader'] section > input + div {
            display: none;
        }
        [data-testid='stFileUploader'] section + div {
            display: none;
        }

    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

def import_file():
    load_custom_css()
    if "raw_data" not in st.session_state:
        st.session_state.raw_data = None

    file = st.file_uploader(
        label="",
        type="json",
        accept_multiple_files = False,
        key="file",
        help = None,
        on_change = None,
        args = None,
        kwargs = None,
        disabled = False,
        label_visibility = "hidden"
    )

    if file is not None:
        if "fieldList" in st.session_state:
            del st.session_state.fieldList
        st.session_state.raw_data = file
        st.session_state.has_file_uploaded = True
        parseFile()

        if st.session_state.already_redirected_after_upload == False:
            st.session_state.already_redirected_after_upload = True
            st.switch_page(page="components/mapping_ontology.py")
