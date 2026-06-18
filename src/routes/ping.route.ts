import { Router } from 'express';
import { pingController } from '../controllers/ping.controller';

/**
 * Express router for the /ping endpoint.
 * @type {express.Router}
 */
export const pingRouter = Router();

/**
 * GET /ping route.
 * Returns status and current UTC timestamp.
 */
pingRouter.get('/ping', (req, res) => {
  const response = pingController.get();
  res.json(response);
});