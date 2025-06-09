import axios from 'axios';
import type { Supplier } from '../types/supplier';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

export const supplierClient = {
  async getSuppliers(): Promise<Supplier[]> {
    const response = await axios.get(`${API_URL}/api/suppliers`);
    return response.data;
  },

  async createSupplier(supplier: Omit<Supplier, 'id'>): Promise<Supplier> {
    const response = await axios.post(`${API_URL}/api/suppliers`, supplier);
    return response.data;
  },

  async updateSupplier(id: string, supplier: Partial<Supplier>): Promise<Supplier> {
    const response = await axios.patch(`${API_URL}/api/suppliers/${id}`, supplier);
    return response.data;
  },

  async deleteSupplier(id: string): Promise<void> {
    await axios.delete(`${API_URL}/api/suppliers/${id}`);
  },

  async getSupplierRatings(id: string): Promise<{rating: number}> {
    const response = await axios.get(`${API_URL}/api/suppliers/${id}/ratings`);
    return response.data;
  }
};
