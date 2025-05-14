import { getGraph } from '@mmorg/rdfx-graphql'
import { default as xmlDataTypes } from '@mmorg/rdfx-onto-xml-datatypes'
import { default as rdf } from '@mmorg/rdfx-onto-rdf' 
import { default as rdfs } from '@mmorg/rdfx-onto-rdfs'


// loading the "Ontology World"
export default function loadWorldGraph() {
  return getGraph(xmlDataTypes, rdf, rdfs)
}
