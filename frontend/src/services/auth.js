import api from './api';

export const login = async (username, password) => {
  try {
    const { data } = await api.post('/auth/token/', { username, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  } catch (error) {
    console.error('Login error:', error.response?.data);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const getProfile = async () => {
  const { data } = await api.get('/profile/');
  return data;
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};
