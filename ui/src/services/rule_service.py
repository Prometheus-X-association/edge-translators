import streamlit as st
from schemas.rule import Rule

def create_rule_v2(field) -> None:
    target_class = st.session_state[f'object_{field}']['class']
    generate_id = f"generateID_{field}" in st.session_state
    if generate_id:
        create_rule_generate_id(field, target_class)
        create_mandatory_properties_rule(field, target_class)

    match target_class:
        case "Profile":
            create_profile_rule(field, target_class)
        case "Experience":
            create_experience_rule(field, target_class)
        case "Skill":
            create_skill_rule(field, target_class)

def create_rule_generate_id(field: str, target_class: str) -> None:
    rule = Rule()
    rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
    rule.sourcePath = field
    rule.targetClass = f"soo:{target_class}"
    rule.generateId = True

    st.session_state.mappingList.append(rule.__dict__)

def create_mandatory_properties_rule(field: str, target_class: str) -> None:

    match target_class:
        case "Profile":
            pass

        case "Experience":
            relation_rule = Rule()
            relation_rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
            relation_rule.sourcePath = field
            relation_rule.targetClass = f"soo:{target_class}"
            relation_rule.relationTo = "soo:Profile"
            relation_rule.relationName = "soo:profile"
            relation_rule.relationNameInverse = "soo:experience"
            st.session_state.mappingList.append(relation_rule.__dict__)

            type_rule = Rule()
            type_rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
            type_rule.sourcePath = field
            type_rule.targetClass = f"soo:{target_class}"
            type_rule.targetProperty = "soo:experienceType"
            type_rule.targetValue = f"term:experience/type/{st.session_state[f'object_{field}']['type'].replace(' ','')}"
            st.session_state.mappingList.append(type_rule.__dict__)

            status_rule = Rule()
            status_rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
            status_rule.sourcePath = field
            status_rule.targetClass = f"soo:{target_class}"
            status_rule.targetProperty = "soo:experienceStatus"
            status_rule.targetValue = f"term:experience/status/{st.session_state[f'object_{field}']['status']}"
            st.session_state.mappingList.append(status_rule.__dict__)

        case "Skill":
            relation_rule = Rule()
            relation_rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
            relation_rule.sourcePath = field
            relation_rule.targetClass = f"soo:{target_class}"
            relation_rule.relationTo = "soo:Experience"
            relation_rule.relationName = "soo:experience"
            relation_rule.relationNameInverse = "soo:skill"
            st.session_state.mappingList.append(relation_rule.__dict__)

            relation_rule = Rule()
            relation_rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
            relation_rule.sourcePath = field
            relation_rule.targetClass = f"soo:{target_class}"
            relation_rule.relationTo = "soo:Profile"
            relation_rule.relationName = "soo:profile"
            relation_rule.relationNameInverse = "soo:skill"
            st.session_state.mappingList.append(relation_rule.__dict__)

def create_profile_rule(field: str, target_class: str):
    rule = Rule()
    rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
    rule.sourcePath = field
    rule.targetClass = f"soo:{target_class}"
    rule.targetProperty = f"soo:{st.session_state[f'property4{field}']}"

    st.session_state.mappingList.append(rule.__dict__)

def create_experience_rule(field: str, target_class: str) -> None:
    rule = Rule()
    rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
    rule.sourcePath = field
    rule.targetClass = f"soo:{target_class}"
    rule.targetProperty = f"soo:{st.session_state[f'property4{field}']}"

    match st.session_state[f'property4{field}']:
        case "prefLabel":
            rule.targetFunction = "fno:find-matching"

        case "dateFrom" | "dateTo":
            rule.targetFunction = "fno:date-to-xsd"
            rule.targetFunctionParam = f"param:{st.session_state[f'dateformat4{field}']}"

        case "family":
            rule.targetFunction = "fno:handle-family"

        case "polarity":
            rule.targetFunction = "fno:handle-polarity"
    
    st.session_state.mappingList.append(rule.__dict__)

def create_skill_rule(field: str, target_class: str) -> None:
    rule = Rule()
    rule.id = f"mmr:rule-{len(st.session_state.mappingList)}"
    rule.sourcePath = field
    rule.targetClass = f"soo:{target_class}"
    rule.targetProperty = f"soo:{st.session_state[f'property4{field}']}"

    match st.session_state[f'property4{field}']:
        case "prefLabel":
            rule.targetFunction = "fno:find-matching"

        case "dateFrom" | "dateTo":
            rule.targetFunction = "fno:date-to-xsd"
            rule.targetFunctionParam = f"param:{st.session_state[f'dateformat4{field}']}"

        case "skillLevelValue":
            rule.targetFunction = "fno:skill-value-to-scale"

        case "family":
            rule.targetFunction = "fno:handle-family"

        case "polarity":
            rule.targetFunction = "fno:handle-polarity"    
    
    st.session_state.mappingList.append(rule.__dict__)