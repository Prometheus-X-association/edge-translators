const esco = require('../lib/esco-helper');

const supportedLanguages = esco.constants.esco.supportedLanguages;

const props = {
    filesLocation: process.env.ESCO_FILES_LOCATION,
    filePrefix: process.env.ESCO_FILES_PREFIX,
    maxDistance: 2,
    enableSynonyms: false,
};

var escoHelper = new esco.EscoOntology(props);

const EscoConstants = {
    escoHelper,
    supportedLanguages,
};

module.exports = EscoConstants;