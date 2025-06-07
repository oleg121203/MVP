import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      try {
        const refresh = localStorage.getItem('refresh_token');
        const { data } = await axios.post(`${API_BASE}/token/refresh/`, { refresh });
        localStorage.setItem('access_token', data.access);
        error.config.headers.Authorization = `Bearer ${data.access}`;
        return axios(error.config);
      } catch (e) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
