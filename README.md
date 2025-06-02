# AI Translator

The Edge Translator Building Block is the core component for translating input data format and value to a standard output.  

The main benefit of the Translator lies in its ability to ensure the interoperability of jobs, skills and qualifications data.

The AI Translator Building Block is able to receive skills data from a single or multiple sources through an API and translate it into the requested output format/language in real time. The skills framework translations may include any national one to the international ESCO, between almost all the European languages, as well as any Json data structure to Json-ld.

## Design Document

See the [design document](docs/DESIGN_DOCUMENT.md).

## Check AI Translator Cloud

- [AI Translator UI](https://ai-translator-ui-934098617065.europe-west1.run.app/)
- [AI Translator API Swagger](https://ai-translator-api-934098617065.europe-west1.run.app/docs)

## Features

- AI Translator
- Framework Repository (ESCO, ROME)
- ESCO Language Translation (HeadAI EscoHelper)

## Project architecture

![building_block_architecture](docs/images/building_block_architecture.png)

## External Dependencies

- **Elasticsearch 8.6.2** : framework repository (esco, rome,..), rules, matchings,..
- **PostgreSQL 16** : provider accounts

## Resources minimal requirements

- Disk : `30 Go`
- RAM : `8 Go`
- CPU : `1 CPU 8 core or 8 vCPU`
- _(optional)_ GPU : `1 or more` _(not mandatory but it will increase speed)_

## Local development environment

### Using Docker / Docker Compose

```sh
# Step 1 : Clone the repository
git clone git@github.com:Prometheus-X-association/edge-translators.git

# Step 2 : Navigate to folder
cd edge-translators/

# Step 3 : Handle environment files of each component
cp api/.env.dist api/.env
cp ui/.env.dist ui/.env
cp esco-helper/.env.dist esco-helper/.env

# Step 4 : Start the AI Translator
docker compose up --build

# Step 5 : Load data (this script require execution permissions `sudo chmod -R +x scripts`)
# You need to load data in Elasticsearch (jobs and skills related data) and PostgreSQL (user table for authentication)
make load-all
# OR
./scripts/import_es.sh
docker compose exec api python -m fixtures.load_all
```

if you want to do a fresh start, you can use `make reset-all` then again `make load-all`

### Check running services

- AI Translator UI : http://localhost:8501
- AI Translator Admin : http://localhost:8501
- AI Translator API : http://localhost:8000/docs
- HeadAI EscoHelper API : http://localhost:8080/api/v1/swagger
- Elasticsearch : http://localhost:9200
- PostgreSQL : http://localhost:5432

## Run tests

check in [TESTS.md](docs/TESTS.md)

## Example usage

> ℹ️ To use the translator you need your Translation Rules. This can be done by API, but will be complicated to understand how to setup Rules via API. Prefer using the UI to setup the Rules, according to the data you want to translate, then you will be able to use the Translator on your data using the API

| Endpoint             | HTTP Method | Example parameters                                        | Example input (request body) | Expected output                                                                |
|----------------------|-------------|-----------------------------------------------------------|------------------------------|--------------------------------------------------------------------------------|
| `/transform` | POST | <ul><li>_(string)_ **target_framework**: `ESCO` _(default)_,  `ROME`</li><li>_(string)_ **language_source**: `en`, `fr` _(default)_, `fi`, `es`, `de`</li><li>_(string)_ **language_source**: `en`, `fr` _(default)_, `fi`, `es`, `de`</li></ul>| check this [input data example](docs/data-examples/faketestprovider/data_full_3_profiles.json) | 200 OK with the your enhanced data as output. See [the example response](docs/data-examples/faketestprovider/output.data_full_3_profiles.jsonld) |


More infos in the [Tests definitions](docs/TESTS.md)

## Deploy in production

We use docker so you can deploy in any cloud provider / personal servers.

Some supported examples:
- Google Cloud : Cloud Run, Kubernetes Engine, Compute Engine,..
- AWS : EC2, ECS, EKS,...
- on your own computer

For development, docker compose start an elasticsearch and postgresql local instances.
**For production, please use your own Elasticsearch and PostgreSQL instances.**

Prerequisit:
- Elasticsearch instance available
- PostgreSQL instance available


Environment variables:
- check in api/.env.dist and replace with approriate values
- check in esco-helper/.env.dist and replace with approriate values
- check in ui/.env.dist and replace with approriate values

You'll need to deploy:
- the **api** using `runtime_prod` docker build target
- the **ui** using `runtime_prod` docker build target
- the **esco-helper** using `runtime` docker build target

You'll also need to download and store the LLM model `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` [available here](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2). You can use the `api/fetch_model.py` command or manually download it in the folder `api/src/.model/`.

For exemple using GCP Cloud Run serverless service, you can store the model in Google Cloud Storage, and use volume mount to make it available for the API _(will work the same in AWS using ECS and S3)_.

## ❓ FAQ

### What is the EDGE AI Translator ?

> The **EDGE AI Translator** is a tool to help achieve **Frictionless Data Interoperability in data transactions.** 
> Check the [Design Document](docs/DESIGN_DOCUMENT.md)

### What are the possible usecases for the EDGE AI Translator ?

> Every data providers that have non standard Skills & Jobs related data who want to enhance their data and match with standard Frameworks like ESCO, ROME,..

### Is the EDGE AI Translator opensource ?

> Yes, the EDGE AI Translator is fully opensource, feel free to install your own EDGE AI Translator.

### Do we send data to any AI API like OpenAI & co

> No, we only use a multilingual LLM opensource model from HugginFace called `paraphrase-multilingual-mpnet-base-v2`. This model set in directly in the service, and dont send any data to any external AI API.

### What are the requirements to install the EDGE AI Translator ?

> You can easily set up the EDGE AI Translator on your infrastructure, even on your computer, see the set up document in this README.md

---

## 🆘 Need Help?

* Read our documentation
    * [README.md](README.md)
    * [Design Document](docs/DESIGN_DOCUMENT.md)
    * [How to use the AI Translator](docs/HOW_TO_USE.md)
    * [Rules specifications](docs/RULES_SPECIFICATIONS.md)
    * [Tests documentation](docs/TESTS.md)
* Found a bug ? You want to propose some changes ? Need some access for the cloud version ? Don't hesitate to [open a issue](https://github.com/Prometheus-X-association/edge-translators/issues/new) nor [create a pull request](https://github.com/Prometheus-X-association/edge-translators/compare)

---