import axios from 'axios';

type PriceRecommendation = {
  suggestedPrice: number;
  strategy: 'premium' | 'competitive' | 'penetration';
  rationale: string;
};

type PriceTrend = {
  trend: 'upward' | 'downward' | 'stable';
  confidence: number;
  predictedPrice: number;
};

const API_BASE = process.env.REACT_APP_API_URL || '/api';

export const PriceClient = {
  getRecommendation: async (projectId: string): Promise<PriceRecommendation> => {
    const { data } = await axios.get(`${API_BASE}/price/${projectId}/recommendation`);
    return data;
  },
  
  getTrends: async (projectId: string): Promise<PriceTrend> => {
    const { data } = await axios.get(`${API_BASE}/price/${projectId}/trends`);
    return data;
  },
  
  refreshMarketData: async (projectId: string): Promise<void> => {
    await axios.post(`${API_BASE}/price/${projectId}/refresh`);
  }
};
