const esco = require('../lib/esco-helper');

const supportedLanguages = esco.constants.esco.supportedLanguages;

const props = {
    filesLocation: process.env.LOCATION_ESCO_FILES,
    maxDistance: 2,
    enableSynonyms: false,
};

var escoHelper = new esco.EscoOntology(props);

const EscoConstants = {
    escoHelper,
    supportedLanguages,
};

module.exports = EscoConstants;