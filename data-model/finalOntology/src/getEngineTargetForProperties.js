import { getGraph, diffEntity } from '@mmorg/rdfx-graphql'
import hash from 'object-hash'

// generate the engines `metadata on rdf triples` for properties on the current ontology
export default function getEngineTargetForProperties(ontology, extraEngineOntology, ld_met_previous) {
  const graph_met_target = []

  // 1/ apply generation rules for properties 

  const graph_main = getGraph(ontology)

  // a) byDomain rules: Check ObjectProperty values engines for domain-classes assigned to an engine (via extra-engine.jsonld)
  // This will generate additionnal metadata-on-triple when needed.
  const checkProperty = 'domain'

  const withEngine = extraEngineOntology.graph
  for (const we of withEngine) {

    const propertiesAttached = graph_main.filterBy(checkProperty, we.id)

    // check each property and create the related metadata-on-triple if needed
    for (const prop of propertiesAttached) {
      if (prop?.domain?.length > 1) {
        const subject = prop.id
        const predicate = checkProperty
        const object = we.id
        const engine = we.engine
        const id = `mmm:${hash([subject, predicate, object])}`

        const _met = {
          id,
          type: ['met:PropertyEngine'],
          subject,
          predicate,
          object,
          engine,
        }

        graph_met_target.push(_met)
      }
    }
  }


  // 2/ compare the generated version with the actual one 
  const entityDiff = diffEntity(graph_met_target, ld_met_previous.graph)
  const diffStats = entityDiff.reduce((acc, diff) => {
    acc.full += diff.type === 'objectDiffFull' ? 1 : 0
    acc.partial += diff.type === 'objectDiffPartial' ? 1 : 0
    return acc
  }, { full: 0, partial: 0 })

  if (!diffStats.full && !diffStats.partial) {
    console.log('met-for-engines: There is no changes in the new file')
  } else {
    console.log(`met-for-engines: There is ${diffStats.full} mapping added and ${diffStats.partial} mapping changed`)
  }

  const ld_met = {
    '@context': ld_met_previous['@context'],
    graph: graph_met_target
  }
  return ld_met
}