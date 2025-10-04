// API service for communicating with the backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface SignupData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  user?: User;
  access_token?: string;
  token_type?: string;
  errors?: string[];
  data?: T;
}

class ApiService {
  private baseURL: string;
  private token: string | null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('auth_token');
  }

  // Set the auth token
  setToken(token: string | null): void {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  // Get the auth token
  getToken(): string | null {
    return this.token || localStorage.getItem('auth_token');
  }

  // Make HTTP requests with auth headers
  async request<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getToken();

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication methods
  async signup(userData: SignupData): Promise<ApiResponse> {
    return this.request<ApiResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: LoginCredentials): Promise<ApiResponse> {
    const response = await this.request<ApiResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    // Store the token if login is successful
    if (response.success && response.access_token) {
      this.setToken(response.access_token);
    }

    return response;
  }

  async logout(): Promise<void> {
    this.setToken(null);
    // You could also call a logout endpoint here if needed
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Get user info from token (you might want to decode JWT on frontend)
  getUserInfo(): User & { exp: number } | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      // Decode JWT payload (basic decoding, not verification)
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        id: payload.user_id,
        email: payload.email,
        first_name: payload.first_name,
        last_name: payload.last_name,
        created_at: payload.created_at || '',
        exp: payload.exp,
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  }

  // Flow generation methods
  async generateFlow(flowData: any): Promise<any> {
    return this.request('/flow/generate', {
      method: 'POST',
      body: JSON.stringify(flowData),
    });
  }

  async testFlowEndpoint(): Promise<any> {
    return this.request('/flow/test', {
      method: 'GET',
    });
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;
