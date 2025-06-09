export interface Supplier {
  id: string;
  name: string;
  contactEmail: string;
  phoneNumber: string;
  materialsProvided: string[];
  reliabilityScore: number;
  deliveryTimeDays: number;
  priceCompetitiveness: number;
  lastUpdated: string;
}
