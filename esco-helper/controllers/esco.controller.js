const EscoConstants = require("../constants/esco.constants");
const { escoHelper } = require("../constants/esco.constants");

async function getLabel(req,res){
    const {
        uri, language
    } = req.body;

    const label = escoHelper.getEscoLabel(uri, language);

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
    
    escoHelper.maxDistance = maxDistance || 0;
    escoHelper.enableSynonyms = enableSynonyms;
    const responseClosest = escoHelper.getClosestLabel(label, language);

    if (responseClosest == null) return res.status(400).json({
        closestLabel: null,
        typeClosestLabel: null,
        distance: null,
        preferredLabel: null,
        translation: null,
        uri: null,
        error: `Label '${label}' doesn't match with any of the Official ESCO Concepts.`
    })

    return res.status(200).json(responseClosest);
}

async function translate(req,res){
    const {
        label, sourceLanguage, destLanguage, maxDistance,
    } = req.body;

    const enableSynonyms = req.body.enableSynonyms == true;
    
    escoHelper.maxDistance = maxDistance || 0;
    escoHelper.enableSynonyms = enableSynonyms;

    const response = escoHelper.translate(label, sourceLanguage, destLanguage);

    if (response == null) return res.status(400).json({
        closestLabel: null,
        typeClosestLabel: null,
        distance: null,
        preferredLabel: null,
        translation: null,
        uri: null,
        error: `Label '${label}' doesn't match with any of the Official ESCO Concepts.`
    })

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
    
        const esco = escoHelper.ontology[language];
        if (!Array.isArray(esco)){
            const availableLanguages = Object.keys(escoHelper.ontology);
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