const express = require('express');
const EscoRouter = express.Router();
const EscoController = require('../controllers/esco.controller');

/**
 *  @openapi
 *  /esco/getLabel:
 *  post:
 *      summary: Get ESCO Label from URI
 *      description: Get the Official ESCO Label based on a give URI and a specified language.
 *      requestBody:
 *          required: true
 *          content:
 *              application/json:
 *                  schema:
 *                      type: object
 *                      properties:
 *                          language:
 *                              type: string
 *                              description: Language of the label to be obtained. It must be formatted following the ISO 639-2 standard (2-letter language code)
 *                              example: en
 *                          uri:
 *                              type: string
 *                              description: URI of the ESCO Concept
 *                              example: edebd83d-35f6-4ed5-a940-6c203d178c01
 *      responses:
 *          200:
 *              description: This will return success message upon successful request
 *              content:
 *                  application/json:
 *                      schema:
 *                        type: object
 *                        properties:
 *                          label:
 *                            type: string
 *                            description: Label of the ESCO Concept in the specified language
 *                            example: data science
 */
EscoRouter.post('/getLabel', 
    EscoController.languageValidator('language'), 
    EscoController.getLabel);

/**
 *  @openapi
 *  /esco/getClosestLabel:
 *  post:
 *      summary: Gets the ESCO Label that approximates syntactically the most to the specified term.
 *      requestBody:
 *          required: true
 *          content:
 *              application/json:
 *                  schema:
 *                      type: object
 *                      properties:
 *                          label:
 *                              type: string
 *                              description: Label used to search exact ESCO term
 *                              example: Data Science
 *                          language:
 *                              type: string
 *                              description: Language of the label to be obtained. It must be formatted following the ISO 639-2 standard (2-letter language code)
 *                              example: en
 *                          maxDistance:
 *                              type: number
 *                              description: If value is greater than zero, the algoritm will calculate the syntactic distance between the given labels and the list of labels available in ESCO Ontology. Value equal to zero means that only exact matches will be allowed. If you want to have more flexibility in the detection of the ESCO labels, recommended value is 2 (plural/singular matching or small typo handling).
 *                              example: 0
 *                          enableSynonyms:
 *                              type: boolean
 *                              description: If value is true, enables the search over a list of synonyms that were generated in advance to expand the capabilites of the detector. Otherwise, search will occur only over ESCO concepts. Default value is False to guarantee maximum precision on the operations.
 *                              example: false
 *      responses:
 *          200:
 *              description: This will return success message upon successful request
 *              content:
 *                  application/json:
 *                      schema:
 *                        type: object
 *                        properties:
 *                          closestLabel:
 *                              type: string
 *                              description: Label of the ESCO Concept that approximates the most to the given term.
 *                              example: project leader
 *                          typeClosestLabel:
 *                              type: string
 *                              description: Type of the concept that matches with the given term (preferredLabel / altLabel / synonym)
 *                              example: altLabel
 *                          distance:
 *                              type: integer
 *                              description: Syntactical distance between the given term and the closest ESCO concept
 *                              example: 1
 *                          preferredLabel:
 *                              type: string
 *                              description: Preferred label of the matching concept 
 *                              example: project manager
 *                          uri:
 *                              type: string
 *                              description: URI of the ESCO Concept that approximates the most to the given term.
 *                              example: bea99fea-0383-4c63-b944-70d4799de2c5
 *                          
 */
EscoRouter.post('/getClosestLabel', 
    EscoController.languageValidator('language'),
    EscoController.getClosestLabel);

/**
 *  @openapi
 *  /esco/translate:
 *  post:
 *      summary: Translates the given ESCO concept to a given language, detecting closest ESCO label.
 *      requestBody:
 *          required: true
 *          content:
 *              application/json:
 *                  schema:
 *                      type: object
 *                      properties:
 *                          label:
 *                              type: string
 *                              description: Label used to find the translation.
 *                              example: Data Science
 *                          sourceLanguage:
 *                              type: string
 *                              description: Language of the label to be translated.
 *                              example: en
 *                          destLanguage:
 *                              type: string
 *                              description: Destination Language of the translation.
 *                              example: es
 *                          maxDistance:
 *                              type: number
 *                              description: If value is greater than zero, the algoritm will calculate the syntactic distance between the given labels and the list of labels available in ESCO Ontology. Value equal to zero means that only exact matches will be allowed. If you want to have more flexibility in the detection of the ESCO labels, recommended value is 2 (plural/singular matching or small typo handling).
 *                              example: 0
 *                          enableSynonyms:
 *                              type: boolean
 *                              description: If value is true, enables the search over a list of synonyms that were generated in advance to expand the capabilites of the detector. Otherwise, search will occur only over ESCO concepts. Default value is False to guarantee maximum precision on the operations.
 *                              example: false
 * 
 *      responses:
 *          200:
 *              description: This will return success message upon successful request
 *              content:
 *                  application/json:
 *                      schema:
 *                        type: object
 *                        properties:
 *                          translation:
 *                            type: string
 *                            description: Label of the ESCO Concept that approximates the most to the given term.
 *                            example: data science
 *                          closestLabel:
 *                            type: string
 *                            description: Label of the ESCO Concept that approximates the most to the given term.
 *                            example: project leader
 *                          typeClosestLabel:
 *                            type: string
 *                            description: Type of the concept that matches with the given term (preferredLabel / altLabel / synonym)
 *                            example: altLabel
 *                          distance:
 *                            type: integer
 *                            description: Syntactical distance between the given term and the closest ESCO concept
 *                            example: 1
 *                          preferredLabel:
 *                            type: string
 *                            description: Preferred label of the matching concept
 *                            example: project manager
 *                          uri:
 *                            type: string
 *                            description: URI of the ESCO Concept that approximates the most to the given term.
 *                            example: bea99fea-0383-4c63-b944-70d4799de2c5
 */
EscoRouter.post('/translate', 
    EscoController.languageValidator('sourceLanguage'),
    EscoController.languageValidator('destLanguage'),
    EscoController.translate);

module.exports = EscoRouter;