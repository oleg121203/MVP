import axios from 'axios';
import { CRMContact, CRMDeal, CRMTask } from '../types/crm';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// CRM API Client
export class CRMClient {
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

  static async getContacts(): Promise<CRMContact[]> {
    const cacheKey = 'crmContacts';
    const cachedData = this.getCachedData<CRMContact[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/crm/contacts');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async getContact(id: string): Promise<CRMContact> {
    const cacheKey = `crmContact_${id}`;
    const cachedData = this.getCachedData<CRMContact>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get(`/crm/contacts/${id}`);
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async createContact(contact: Partial<CRMContact>): Promise<CRMContact> {
    const response = await apiClient.post('/crm/contacts', contact);
    // Clear cache for contacts list since it has changed
    localStorage.removeItem('crmContacts');
    return response.data;
  }

  static async updateContact(id: string, contact: Partial<CRMContact>): Promise<CRMContact> {
    const response = await apiClient.put(`/crm/contacts/${id}`, contact);
    // Clear cache for this contact and the list
    localStorage.removeItem(`crmContact_${id}`);
    localStorage.removeItem('crmContacts');
    return response.data;
  }

  static async deleteContact(id: string): Promise<void> {
    await apiClient.delete(`/crm/contacts/${id}`);
    // Clear cache for this contact and the list
    localStorage.removeItem(`crmContact_${id}`);
    localStorage.removeItem('crmContacts');
  }

  static async getDeals(): Promise<CRMDeal[]> {
    const cacheKey = 'crmDeals';
    const cachedData = this.getCachedData<CRMDeal[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/crm/deals');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async getDeal(id: string): Promise<CRMDeal> {
    const cacheKey = `crmDeal_${id}`;
    const cachedData = this.getCachedData<CRMDeal>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get(`/crm/deals/${id}`);
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async createDeal(deal: Partial<CRMDeal>): Promise<CRMDeal> {
    const response = await apiClient.post('/crm/deals', deal);
    // Clear cache for deals list since it has changed
    localStorage.removeItem('crmDeals');
    return response.data;
  }

  static async updateDeal(id: string, deal: Partial<CRMDeal>): Promise<CRMDeal> {
    const response = await apiClient.put(`/crm/deals/${id}`, deal);
    // Clear cache for this deal and the list
    localStorage.removeItem(`crmDeal_${id}`);
    localStorage.removeItem('crmDeals');
    return response.data;
  }

  static async deleteDeal(id: string): Promise<void> {
    await apiClient.delete(`/crm/deals/${id}`);
    // Clear cache for this deal and the list
    localStorage.removeItem(`crmDeal_${id}`);
    localStorage.removeItem('crmDeals');
  }

  static async getTasks(): Promise<CRMTask[]> {
    const cacheKey = 'crmTasks';
    const cachedData = this.getCachedData<CRMTask[]>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get('/crm/tasks');
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async getTask(id: string): Promise<CRMTask> {
    const cacheKey = `crmTask_${id}`;
    const cachedData = this.getCachedData<CRMTask>(cacheKey);
    if (cachedData) {
      return cachedData;
    }
    
    const response = await apiClient.get(`/crm/tasks/${id}`);
    this.setCachedData(cacheKey, response.data);
    return response.data;
  }

  static async createTask(task: Partial<CRMTask>): Promise<CRMTask> {
    const response = await apiClient.post('/crm/tasks', task);
    // Clear cache for tasks list since it has changed
    localStorage.removeItem('crmTasks');
    return response.data;
  }

  static async updateTask(id: string, task: Partial<CRMTask>): Promise<CRMTask> {
    const response = await apiClient.put(`/crm/tasks/${id}`, task);
    // Clear cache for this task and the list
    localStorage.removeItem(`crmTask_${id}`);
    localStorage.removeItem('crmTasks');
    return response.data;
  }

  static async deleteTask(id: string): Promise<void> {
    await apiClient.delete(`/crm/tasks/${id}`);
    // Clear cache for this task and the list
    localStorage.removeItem(`crmTask_${id}`);
    localStorage.removeItem('crmTasks');
  }
}

export default CRMClient;
