export interface SupplyChainItem {
  id: string;
  name: string;
  supplierId: string;
  origin: string;
  leadTime: number;
  cost: number;
  sustainabilityScore: number;
  criticality: 'low' | 'medium' | 'high';
}
