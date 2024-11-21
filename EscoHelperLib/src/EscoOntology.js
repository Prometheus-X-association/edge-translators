const EscoConstants = require("./constants/esco.constants");
const DistanceUtils = require("./utils/distance.utils");

class EscoOntology {
    constructor(props){
        var {
            maxDistance = 0,
            filesLocation = null,
            filePrefix = 'esco_labels_expanded',
        } = props;

        // Initialize attributes
        this.ontology = {};

        // Set properties
        this.maxDistance = maxDistance;
        this.enableSynonyms = props.enableSynonyms === true;
        this.filesLocation = filesLocation;
        this.filePrefix = filePrefix;
    }

    async loadOntology(languages){
        const supportedLanguages = EscoConstants.supportedLanguages;
        const filesLocation = this.filesLocation;
        if (typeof(filesLocation) !== 'string') throw new Error('Invalid value for parameter "filesLocation"');
        if (!Array.isArray(languages)) languages = supportedLanguages;
    
        for (let i = 0; i < languages.length; i++) {
            const lang = languages[i];
            if (!supportedLanguages.includes(lang)){
                console.log(`Warning: Skipping unsuported language ${lang}`); continue;
            }
            const data = await this._getEscoOntology(lang);
            this.ontology[lang] = data;
        }
    }

    async _getEscoOntology(language){
        const fileLocation = this.filesLocation;
        const filePrefix = this.filePrefix;
        var url = `${fileLocation}/${filePrefix}_${language}.json`;
        try {
            const response = await fetch(url);
            return response.json();    
        } catch (error) {
            console.log(`An error occurred loading ESCO with language="${language}" -> ${error.message}`);
            return [];
        }
    }

    getEscoLabel(uri, language){
        if (typeof(uri) !== 'string') return null;
        const ontology = this.ontology[language];
        console.log(this.ontology,language);    

        for (let i = 0; i < ontology.length; i++) {
            const concept = ontology[i];
            if (uri == concept.uri && concept.type == 'preferredLabel') return concept['label'];
        }

        return null;
    }
    
    getClosestLabel(label, language){
        const enableSynonyms = this.enableSynonyms;
    
        var ontology = this.ontology[language];
        var closestDistance = 1000;
        var closest = null;
        for (var i = 0 ; i < ontology.length; i++){
            const isSynonym = (ontology[i]?.type == 'synonym');
            if (!enableSynonyms && isSynonym) continue;
    
            const label2 = ontology[i]['label'];
    
            // TEMPORAL DISTANCE IMPROVEMENTS //
            if (Math.abs(label2.length - label.length) > this.maxDistance) continue;
            ////////////////////////////////////
    
            const distance = DistanceUtils.levenshtein(label.toLowerCase(), label2.toLowerCase());
            if (distance < closestDistance){
                closestDistance = distance;
                closest = ontology[i];
            }
        }
    
        if (closest == null) return null;
    
        if (closestDistance > this.maxDistance) return null;
    
        const preferredLabel = this.getEscoLabel(closest.uri, language);

        return {
            closestLabel: closest.label,
            typeClosestLabel: closest.type,
            preferredLabel: preferredLabel,
            uri: closest.uri,
            distance: closestDistance
        };
    }

    translate(label, sourceLanguage, destLanguage){
        var responseClosest = this.getClosestLabel(label, sourceLanguage);

        if (responseClosest == null) return null;

        const translation = this.getEscoLabel(responseClosest.uri, destLanguage);;
    
        const response = {
            ...responseClosest,
            translation,
        }

        return response;
    }
}

module.exports = EscoOntology;