const EscoConstants = require("../constants/esco.constants");
const EscoUtils = require("../utils/esco.utils");

async function getLabel(req,res){
    const {
        uri, language
    } = req.body;

    const label = EscoUtils.getEscoLabel(uri, language);

    if (label == null){
        return res.status(200).json({
            'error':'Requested URI not found in ESCO',
        });
    }

    const response = {
        label : label,
    }

    return res.status(200).json(response);
}

async function getClosestLabel(req,res){
    const {
        label, language, maxDistance,
    } = req.body;

    const enableSynonyms = req.body.enableSynonyms == true;

    const responseClosest = EscoUtils.getClosestLabel(label, language, maxDistance, enableSynonyms);

    const response = {
        label : responseClosest.label,
        uri : responseClosest.uri,
        distance : responseClosest.distance,
    }

    return res.status(200).json(response);
}

async function translate(req,res){
    const {
        label, sourceLanguage, destLanguage,
    } = req.body;

    // Default Distance is 0 -> Exact match
    const maxDistance = req.body.maxDistance || 0;
    
    // Disabled if not defined. Only enabled if explicitly set as true
    const enableSynonyms = req.body?.enableSynonyms === true;

    var responseClosest = EscoUtils.getClosestLabel(label, sourceLanguage, maxDistance, enableSynonyms);

    const translation = EscoUtils.getEscoLabel(responseClosest.uri, destLanguage);;

    const response = {
        translation,
        uri: responseClosest.uri,
        original : label,
        detectedEscoLabel : responseClosest.label,
        distance: responseClosest.distance,
    }

    if (responseClosest.distance == 0){
        delete response.original;
        delete response.detectedEscoLabel;
        delete response.distance;
    }

    return res.status(200).json(response);
}

function languageValidator(fieldName){
    async function validateLanguage(req,res, next){
        const language = req.body[fieldName];
        if (!EscoConstants.supportedLanguages.includes(language)){
            return res.status(400).json({
                'error': `Language '${language}' is not supported`,
                'supportedLanguages': EscoConstants.supportedLanguages,
                'code': 'LanguageNotSupported',
            });
        }
    
        const esco = EscoConstants.escoOntology[language];
        if (!Array.isArray(esco)){
            const availableLanguages = Object.keys(EscoConstants.escoOntology);
            return res.status(400).json({
                'error': `Language '${language}' is not available`,
                'availableLanguages': availableLanguages,
                'code': 'LanguageNotLoaded',
            });
        }
        next();
    }
    return validateLanguage;
}


const EscoController = {
    getLabel,
    getClosestLabel,
    translate,
    languageValidator,
}

module.exports = EscoController;