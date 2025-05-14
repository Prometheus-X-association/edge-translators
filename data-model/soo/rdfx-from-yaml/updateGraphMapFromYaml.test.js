// @ts-ignore
import { describe, expect, it, beforeAll } from "@jest/globals";
import { dirname } from 'path'
import { fileURLToPath } from 'url'
const __dirname = dirname(fileURLToPath(import.meta.url))
import { getGraph } from "@mmorg/rdfx-graphql";
import { readData, readJson } from '@mmorg/fsutils';
import updateGraphMapFromYaml from './updateGraphMapFromYaml.js';
import YAML from 'yaml'

const fixtures = `${__dirname}/__fixtures__`

const readYaml = (path) => YAML.parse(readData(path))

// cd data/mmSkillProfile/
// pnpm test -- --watch updateGraphMapFromYaml.test.js

describe('Basic Parsing - empty worldMap', () => {
  // loading empty "Ontology World"
  const worldMap = getGraph({'@context': {}, graph: []})

  it('should return good ranges for string or array<string>', async () => {
    const testModel = readYaml(`${fixtures}/testModel.yaml`)
    const graphMap = new Map()
    updateGraphMapFromYaml(graphMap, testModel, worldMap)
    
    expect(graphMap.get('mms:personalData').range).toStrictEqual(['mms:PersonalDataWallet'])
    expect(graphMap.get('mms:Address').sameAs).toStrictEqual([ 'mnx:Address', 'hrrdf:AddressType' ])
    expect(graphMap.get('mms:occupation').range).toStrictEqual(['rome:onto/Employment/Job', 'rome:onto/Employment/Position'])
  })


});
