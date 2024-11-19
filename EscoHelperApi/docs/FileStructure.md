# ESCO Files

## File Structure

ESCO Handler Backend Application requires access to multiple JSON files (ESCO Tables). Each supported language has a unique file, that defines the official labels, the URI and the concept type.

Officially, ESCO Ontology provides two concept types: preferredLabel and altLabel. We have expanded the capacity of the tool generating a list of synonyms, which are represented with type=synonym.

    [
        {
            "label" : "waste inspector",
            "uri" : "b3867d0a-e902-4d88-b0c2-3e0d2cf35c83",
            "type" : "synonym",
            "original": "hazardous materials inspector"
        },{
            "label" : "manage musical staff",
            "uri" : "b3867d0a-e902-4d88-b0c2-3e0d2cf35c83",
            "type" : "preferredLabel"
        },{
            "label" : "solid waste compliance specialist",
            "uri" : "b3867d0a-e902-4d88-b0c2-3e0d2cf35c83",
            "type" : "altLabel"
        },{
            "label" : "...",
            "uri" : "...",
            "type" : "..."
        },{
            ...
        }
    ]