// @ts-ignore
import { dirname, resolve as resolvePath } from "path";
import { fileURLToPath } from "url";
const __dirname = dirname(fileURLToPath(import.meta.url));
import { readJson, saveJson } from "@mmorg/fsutils";
import romeOntology from "@mmorg/onto-rome";
import { updateStrategies, updateLayers } from "@mmorg/rdfx-layer";
import saveIfChanges from './src/saveIfChanges.js';
import getEngineTargetForProperties from './src/getEngineTargetForProperties.js';

// const path_skill = resolvePath(
//   __dirname,
//   `../../data/mmProfile/mm-profile-1.0.0.jsonld`
// );

// const skillProfileOntology = readJson(path_skill);

const extraEnginePath = resolvePath(__dirname, `./extra-engine-1.0.0.jsonld`);
const extraEngineOntology = readJson(extraEnginePath);

const groupedApiPath = resolvePath(__dirname, `./grouped-api-1.0.0.jsonld`);
const groupedApiOntology = readJson(groupedApiPath);

let ontology = mergeOntologies(
  // skillProfileOntology,
  romeOntology,
  extraEngineOntology,
  groupedApiOntology
);


// check if an engine need to be define for the properties of "assigned object"
const path_extraEngineMet = `./extra-engine-1.0.0-met.jsonld`
const ld_met_previous = readJson(resolvePath(__dirname, path_extraEngineMet));
const ld_met = getEngineTargetForProperties(ontology, extraEngineOntology, ld_met_previous)
saveIfChanges(ld_met, ld_met_previous, path_extraEngineMet)


// add this new properties triples to the global ontology 
ontology = mergeOntologies(ontology, ld_met)

// @TODO: use the "saveIfChange" function if concurrency error are frequent on startup
saveJson(ontology, resolvePath(__dirname, `./final-ontology.ld.json`))


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
