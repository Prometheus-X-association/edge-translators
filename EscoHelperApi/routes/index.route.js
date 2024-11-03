// Routes
const express = require('express');
const EscoRouter = require('./esco.route');
const SwaggerRouter = require('./swagger.route');
const router = express.Router();

// Import all routes
router.use('/esco/', EscoRouter);
router.use('/swagger/', SwaggerRouter);

module.exports = router;