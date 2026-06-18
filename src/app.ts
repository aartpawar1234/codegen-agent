import express from 'express';
import { pingRouter } from './routes/ping.route';

/**
 * Main application class.
 */
class App {
  public app: express.Application;

  constructor() {
    this.app = express();
    this.middleware();
    this.routes();
  }

  /**
   * Sets up application middleware.
   */
  private middleware(): void {
    this.app.use(express.json());
  }

  /**
   * Registers application routes.
   */
  private routes(): void {
    this.app.use('/', pingRouter);
  }
}

export const app = new App().app;