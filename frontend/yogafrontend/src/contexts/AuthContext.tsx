import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiService from '../services/api';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; message: string; errors?: string[] }>;
  signup: (userData: SignupData) => Promise<{ success: boolean; message: string; errors?: string[] }>;
  logout: () => void;
}

interface SignupData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const userInfo = apiService.getUserInfo();
        if (userInfo && userInfo.exp > Date.now() / 1000) {
          // Token is still valid, set user info
          setUser(userInfo);
        } else {
          // Token expired or invalid, clear it
          apiService.logout();
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        apiService.logout();
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const response = await apiService.login({ email, password });
      
      if (response.success && response.user) {
        setUser(response.user);
        return { success: true, message: response.message };
      } else {
        return { 
          success: false, 
          message: response.message, 
          errors: response.errors || ['Login failed'] 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        message: 'Login failed', 
        errors: [error instanceof Error ? error.message : 'An error occurred'] 
      };
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (userData: SignupData) => {
    try {
      setIsLoading(true);
      const response = await apiService.signup(userData);
      
      if (response.success) {
        return { success: true, message: response.message };
      } else {
        return { 
          success: false, 
          message: response.message, 
          errors: response.errors || ['Signup failed'] 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        message: 'Signup failed', 
        errors: [error instanceof Error ? error.message : 'An error occurred'] 
      };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    apiService.logout();
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
