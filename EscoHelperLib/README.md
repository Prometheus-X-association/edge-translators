## Export Library as a single JS file optimized for Browsers (Clien-Side)

To compress all the source files (.js and .css) into one single .js file, you must perform the following command:

```
npm install
npx webpack-cli --mode production
```

## Export Library as a single JS file optimized for NodeJS (Server-Side)

To compress all the source files (.js and .css) into one single .js file, you must perform the following command:

```
npm install
npx webpack-cli --mode production --target node
```


## Serve the Library in Development mode

To serve the library locally in development mode, you must execute the following command:

```
webpack-cli serve
```

## Usage

You can create an ESCO Helper specifying the following parameters:

* **filesLocation:** Location where ESCO Tables are being served.

* **enableSynonyms:** If value is true, enables the search over a list of synonyms that were generated in advance to expand the capabilites of the detector. Otherwise, search will occur only over ESCO concepts. Default value is False to guarantee maximum precision on the operations.

* **maxDistance:** If value is greater than zero, the algoritm will calculate the syntactic distance between the given labels and the list of labels available in ESCO Ontology. Value equal to zero means that only exact matches will be allowed. If you want to have more flexibility in the detection of the ESCO labels, recommended value is 2 (plural/singular matching or small typo handling).

```
const props = {
    filesLocation: 'http://example.esco.com/tables',
    maxDistance: 2,
    enableSynonyms: false,
};

var escoHelper = new esco.EscoOntology(props);
```

Load Ontology in all the supported languages (Implementation for Asynchronous function)
```
await escoHelper.loadOntology();

// Your implementation goes here
```

Load Ontology in all the supported languages (Implementation for Synchronous function)
```
escoHelper.loadOntology().then(()=>{
    // Your implementation goes here
})
```

Once the instance is built, you can get the label of an ESCO concept, specifying the UUID of the concept:

```
uri = 'edebd83d-35f6-4ed5-a940-6c203d178c01'
language = 'en'

escoHelper.getEscoLabel(uri,language)

-- RESPONSE --

'data science'
```

You can also find the ESCO term that is closer to a given label:

```
label = 'data sciences'
language = 'en'
escoHelper.getClosestLabel(label,language)


-- RESPONSE --

{
    label: 'data science',
    uri: 'edebd83d-35f6-4ed5-a940-6c203d178c01',
    distance: 1
}
```

ESCO Helper also allows you to merge both operations. The translate() function finds the most similar ESCO term of a given label and translates it to a desired language:

```
label = 'data sciences'
sourceLang = 'en'
destLang = 'es'
escoHelper.translate(label, sourceLang, destLang)

-- RESPONSE --

{
    translation: 'ciencia de datos', 
    uri: 'edebd83d-35f6-4ed5-a940-6c203d178c01',
    original: 'data sciences',
    detectedEscoLabel: 'data science',
    distance: 1
}
```