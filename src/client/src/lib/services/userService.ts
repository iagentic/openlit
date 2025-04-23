import { api } from '../api';
import { User } from '../../types/user';

export const userService = {
  /**
   * Get the current user's profile
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      return await api.get('/users/me/');
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  },

  /**
   * Create a new user
   */
  async createUser(email: string, password: string): Promise<User> {
    try {
      return await api.post('/users/', { email, password });
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  },

  /**
   * Update the current user's profile
   */
  async updateUserProfile(data: {
    current_password?: string;
    new_password?: string;
    name?: string;
  }): Promise<User> {
    try {
      return await api.put('/users/me/', data);
    } catch (error) {
      console.error('Error updating user profile:', error);
      throw error;
    }
  },

  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<{ access_token: string; token_type: string }> {
    try {
      return await api.login(email, password);
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  /**
   * Logout the current user
   */
  logout(): void {
    try {
      api.logout();
    } catch (error) {
      console.error('Error logging out:', error);
    }
  },

  /**
   * Check if the user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      return await api.isAuthenticated();
    } catch (error) {
      console.error('Error checking authentication status:', error);
      return false;
    }
  }
}; 