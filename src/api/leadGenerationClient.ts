import axios from 'axios';
import { Lead, LeadSource, LeadCampaign } from '../types/leadGeneration';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Lead Generation API Client
export class LeadGenerationClient {
  private static CACHE_DURATION_MS = 5 * 60 * 1000; // 5 minutes cache duration
  
  private static getCachedData<T>(key: string): T | null {
    const cached = localStorage.getItem(key);
    if (cached) {
      const { data, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp < this.CACHE_DURATION_MS) {
        return data;
      } else {
        localStorage.removeItem(key); // Remove expired cache
      }
    }
    return null;
  }
  
  private static setCachedData<T>(key: string, data: T): void {
    localStorage.setItem(key, JSON.stringify({ data, timestamp: Date.now() }));
  }

  static async getLeads(): Promise<Lead[]> {
    const cacheKey = 'leads';
    const cachedData = this.getCachedData<Lead[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/lead-generation/leads');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async getLead(id: string): Promise<Lead> {
    const cacheKey = `lead_${id}`;
    const cachedData = this.getCachedData<Lead>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get(`/lead-generation/leads/${id}`);
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async createLead(lead: Partial<Lead>): Promise<Lead> {
    const response = await apiClient.post('/lead-generation/leads', lead);
    // Clear cache for leads list since it has changed
    localStorage.removeItem('leads');
    return response.data;
  }

  static async updateLead(id: string, lead: Partial<Lead>): Promise<Lead> {
    const response = await apiClient.put(`/lead-generation/leads/${id}`, lead);
    // Clear cache for this lead and the list
    localStorage.removeItem(`lead_${id}`);
    localStorage.removeItem('leads');
    return response.data;
  }

  static async deleteLead(id: string): Promise<void> {
    await apiClient.delete(`/lead-generation/leads/${id}`);
    // Clear cache for this lead and the list
    localStorage.removeItem(`lead_${id}`);
    localStorage.removeItem('leads');
  }

  static async getLeadSources(): Promise<LeadSource[]> {
    const cacheKey = 'leadSources';
    const cachedData = this.getCachedData<LeadSource[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/lead-generation/sources');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async getLeadCampaigns(): Promise<LeadCampaign[]> {
    const cacheKey = 'leadCampaigns';
    const cachedData = this.getCachedData<LeadCampaign[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/lead-generation/campaigns');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async createLeadSource(source: Partial<LeadSource>): Promise<LeadSource> {
    const response = await apiClient.post('/lead-generation/sources', source);
    // Clear cache for lead sources
    localStorage.removeItem('leadSources');
    return response.data;
  }

  static async createLeadCampaign(campaign: Partial<LeadCampaign>): Promise<LeadCampaign> {
    const response = await apiClient.post('/lead-generation/campaigns', campaign);
    // Clear cache for lead campaigns
    localStorage.removeItem('leadCampaigns');
    return response.data;
  }
}

export default LeadGenerationClient;
