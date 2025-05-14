import time
import streamlit as st
from client.ontobridge import OntobridgeClient
from elasticsearch import Elasticsearch, NotFoundError

def fetch_matchings(validated, concept_type, framework):
    client = OntobridgeClient()
    response = client.get_matchings(validated=validated, concept_type=concept_type, framework=framework)
    return response.json()

def update_validation(doc_id, new_match, new_suggestions):
    body = {"doc": {"match": new_match, "suggestions": new_suggestions}}
    es_client: Elasticsearch = st.session_state.ES
    try:
        es_client.update(index="edge_matchings", id=doc_id, body=body, refresh="wait_for")
    except NotFoundError as nfe:
        st.error("Could not validate the suggestion.")
        return
    
    st.rerun()

def consolidate_suggestions(current_match, suggestions):
    combined = [current_match] if current_match else []
    suggestions.sort(key=lambda s: s["score"], reverse=True)

    combined.extend(suggestions or [])

    unique_suggestions = {}
    for suggestion in combined:
        suggestion_id = suggestion.get("id") or f"no_id_{id(suggestion)}"
        unique_suggestions.setdefault(suggestion_id, suggestion)

    return unique_suggestions

def render_match(doc, is_validated):
    doc_id = doc["_id"]
    label = doc.get("prefLabel", {}).get("value", "Sans label")
    language_source = doc.get("prefLabel", {}).get("language", "")
    language_target = doc.get("match", {}).get("target", {}).get("prefLabel", {}).get("language", "")

    current_match = doc.get("match")
    suggestions = doc.get("suggestions", [])
    unique_dict = consolidate_suggestions(current_match, suggestions)


    radio_options = [
        s.get("target", {}).get("prefLabel", {}).get("value", "Sans label") for s in unique_dict.values()
    ]

    with st.form(key=f"form_{doc_id}"):
        col1, col2 = st.columns([5, 1], vertical_alignment="bottom")
        col1.markdown(f"""
            #### {label.capitalize()}
            - source language: `{language_source}`
            - translation language: `{language_target}`
        """)
        col1.markdown(f"> {doc.get("description", "")}")

        choice_key = f"choice_{doc_id}" if not is_validated else f"valid_choice_{doc_id}"
        if is_validated:
            subcol1, subcol2, subcol3 = col1.columns([5, 1, 1], vertical_alignment="bottom")
            subcol1.selectbox("Update or delete the validation", options=radio_options, key=choice_key)
            if subcol2.form_submit_button(label="Update", icon=":material/edit:", type="secondary", use_container_width=True):
                selected_label = st.session_state.get(choice_key, "--")
                handle_selection(doc, selected_label, unique_dict)
            if subcol3.form_submit_button(label="Remove", icon=":material/delete:", type="primary", use_container_width=True):
                handle_selection(doc, "--", unique_dict)
        else:
            col1.selectbox(f"Select and validate one **{doc.get("framework").upper()}** match", options=radio_options, key=choice_key)
            if col2.form_submit_button(label="Validate", icon=":material/task_alt:", type="secondary", use_container_width=True):
                selected_label = st.session_state.get(choice_key, "--")
                handle_selection(doc, selected_label, unique_dict)

def handle_selection(doc, selected_label, unique_dict):
    doc_id = doc["_id"]
    if selected_label == "--":
        update_validation(doc_id, {"validated": 0}, list(unique_dict.values()))
        return

    label_to_id = {
        s.get("target", {}).get("prefLabel", {}).get("value", "Sans label"): s_id for s_id, s in unique_dict.items()
    }

    chosen_id = label_to_id[selected_label]
    for suggestion in unique_dict.values():
        suggestion["validated"] = 0

    chosen_suggestion = unique_dict[chosen_id]
    chosen_suggestion["validated"] = 1

    new_match = chosen_suggestion
    new_suggestions = [s for s_id, s in unique_dict.items() if s_id != chosen_id]

    update_validation(doc_id, new_match, new_suggestions)

def main():
    st.markdown("### Suggestions Validation :material/rule:")
    st.caption("_Validate AI Translator suggestions to match your preferences._")

    if not st.session_state.get("has_existing_mapping_rules", True):
        st.warning(
            "**MISSING_RULES**: _No rules defined yet. Create transformation rules to process data with the AI Translator._", 
            icon=":material/unknown_document:"
        )
        return

    if "ES" not in st.session_state:
        st.warning("Elasticsearch is not initialized in session state. Configure `st.session_state.ES`.")
        return

    col1, col2 = st.columns(2)
    type_filter = col1.selectbox("Type", ["experience", "skill"])
    framework_filter = col2.selectbox("Framework", ["esco", "rome"])

    with st.spinner("⏳ Loading data..."):
        docs_non_valides = fetch_matchings(validated=False, concept_type=type_filter, framework=framework_filter)
        docs_valides = fetch_matchings(validated=True, concept_type=type_filter, framework=framework_filter)

    if not docs_non_valides and not docs_valides:
        st.info("no data")
        return
    tab_non_valid, tab_valid = st.tabs([f"Pending ({len(docs_non_valides)})", f"Validated ({len(docs_valides)})"])

    with tab_non_valid:
        st.session_state.selected_tab = "tab_non_valid"
        if not docs_non_valides:
            st.info("no pending match validation, all good 😎")
        else:
            for doc in docs_non_valides:
                render_match(doc, is_validated=False)

    with tab_valid:
        st.session_state.selected_tab = "tab_valid"
        if not docs_valides:
            st.info("no match validated, please validate some suggestions")
        else:
            for doc in docs_valides:
                render_match(doc, is_validated=True)

main()
