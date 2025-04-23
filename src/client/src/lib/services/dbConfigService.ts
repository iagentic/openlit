import { api } from '../api';
import { DatabaseConfig, APIKey } from '@/types/databaseConfig';

export const dbConfigService = {
  /**
   * Get all database configs for the current user
   */
  async getDatabaseConfigs(): Promise<DatabaseConfig[]> {
    return api.get('/database-configs/');
  },

  /**
   * Create a new database config
   */
  async createDatabaseConfig(config: {
    name: string;
    environment?: string;
    username?: string;
    password?: string;
    host?: string;
    port?: string;
    database?: string;
    query?: string;
  }): Promise<DatabaseConfig> {
    return api.post('/database-configs/', config);
  },

  /**
   * Get API keys for the current user
   */
  async getApiKeys(): Promise<APIKey[]> {
    return api.get('/api-keys/');
  },

  /**
   * Create a new API key
   */
  async createApiKey(data: {
    name: string;
    database_config_id: string;
  }): Promise<APIKey> {
    return api.post('/api-keys/', data);
  }
}; 