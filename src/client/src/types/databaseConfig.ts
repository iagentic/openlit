export interface DatabaseConfig {
  id: string;
  name: string;
  environment: string;
  username: string;
  password?: string;
  host: string;
  port: string;
  database: string;
  query?: string;
  created_at: Date;
  updated_at: Date;
  user_id: string;
}

export interface APIKey {
  id: string;
  name: string;
  api_key: string;
  database_config_id: string;
  is_deleted: boolean;
  created_at: Date;
  created_by_user_id: string;
  deleted_at?: Date;
  deleted_by_user_id?: string;
} 