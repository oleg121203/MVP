// Auto-generated price API client
import axios from 'axios';

export interface PriceItem {
  id: string;
  name: string;
  price: number;
  currency: string;
  trend: 'up' | 'down' | 'stable';
  change: number;
  supplier: string;
  lastUpdated: string;
}

export interface PriceData {
  prices: PriceItem[];
  lastUpdated: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

export const priceClient = {
  getCurrentPrices: async (): Promise<PriceData> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/prices`);
      return response.data;
    } catch (error) {
      console.error('Error fetching price data:', error);
      throw new Error('Failed to fetch price data');
    }
  },

  getPriceHistory: async (itemId: string): Promise<PriceItem[]> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/prices/${itemId}/history`);
      return response.data;
    } catch (error) {
      console.error('Error fetching price history:', error);
      throw new Error('Failed to fetch price history');
    }
  }
};

// Legacy function for backward compatibility
export const getPriceData = priceClient.getCurrentPrices;

export default priceClient;