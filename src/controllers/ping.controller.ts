/**
 * Ping controller that handles the /ping endpoint logic.
 * Returns a status and current UTC timestamp.
 */
export const pingController = {
  /**
   * Handles the GET /ping request.
   * @returns {Object} Response object with status and timestamp.
   */
  get: (): { status: string; timestamp: string } => {
    const timestamp = new Date().toISOString();
    return {
      status: 'ok',
      timestamp,
    };
  },
};