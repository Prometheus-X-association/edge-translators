const swaggerJsdoc = require("swagger-jsdoc");
const swaggerUi = require("swagger-ui-express");

// Routes
const express = require('express');
const SwaggerRouter = express.Router();

const options = {
    definition: {
      openapi: "3.1.0",
      info: {
        title: "ESCO Helper API Documentation",
        version: "0.1.0",
        description:
          "ESCO Helper API Documentation",
      },
      servers: [
        {
          url: "http://localhost:8080/api/v1/",
        },
      ],
    },
    apis: ["./routes/*.js"],
  };
  
const specs = swaggerJsdoc(options);

SwaggerRouter.use(
    "/",
    swaggerUi.serve,
    swaggerUi.setup(specs)
);

module.exports = SwaggerRouter;