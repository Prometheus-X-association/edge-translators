import { getGraph } from "@mmorg/rdfx-graphql";

const RT_dataType = 'rt_datatype'
const RT_object = 'rt_objet'
const RT_mixed = 'rt_mixed'

const getNs = (id: string): string => id.split(':')[0]
const getPropertyName = (propId: string): string => propId.split(':')[1]


export default function contextBuilder(ontology) {
  // 0/ Get the ontology's properties
  const graph = getGraph(ontology)
  const properties = graph.filterByType('rdf:Property')

  // 1/ Define the basics of the context 
  const context = {
    id: "@id",
    graph: {
      "@id": "@graph",
      "@container": "@set"
    },
    type: {
      "@id": "@type",
      "@container": "@set"
    },
  }

  // 2/ get the NS declarations for the ones used 
  const propNs: Set<string> = new Set(properties.map(prop => getNs(prop.id)))
  for (const sNs of propNs) {
    const ontologyNs = ontology['@context'][sNs]
    if (!ontologyNs) throw new Error('This Ns has to be defined in the source Ontology: ' + sNs)
    context[sNs] = ontologyNs
  }

  // 3/ Create the json-ld aliases for the ontology's properties
  for (const prop of properties) {
    const rangeType = getRangeType(prop.range)
    if (rangeType === RT_mixed) {
      console.log(prop)
      throw new Error('@to_implement: this case has to be implemented')
    }
    const propName = getPropertyName(prop.id)
    if (rangeType === RT_dataType) {
      if (prop.range.length > 1) {
        console.log(prop)
        throw new Error('@To_implement: manage the case of multiple ranged dataTypes')
      }
      context[propName] = {
        '@id': prop.id,
        '@type': prop.range[0],
        '@container': '@set'
      }
    }
    if (rangeType === RT_object) {
      context[propName] = {
        '@id': prop.id,
        '@type': '@id',
        '@container': '@set'
      }
    }
  }
  return context
}


function getRangeType(ranges) {
  const isDataType = range => (range === 'rdf:langString' || getNs(range) === 'xsd')
  // check they are all DataTypes
  if (ranges.every(isDataType)) return RT_dataType
  if (ranges.some(isDataType)) return RT_mixed
  return RT_object
}