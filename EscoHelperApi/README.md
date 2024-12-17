# ESCO Helper - Backend Application

## Prerequisites

* NodeJS >= 20.6.x
* npm (Node Package Manager)
* pm2 (Process Manager)

Development Dependencies

* nodemon (You can apply real-time changes during dev without reloading the process)

## Install Prerequisites for Dev Environment

```
npm install pm2 -g
npm install nodemon -g
```

## Explanation of the .env variables

* **IP:** Network Address where Backend will be available.
* **PORT:** Port under specified IP where Backend will be available.
* **ESCO_FILES_LOCATION:** Main Directory or path where ESCO Tables will be fetched via HTTP GET request.
* **ESCO_FILES_PREFIX:** Prefix in the name of the ESCO Table files.

## Usage

1. You must install the code dependencies of both systems (Frontend and Backend)

   ```
   cd edge-translators/EscoHelper/
   npm install
   ```
2. Copy the file called .env.template and setup the respective variables.

   ```
   cp .env.sample .env
   ```

3. Execute the application as a Linux Daemon using PM2:

   ```
   pm2-runtime process.dev.json
   ```

   If you want to execute the system in the production environment you can execute:

   ```
   pm2 start process.json
   ```

   If the program is already running, you can refresh it executing:

   ```
   pm2 restart process.json
   ```

   Alternatively, you can execute it directly without using pm2:

   ```
   npm start
   ```

## API Documentation

Each API endpoint has been documented using OpenAPI standard. This documentation is rendered via SwaggerUI. You can access it at **/api/v1/swagger/**