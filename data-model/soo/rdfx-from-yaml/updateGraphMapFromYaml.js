import getApiLabel from '@mmorg/rdfx-graphql/src/rdfx-id/getApiLabel.js'
import createClass from './src/createClass.js'
import createProperty from './src/createProperty.js'
import { updateEntity, updateStrategies } from '@mmorg/rdfx-layer'


export default function updateGraphMapFromYaml(graphMap, model, worldGraph){

  for (const [klassId, prop] of Object.entries(model.triple)) {
    const klass = getOrCreateClass(klassId)
    graphMap.set(klass.id, klass)
  
    for (const [propertyId, range] of Object.entries(prop)) {
      getOrCreateProperty(propertyId, klass, range)
    }
  
  }
  
  function getOrCreateClass(klassId) {
  
    const inCurrentGraph = graphMap.get(klassId)
    const inWorldGraph = worldGraph.findById(klassId)
  
    if (inCurrentGraph) return inCurrentGraph
  
    let entity = null
    if (inWorldGraph) {
      // copy and add to current graph 
      entity = JSON.parse(JSON.stringify(inWorldGraph))
      // @TODO: retrive the linked properties ? 
    }
  
    if (!entity) {
      entity = createClass(klassId)
    }
    // console.log(entity)
    return entity
  }
  
  function getOrCreateProperty(propertyId, klass, rangeOrValue) {
    const inCurrentGraph = graphMap.get(propertyId)
    const inWorldGraph = worldGraph.findById(propertyId)

    // class' descriptives properties processing
    const idStructure = getApiLabel({id : propertyId})
    const isClassDescriptiveProps = ['rdf', 'rdfs', 'owl'].includes(idStructure.ns)
    
    if(isClassDescriptiveProps){ // add the patch to the class
      const patch = {
        id: klass.id,
        [idStructure.label] : rangeOrValue // this is a value here
      }
      updateEntity(updateStrategies.add, klass, patch)
      return 
    }
  
    // Create a new property entity or add patch to the existing one
    const patch =  {
      id: propertyId,
      domain: [klass.id],
      range: Array.isArray(rangeOrValue) ? rangeOrValue : [rangeOrValue],
    }

    // The property do not exist in current or world graph 
    if(!inCurrentGraph && !inWorldGraph){
      const entity = createProperty(patch)
      graphMap.set(entity.id, entity)
      return 
    }

    const entity = inCurrentGraph ? inCurrentGraph : 
      inWorldGraph ? JSON.parse(JSON.stringify(inWorldGraph)) : null
    
  
    // apply patch on existing one 
    updateEntity(updateStrategies.add, entity, patch)
    
    return 
  }
  

}

