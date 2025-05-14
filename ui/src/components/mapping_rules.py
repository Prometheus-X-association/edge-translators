from datetime import datetime
import json
import streamlit as st

def main():
    st.markdown("### View your Rules :material/search:")
    st.caption("_little description here to be done_")

    if st.session_state.has_existing_mapping_rules == False:
        error_type = "MISSING_RULES"
        error_message = "You dont have any rule defined yet. Please create some transformation rules to be able to process data with the AI Translator."
        st.warning(f"**{error_type}**: _{error_message}_", icon=":material/unknown_document:")
        return

    st.code(json.dumps(st.session_state.ruleFile, indent=4), language="json")

main()