import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/auth";
import { headers } from "next/headers";
import { Session } from "next-auth";

// Extend the Session type to include accessToken
interface CustomSession extends Session {
  accessToken?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:9090';

// Function to get the auth token from the server session
const getAuthToken = async () => {
  try {
    const session = await getServerSession(authOptions) as CustomSession;
    return session?.accessToken;
  } catch (error) {
    console.error("Error getting auth token:", error);
    return null;
  }
};

// Function to create headers with auth token
const createHeaders = async () => {
  const token = await getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
};

export const serverApi = {
  async get(endpoint: string) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        headers,
        cache: 'no-store',
      });
      
      if (!response.ok) {
        // Log the error but don't throw for 401/403 errors
        if (response.status === 401 || response.status === 403) {
          console.warn(`Authentication error: ${response.status}`);
          return null;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in GET request to ${endpoint}:`, error);
      return null;
    }
  },

  async post(endpoint: string, data: any) {
    try {
      const headers = await createHeaders();
      
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
        cache: 'no-store',
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
        cache: 'no-store',
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
        cache: 'no-store',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error(`Error in DELETE request to ${endpoint}:`, error);
      throw error;
    }
  }
}; 