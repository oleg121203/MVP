export interface CRMContact {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  company: string;
  jobTitle: string;
  address: string;
  notes: string;
  createdAt: string;
  updatedAt: string;
}

export interface CRMDeal {
  id: string;
  title: string;
  description: string;
  value: number;
  stage: string;
  contactId: string;
  expectedCloseDate: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}

export interface CRMTask {
  id: string;
  title: string;
  description: string;
  dueDate: string;
  status: string;
  contactId: string;
  dealId: string;
  createdAt: string;
  updatedAt: string;
}
