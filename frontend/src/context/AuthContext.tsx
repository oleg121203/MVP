import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { apiClient } from '../api/client';

interface AuthContextType {
  isAuthenticated: boolean;
  user: { role?: string } | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{ role?: string } | null>(null);

  // Initialize with guest user for demo purposes
  useEffect(() => {
    // For demo, set a default user role so navigation works
    if (!user) {
      setUser({ role: 'user' });
    }
  }, []);

  const login = async (username: string, password: string) => {
    try {
      await apiClient.login(username, password);
      setIsAuthenticated(true);
      // TODO: Fetch user data from API and set it
      setUser({ role: 'user' }); // Temporary placeholder
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    apiClient.setToken('');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
