import axios from 'axios';
import { API_BASE_URL } from './apiConfig';

// Create an Axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Змінюємо на false для уникнення CORS помилок
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('vent-ai-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const { status, data } = error.response;
      let errorMessage = data?.detail || `Server error: ${status}`;

      if (status === 401 || status === 403) {
        // Handle unauthorized/forbidden access
        console.error('Authentication error:', errorMessage);
        // Optionally redirect to login or refresh token
      } else if (status === 404) {
        errorMessage = data?.detail || 'Resource not found.';
      } else if (status === 400) {
        errorMessage = data?.detail || 'Bad request. Please check your input.';
      } else if (status >= 500) {
        errorMessage = 'Server error. Please try again later.';
      }

      return Promise.reject({
        status,
        message: errorMessage,
        data: data || {},
        originalError: error,
      });
    } else if (error.request) {
      // The request was made but no response was received
      return Promise.reject({
        status: 0,
        message: 'Network error: No response from server. Please check your connection.',
        originalError: error,
      });
    } else {
      // Something happened in setting up the request
      return Promise.reject({
        status: -1,
        message: error.message || 'An unexpected error occurred.',
        originalError: error,
      });
    }
  }
);

// --- Authentication Services ---
export const loginUser = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await axios.post(`${API_BASE_URL}/token`, formData.toString(), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    withCredentials: false,
  });
  return response.data;
};

export const registerUser = async (username, email, password) => {
  const requestData = { username, email, password };
  console.log('REGISTER REQUEST DATA:', requestData);
  const response = await api.post('/users/', requestData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/users/me/');
  return response.data;
};

// --- Project Services ---
export const getProjects = async (skip = 0, limit = 100) => {
  const response = await api.get(`/projects/?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const getProjectDetails = async (projectId) => {
  const response = await api.get(`/projects/${projectId}`);
  return response.data;
};

export const createProject = async (projectData) => {
  const response = await api.post('/projects/', projectData);
  return response.data;
};

export const updateProject = async (projectId, projectData) => {
  const response = await api.put(`/projects/${projectId}`, projectData);
  return response.data;
};

export const deleteProject = async (projectId) => {
  const response = await api.delete(`/projects/${projectId}`);
  return response.data;
};

// --- Market Research Services ---
export const researchMarketPrices = async (componentName) => {
  const response = await api.post('/api/market-prices/research', { component_name: componentName });
  return response.data;
};

export const getMarketResearchHistory = async (skip = 0, limit = 20) => {
  const response = await api.get(`/api/market-prices/history?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const getMarketResearchQueryDetails = async (queryId) => {
  const response = await api.get(`/api/market-prices/${queryId}`);
  return response.data;
};

export const getMarketPricesForQuery = async (queryId, skip = 0, limit = 10) => {
  const response = await api.get(
    `/api/market-prices/${queryId}/prices?skip=${skip}&limit=${limit}`
  );
  return response.data;
};

// --- CRM Services ---
export const updateCRMSettings = async (apiKey) => {
  const response = await api.put('/api/users/me/settings', { crm_api_key: apiKey });
  return response.data;
};

export const createCRMDealFromProject = async (projectId) => {
  const response = await api.post(`/api/project/${projectId}/create-crm-deal`);
  return response.data;
};

// --- Specification Services ---
export const createSpecification = async (projectId, specData) => {
  const response = await api.post(`/projects/${projectId}/specifications/`, specData);
  return response.data;
};

export const getSpecificationsByProject = async (projectId, skip = 0, limit = 100) => {
  const response = await api.get(
    `/projects/${projectId}/specifications/?skip=${skip}&limit=${limit}`
  );
  return response.data;
};

export const getSpecificationDetails = async (specId) => {
  const response = await api.get(`/specifications/${specId}`);
  return response.data;
};

export const updateSpecification = async (specId, specData) => {
  const response = await api.put(`/specifications/${specId}`, specData);
  return response.data;
};

export const deleteSpecification = async (specId) => {
  const response = await api.delete(`/specifications/${specId}`);
  return response.data;
};

export const searchSpecifications = async (projectId, queryText, topK = 5) => {
  const response = await api.post(`/projects/${projectId}/specifications/search`, {
    query_text: queryText,
    top_k: topK,
  });
  return response.data;
};

// --- AI Document Analysis Services ---
export const analyzeDocument = async (formData) => {
  const response = await api.post('/api/project/analyze-document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const refineAnalysis = async (sessionId, answers) => {
  const response = await api.post('/api/project/refine-analysis', {
    session_id: sessionId,
    answers: answers,
  });
  return response.data;
};

// --- Project Chat Services ---
export const postProjectChatMessage = async (projectId, question, history) => {
  const response = await api.post(`/api/project/${projectId}/chat`, {
    question,
    history,
  });
  return response.data;
};

// --- Compliance and Optimization Services ---
export const runComplianceCheckForProject = async (projectId) => {
  const response = await api.post(`/api/project/${projectId}/run-compliance-check`);
  return response.data;
};

export const runOptimizationAnalysisForProject = async (projectId) => {
  const response = await api.post(`/api/project/${projectId}/run-optimization`);
  return response.data;
};

// --- Commercial Proposal Services ---
export const generateCommercialProposalForProject = async (projectId) => {
  const response = await api.get(`/api/project/${projectId}/proposal`, {
    responseType: 'blob',
  });
  return response.data;
};
