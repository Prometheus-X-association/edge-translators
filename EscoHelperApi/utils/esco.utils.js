const EscoConstants = require("../constants/esco.constants");
const DistanceUtils = require("./distance.utils");

function getEscoLabel(uri, language){
    if (typeof(uri) !== 'string') return null;
    const ontology = EscoConstants.escoOntology[language];
    for (let i = 0; i < ontology.length; i++) {
        const concept = ontology[i];
        if (uri == concept.uri && concept.type == 'preferredLabel') return concept['label'];
    }
}

function getClosestLabel(label, language, maxDistance, enableSynonyms){
    // Casts value
    enableSynonyms = enableSynonyms == true;

    var ontology = EscoConstants.escoOntology[language];
    var closestDistance = 1000;
    var closest = null;
    for (var i = 0 ; i < ontology.length; i++){
        const isSynonym = (ontology[i]?.type == 'synonym');
        if (!enableSynonyms && isSynonym) continue;

        const label2 = ontology[i]['label'];

        // TEMPORAL DISTANCE IMPROVEMENTS //
        if (Math.abs(label2.length - label.length) > maxDistance) continue;
        ////////////////////////////////////

        const distance = DistanceUtils.levenshtein(label.toLowerCase(), label2.toLowerCase());
        if (distance < closestDistance){
            closestDistance = distance;
            closest = ontology[i];
        }
    }

    if (closest == null) return null;

    if (closestDistance > this.maximumDistance) closest = null;

    return {
        label : closest.label,
        uri : closest.uri,
        distance : closestDistance,
    };
}

const EscoUtils = {
    getEscoLabel,
    getClosestLabel,
}

module.exports = EscoUtils;