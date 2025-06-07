import React, { createContext, useState, useContext, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
// Import our new API service functions
import {
  loginUser as apiLoginUser,
  registerUser as apiRegisterUser,
  getCurrentUser as apiGetCurrentUser,
} from '../services/apiService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('vent-ai-token'));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Fetch user data if token exists
    const fetchUser = async () => {
      if (token) {
        setLoading(true);
        try {
          const userData = await apiGetCurrentUser(); // Using our API service
          setUser(userData);
        } catch (error) {
          console.error('Error fetching user data:', error);
          logout(); // Token is invalid or expired
        } finally {
          setLoading(false);
        }
      } else {
        setUser(null);
      }
    };

    fetchUser();
  }, [token]);

  useEffect(() => {
    const storedToken = localStorage.getItem('vent-ai-token');
    if (storedToken) {
      try {
        const decodedUser = jwtDecode(storedToken);
        setUser(decodedUser); // Store the decoded user object
        setToken(storedToken);
      } catch (error) {
        console.error('Failed to decode token:', error);
        localStorage.removeItem('vent-ai-token'); // Clear invalid token
        setToken(null);
        setUser(null);
      }
    } else {
      setUser(null); // Ensure user is null if no token
    }
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);

    try {
      const data = await apiLoginUser(email, password); // Using our API service
      console.log('LOGIN RESPONSE:', data);
      localStorage.setItem('vent-ai-token', data.access_token);
      setToken(data.access_token);

      const decodedUser = jwtDecode(data.access_token);
      setUser(decodedUser);
      console.log('TOKEN SET IN LOCALSTORAGE:', localStorage.getItem('vent-ai-token'));

      return true;
    } catch (error) {
      setError(error.message);
      console.log('LOGIN ERROR:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, email, password) => {
    setLoading(true);
    setError(null);

    try {
      const regData = await apiRegisterUser(username, email, password); // Using our API service
      console.log('REGISTER RESPONSE:', regData);
      // Automatically log in after successful registration
      const loginResult = await login(email, password);
      return loginResult;
    } catch (error) {
      // Покращуємо відображення помилки
      let errorMessage = 'Registration failed';

      if (error.message) {
        errorMessage = error.message;
      }

      // Встановлюємо зрозумілий текст помилки
      setError(errorMessage);
      console.log('REGISTER ERROR:', error);
      console.log('REGISTER ERROR MESSAGE:', error.message);
      console.log('REGISTER ERROR RESPONSE:', error.response?.data);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('vent-ai-token');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = () => {
    return !!token;
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        logout,
        register,
        isAuthenticated,
        loading,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
