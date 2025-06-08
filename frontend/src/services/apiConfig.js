// Centralized API Configuration

// Base URLs for different backend services
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const FASTAPI_BASE_PATH = process.env.REACT_APP_FASTAPI_PATH || '/api';
const DJANGO_BASE_PATH = process.env.REACT_APP_DJANGO_PATH || '/api';

// Constructed full base URLs
export const FASTAPI_BASE_URL = `${API_BASE_URL}${FASTAPI_BASE_PATH}`;
export const DJANGO_BASE_URL = `${API_BASE_URL}${DJANGO_BASE_PATH}`;

// Endpoint paths
export const LOGIN_ENDPOINT = '/token';
export const TOKEN_REFRESH_ENDPOINT = '/token/refresh/';
export const AI_CHAT_ENDPOINT = '/ai/chat';
export const AI_DASHBOARD_ENDPOINT = '/dashboard';

// Additional configurations can be added here as needed
