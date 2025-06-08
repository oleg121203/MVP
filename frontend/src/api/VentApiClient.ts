import axios from 'axios';

class VentApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  }

  async request(method: string, endpoint: string, data: any = null, headers: any = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await axios({
        method,
        url,
        data,
        headers,
      });
      return response;
    } catch (error) {
      throw error;
    }
  }
}

export default VentApiClient;
