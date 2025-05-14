
from pathlib import Path
import streamlit as st

def done(message):
    st.markdown(f"**:green[:material/task_alt: {message}]**")

def todo(message):
    st.markdown(f"**:orange[:material/error: {message}]**")

def widget_checklist():
    check_user = st.session_state.user is not None
    check_has_existing_mapping_rules = st.session_state.has_existing_mapping_rules is True
    check_has_file_uploaded = st.session_state.has_file_uploaded is True
    check_status_api =  True
    check_has_model =  True
    checklist_expander = st.expander(
        f"**CHECK LIST {check_user + check_has_existing_mapping_rules + check_has_file_uploaded + check_status_api + check_has_model}/{5}**",
        expanded=True
    )

    with checklist_expander: 
        if check_user:
            done("User is active")
        else:
            todo("User is active")

        if check_has_existing_mapping_rules:
            done(f"{len(st.session_state.mappingList)} rules detected")
        else:
            todo("no rules detected")
        
        if check_has_file_uploaded:
            done("Data available")
        else:
            todo("Data available")

        if check_status_api:
            done("Healtcheck API")
        else:
            todo("Healtcheck API")

        if check_has_model:
            done("Model ready to use")
        else:
            todo("Model ready to use")

def widget_documentation():
    # st.image("src/components/images/image1.png")
    documentation_expander = st.expander("**DOCUMENTATION**", expanded=True)
    with documentation_expander:
        data = Path(f"{Path(__file__).parent}/design-document.md").read_text()
        st.markdown(data, unsafe_allow_html=True)

def under_construction():
    # container = st.container(border=True)
    image = Path(f"{Path(__file__).parent}/images/under_construction.jpg")
    colleft, colcenter, colright = st.columns([2.2,5,2])
    colcenter.image(image, width=500)
    # colcenter.subheader(":orange[Page under construction, coming soon]")
    colcenter.markdown("<h3 style='margin-left: 5%; color: #ed6f13;'>Page under construction, coming soon</h3>", unsafe_allow_html=True)

def main():
    st.write("#")
    st.write("#")
    colleft, colcenter, colright = st.columns([2,2,2])
    colcenter.markdown("# 👋 Welcome!")
    colleft, colcenter, colright = st.columns([1.9,2,2])

    colcenter.markdown("Upload your data to enable Edge AI Translator")

    # st.markdown("### Welcome page :material/dashboard:")
    # under_construction()
    # st.caption("""
    #     Welcome on the AI Translator UI :material/waving_hand: On this interface, you will enhance interoperability of your data :
    #     - Map your data objects and fields with the Pivotal Ontology
    #     - Create your translation rules
    #     - Apply the AI Translator on your data using your rules
    #     - Improve AI result by manually validating target framework match suggestions
    # """)
    
    # col1, col2 = st.columns([5, 2])

    # with col1:
    #     widget_documentation()

    # with col2:
    #     widget_checklist()


main()