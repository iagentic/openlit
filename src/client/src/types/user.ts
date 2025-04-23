export interface User {
  id: string;
  email: string;
  name?: string;
  image?: string;
  email_verified?: Date;
  password?: string;
  created_at: Date;
  updated_at: Date;
} 