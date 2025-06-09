import axios from 'axios';
import type { Competitor } from '../types/competitor';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

export const competitorClient = {
  async getCompetitors(): Promise<Competitor[]> {
    const response = await axios.get(`${API_URL}/api/competitors`);
    return response.data;
  },

  async analyzeCompetitorPrices(competitorId: string): Promise<{priceComparison: any}> {
    const response = await axios.get(`${API_URL}/api/competitors/${competitorId}/prices`);
    return response.data;
  }
};
