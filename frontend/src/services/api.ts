import axios from 'axios';
import { AuthResponse } from '../types/api';

// Base URLs for backend services
const FASTAPI_BASE_URL = 'http://localhost:5000/api/ai';
const DJANGO_BASE_URL = 'http://localhost:8000/api';

// FastAPI client for AI services
export const fastApiClient = axios.create({
  baseURL: FASTAPI_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Django client for authentication and core services
export const djangoApiClient = axios.create({
  baseURL: DJANGO_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to set Authorization token for Django API client
export const setAuthToken = (token: string) => {
  djangoApiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

// Function to remove Authorization token
export const removeAuthToken = () => {
  delete djangoApiClient.defaults.headers.common['Authorization'];
};

// Example API call functions
export const getAIDashboardData = async () => {
  const response = await fastApiClient.get('/dashboard');
  return response.data;
};

export const loginUser = async (credentials: { username: string; password: string }): Promise<AuthResponse> => {
  const response = await djangoApiClient.post('/auth/login/', credentials);
  return response.data as AuthResponse;
};
