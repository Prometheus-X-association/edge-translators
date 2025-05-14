import { dirname } from 'path'
import { fileURLToPath } from 'url'
// const __dirname = dirname(fileURLToPath(import.meta.url))
import fs from 'fs'
import YAML from 'yaml'
import { readData, readJson, saveJson } from '@mmorg/fsutils'
import loadWorldGraph from './src/loadWorldGraph.js'
import textView from './src/textView.js'
import parseYamlModels from './rdfx-from-yaml/parseYamlModels.js'
import { updateStrategies, updateLayers } from "@mmorg/rdfx-layer";
import contextBuilder from './src/contextBuilder'

// cd data/soo
// pnpm vn generate.js 

const ontoPart = {
  name: 'onto-soo',
  version: '1.0.0'
}
const ontoPath = `./${ontoPart.name}-${ontoPart.version}.jsonld`
const ontoContextPath = `./${ontoPart.name}-context-${ontoPart.version}.jsonld`

const modelFolder = `${__dirname}/model`
const otherGraph = []

const worldGraph = loadWorldGraph()
const model = YAML.parse(readData(`${__dirname}/model/model.yaml`))

// load the pre-existing context to get the rdfs properties 
// @TODO: load a std context from rdf & rdfs (they will be shaped after that)
const context = readJson(ontoPath)['@context']


console.log('Generate the mms skills profile ontology')

const current_ld = parseYamlModels({ context, worldGraph }, model)

// @TODO: put this Ontology entity into a yml file
current_ld.graph.push(getOntologyEntity())
const loaded = otherGraph.map(path => readJson(path))

const aggregated_ld = mergeOntologies(current_ld, ...loaded)

saveJson(aggregated_ld, ontoPath)

console.log(textView(aggregated_ld), '===')

// generate the "implementation context" : the context to use when the ontology is used 
const implementationContext = contextBuilder(aggregated_ld)
saveJson({ '@context': implementationContext }, ontoContextPath)


function getOntologyEntity() {
  return {
    "id": "mms:Ontology",
    "type": [
      "owl:Ontology"
    ],
    "title": [
      {
        "@language": "en",
        "@value": "Ontologie for Competencies & Skills Profiles"
      }
    ],
    "contributor": [],
    "creator": [
      {
        "@language": "fr",
        "@value": "Florent André (mindmatcher.org)"
      }
    ],
    "__description": [
      {
        "@language": "fr",
        "@value": "Ontologie pour la description d'un profil de compétences"
      }
    ],
    "imports": []
  }
}

function mergeOntologies(ld1, ...ld2) {
  const sourceLayer = {
    ld: ld1,
  };

  const otherLayers = ld2.map((ld) => ({
    updateStrategy: updateStrategies.add,
    ld,
  }));

  const mergedLayer = updateLayers(sourceLayer, otherLayers);
  // updateExternalEngine(mergedLayer.ld, extraEngineOntology)
  return mergedLayer.ld;
}