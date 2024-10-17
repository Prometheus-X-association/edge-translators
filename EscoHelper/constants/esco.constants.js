const supportedLanguages = [
    'en','fr','fi','es','de',
];

const escoOntology = {};

const ESCO_TABLE_PREFIX = 'esco_labels_expanded';

async function getEscoOntology(language){
    const fileLocation = process.env.LOCATION_ESCO_FILES;
    const filePrefix = ESCO_TABLE_PREFIX;
    var url = `${fileLocation}/${filePrefix}_${language}.json`;
    try {
        const response = await fetch(url);
        return response.json();    
    } catch (error) {
        console.log(`An error occurred loading ESCO with language="${language}" -> ${error.message}`);
        return [];
    }
}

async function loadEscoOntology(languages){
    if (!Array.isArray(languages)) languages = supportedLanguages;

    for (let i = 0; i < languages.length; i++) {
        const lang = languages[i];
        if (!supportedLanguages.includes(lang)){
            console.log(`Warning: Skipping unsuported language ${lang}`); continue;
        }
        const data = await getEscoOntology(lang);
        escoOntology[lang] = data;
    }
}

const EscoConstants = {
    escoOntology,
    supportedLanguages,
    loadEscoOntology,
};

module.exports = EscoConstants;