import updateGraphMapFromYaml from './updateGraphMapFromYaml.js'

export default function parseYamlModels({ context, worldGraph }, ...ymlContents) {
  const graphMap = new Map()

  for (const model of ymlContents.flat()) {
    updateGraphMapFromYaml(graphMap, model, worldGraph)
    // Parse the NS entries if they exist, add them to the context 
    if (model.ns) {
      Object.assign(context, model.ns)
    }
  }

  const ld = {
    "@context": context, // @TODO: generate clean context
    graph: [...graphMap.values()]
  }
  return ld
}
