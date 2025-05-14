import streamlit as st
import pandas as pd
import numpy as np
from stqdm import stqdm
import json 

################################### SKILL MATCHING #############################################################

@st.cache_data(ttl=3600)
def skill_match(formation_title, target_framework):
    # Get the formation vector
    embeddings = st.session_state.formation_embeddings
    
    if formation_title not in embeddings:
        st.warning(f"No embeddings found for {formation_title}.")
        return []

    vector = np.array(embeddings[formation_title])
    
    adjusted_vector = (vector - 0.5 * np.array(st.session_state.get("bias", []))).tolist()

    # Determine the type to match based on the target framework
    type_match = {
        "ESCO": {"match": {"type": "esco:Skill"}},
        "ROME": {"match": {"type": "rome:alias/Skill_rome"}},
    }.get(target_framework, {"match": {"type": "rome:alias/Skill_rome"}})

    # Elasticsearch query
    query = {
        "bool": {
            "must": [
                {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                            "params": {"query_vector": adjusted_vector},
                        },
                    }
                },
                type_match,
            ]
        }
    }

    response = st.session_state.ES.search(
        index=".ent-search-engine-documents-ariane-first-test",
        query=query,
        source=["pref_label__value"],
        size=100,
    )

    return [
        {
            "Skill ID": f"{target_framework} / skill / {res['_id'][-6:]}",
            "Skill Label": res["_source"]["pref_label__value"],
            "Score": round(res["_score"] / 5 * 100, 2),
        }
        for res in response["hits"]["hits"]
    ]

################################### SIDEBAR #############################################################

def display_sidebar():
    st.sidebar.header("Use Cases", divider="red")
    st.sidebar.button("GEN", use_container_width=True)

    st.sidebar.header("Target Framework", divider="red")
    st.sidebar.selectbox(
        "Select Target Framework",
        ["ROME", "ESCO"],
        key="target"
    )

    st.sidebar.header("Catalogue", divider="red")

    all_formations = list(st.session_state.data_to_match["formations"].values())

    formation_titles = [formation["prefLabel"] for formation in all_formations]
    selectedFormationTitle = st.sidebar.selectbox(
        "Select your Item",
        formation_titles,
        key="selectedFormationTitle",
    )

    st.session_state.selectedFormation = next(
        (f for f in all_formations if f["prefLabel"] == st.session_state.selectedFormationTitle), None
    )

################################### TRAINING DISPLAY #############################################################

def display_formation():
    st.header("Formation Details", divider="red")

    if st.session_state.selectedFormation:
        formation = st.session_state.selectedFormation
        st.subheader(formation["prefLabel"], divider="blue")
        st.write(formation.get("description", "No description available."))

################################### SKILL SUGGESTIONS #############################################################

def display_rome_skills():
    tabs = st.tabs(["Validation","All Matches"])
    with tabs[0]:
        st.header("Suggested Skills", divider="red")
        formation_title = st.session_state.selectedFormation["prefLabel"]
        suggestions = skill_match(formation_title, st.session_state.target)
        suggestions_df = pd.DataFrame(suggestions)

        if not suggestions_df.empty:
            # Display the dataframe with row selection enabled
            event = st.dataframe(
                suggestions_df[['Skill Label', 'Score']],
                use_container_width=True,
                hide_index=True,
                key="skill_selection",
                on_select="rerun",
                selection_mode="multi-row",
            )

            if event.selection:
                # Retrieve the selected rows
                selected_rows = suggestions_df.iloc[event.selection["rows"]]

                if st.button("Validate Selected Skills"):
                    # Add validated skills to session state
                    validated_skills = selected_rows[['Skill Label']].copy()
                    validated_skills["Framework"] = st.session_state.target
                    validated_skills["Formation Title"] = formation_title
                    st.session_state["validated_skills"] = pd.concat(
                        [st.session_state.get("validated_skills", pd.DataFrame()), validated_skills],
                        ignore_index=True
                    ).drop_duplicates()
                    st.toast("Selected skills validated.")
                    st.rerun()
            else:
                st.info("Select rows to validate skills.")
        else:
            st.write("No skill suggestions available.")

    with tabs[1]:
        # Display the validated skills
        st.subheader("Validated Skills")
        if "validated_skills" in st.session_state and not st.session_state["validated_skills"].empty:
            st.dataframe(
                st.session_state["validated_skills"],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("No validated skills yet.")

################################### GET VECTORS #####################################################################

def get_vectors():
    model = st.session_state.model
    data_to_match = st.session_state.data_to_match["formations"].values()
    descriptions = [formation["description"] for formation in data_to_match]
    labels = [formation["prefLabel"] for formation in data_to_match]
    encoded_vectors = list(stqdm(model.encode(descriptions), unit="experiences"))
    formation_embeddings = dict(zip(labels, encoded_vectors))
    st.session_state.formation_embeddings = formation_embeddings

################################### APP LOGIC #############################################################

def skill_extraction():
    st.markdown("### Training Enhancing Tool :material/school:")
    st.caption("_little description here to be done_")

    if 'data_to_match' not in st.session_state or len(st.session_state.data_to_match["formations"])==0:
        st.info("No data to match. Please go back to the mapping page and generate the data.")
    elif 'data_to_match' in st.session_state and 'formations' not in st.session_state.data_to_match:
        st.warning("No educational experiences in the mappings.")
    else:
        st.session_state.total_formations = len(st.session_state.data_to_match["formations"])
        if "formation_embeddings" not in st.session_state:
            # with st.spinner(f"Processing the formations"):
            get_vectors()
            st.session_state["bias"] = json.load(open("data/bias.json"))
        if "validated_skills" not in st.session_state:
            st.session_state["validated_skills"] = pd.DataFrame(columns=["Formation Title", "Framework", "Skill Label"])
        display_sidebar()
        display_formation()
        display_rome_skills()

skill_extraction()
