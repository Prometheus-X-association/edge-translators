import { dirname } from 'path'
import { fileURLToPath } from 'url'
const __dirname = dirname(fileURLToPath(import.meta.url))
import { readJson } from '@mmorg/fsutils'

export const ontologyFileName = 'mm-skillProfile-1.0.0.jsonld'
export const ontology = readJson(`${__dirname}/${ontologyFileName}`)

export default ontology 
