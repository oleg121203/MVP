import axios from 'axios';
import { FASTAPI_BASE_URL, TOKEN_REFRESH_ENDPOINT } from './apiConfig';

const api = axios.create({
  baseURL: FASTAPI_BASE_URL,
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
        const { data } = await axios.post(`${FASTAPI_BASE_URL}${TOKEN_REFRESH_ENDPOINT}`, { refresh });
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
