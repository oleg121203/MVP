// Auto-generated API client for VentAI

declare const process: {
  env: {
    REACT_APP_API_URL?: string;
  };
};

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface ApiConfig {
  headers?: Record<string, string>;
  noAuth?: boolean;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

export interface GetProjectsResponse {
  projects: Project[];
}

export interface ApiError {
  message: string;
  code?: number;
}

export interface AITaskResponse {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  result?: string;
  error?: string;
}

export class VentApiClient {
  private token: string | null = null;
  private loading: boolean = false;

  setToken(token: string) {
    this.token = token;
  }

  setLoading(loading: boolean) {
    this.loading = loading;
  }

  async request<T, D = unknown>(
    method: string,
    endpoint: string,
    data?: D,
    config: ApiConfig = {}
  ): Promise<T> {
    if (this.loading) {
      throw new Error('API client is currently loading');
    }

    this.setLoading(true);

    const url = `${API_BASE_URL}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(this.token && !config.noAuth ? { Authorization: `Bearer ${this.token}` } : {}),
      ...(config.headers || {})
    };

    const response = await fetch(url, {
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });

    this.setLoading(false);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Request failed');
    }

    return response.json();
  }

  // Auth methods
  async register(username: string, email: string, password: string) {
    return this.request(
      'POST',
      '/api/auth/register',
      { username, email, password },
      { noAuth: true }
    );
  }

  async login(username: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/api/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    const data = await response.json();
    this.setToken(data.access);
    return data;
  }

  // Project methods
  async createProject(name: string, description: string) {
    return this.request('POST', '/api/projects/', { name, description });
  }

  async getProjects<T = GetProjectsResponse>(): Promise<T> {
    return this.request<T>('GET', '/api/projects/');
  }

  // AI methods
  async generateContent<T = unknown>(data: { prompt: string }): Promise<T> {
    return this.request<T>('POST', '/api/ai/generate', data);
  }

  async getTaskStatus<T = AITaskResponse>(taskId: string): Promise<T> {
    return this.request<T>('GET', `/api/ai/tasks/${taskId}`);
  }
}

export const apiClient = new VentApiClient();
