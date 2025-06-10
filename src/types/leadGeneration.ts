export interface Lead {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  company: string;
  jobTitle: string;
  sourceId: string;
  campaignId: string;
  status: string;
  score: number;
  notes: string;
  createdAt: string;
  updatedAt: string;
}

export interface LeadSource {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
}

export interface LeadCampaign {
  id: string;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}
