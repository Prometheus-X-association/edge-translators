// Dependencies
const express = require('express');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
dotenv.config();

const cors = require('cors');

const mainRouter = require('./routes/index.route');
const { escoHelper } = require('./constants/esco.constants');

async function startServer(){
    // Load External Variables in Environment
    
    
    await escoHelper.loadOntology();

    // Build Express App
    const app = express();

    // CORS
    app.use(cors());

    const PORT = process.env.PORT;
    const IP = process.env.IP;

    // This value must be changed also in /etc/nginx/nginx.conf
    const MAX_FILE_SIZE = '5mb';

    // Enables receiving Body in Requests, otherwise body is empty
    app.use(bodyParser.urlencoded({ extended : false, limit : MAX_FILE_SIZE }));
    app.use(bodyParser.json({ limit : MAX_FILE_SIZE }));

    // Routes -> This must be at the end of the Controller definition, otherwise other controllers will not be executed
    app.use('/api/v1/', mainRouter);

    // Use specified port to run the application
    app.listen(PORT, IP, () => console.log(`Express app running on port ${PORT}!`));
}

startServer();