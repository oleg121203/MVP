import axios from 'axios';
import { AuthResponse } from '../types/api';
import { FASTAPI_BASE_URL, DJANGO_BASE_URL, LOGIN_ENDPOINT, AI_DASHBOARD_ENDPOINT } from './apiConfig';

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
  const response = await fastApiClient.get(AI_DASHBOARD_ENDPOINT);
  return response.data;
};

export const loginUser = async (credentials: { username: string; password: string }): Promise<AuthResponse> => {
  const response = await djangoApiClient.post(LOGIN_ENDPOINT, credentials);
  return response.data as AuthResponse;
};
