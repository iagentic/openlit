import { getSession } from 'next-auth/react';
import { Session } from 'next-auth';

// Extend the Session type
interface CustomSession extends Session {
  accessToken?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:9090';

// Function to get the auth token from the session
const getAuthToken = async () => {
  try {
    if (typeof window !== 'undefined') {
      const session = await getSession() as CustomSession;
      return session?.accessToken;
    }
    return null;
  } catch (error) {
    console.error('Error getting auth token:', error);
    return null;
  }
};

// Function to create headers with auth token
const createHeaders = async () => {
  try {
    const token = await getAuthToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  } catch (error) {
    console.error('Error creating headers:', error);
    return { 'Content-Type': 'application/json' };
  }
};

export const api = {
  async get(endpoint: string) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        headers,
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in GET request to ${endpoint}:`, error);
      throw error;
    }
  },

  async post(endpoint: string, data: any) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in POST request to ${endpoint}:`, error);
      throw error;
    }
  },

  async put(endpoint: string, data: any) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data),
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in PUT request to ${endpoint}:`, error);
      throw error;
    }
  },

  async delete(endpoint: string) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'DELETE',
        headers,
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in DELETE request to ${endpoint}:`, error);
      throw error;
    }
  },
  
  // Authentication methods
  async login(email: string, password: string) {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await fetch(`${API_URL}/token`, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error in login request:', error);
      throw error;
    }
  },
  
  logout() {
    // Token is handled by NextAuth
  },
  
  async isAuthenticated() {
    try {
      const session = await getSession();
      return !!session;
    } catch (error) {
      console.error('Error checking authentication status:', error);
      return false;
    }
  }
}; 