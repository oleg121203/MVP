import { CRMClient } from '../api/crmClient';
import { LeadGenerationClient } from '../api/leadGenerationClient';
import { Lead, LeadSource, LeadCampaign } from '../types/leadGeneration';
import { CRMContact, CRMDeal, CRMTask } from '../types/crm';

/**
 * IntegrationService handles data synchronization between CRM, Lead Generation,
 * and existing VentAI systems.
 */
export class IntegrationService {
  private crmClient: CRMClient;
  private leadGenClient: LeadGenerationClient;

  constructor() {
    this.crmClient = new CRMClient();
    this.leadGenClient = new LeadGenerationClient();
  }

  /**
   * Syncs leads from Lead Generation to CRM as contacts and potential deals.
   */
  async syncLeadsToCRM(): Promise<void> {
    try {
      const leads = await LeadGenerationClient.getLeads();
      for (const lead of leads) {
        const contact: CRMContact = {
          id: lead.id,
          firstName: lead.firstName,
          lastName: lead.lastName,
          email: lead.email,
          phone: lead.phone || '',
          company: lead.company || '',
          jobTitle: lead.jobTitle || '',
          address: '', // Removed reference to non-existent property
          notes: `Imported from Lead Generation on ${new Date().toISOString()}`,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        await CRMClient.createContact(contact);

        if (lead.status === 'Qualified') {
          const deal: CRMDeal = {
            id: `deal-${lead.id}`,
            title: `${lead.firstName} ${lead.lastName} - Potential Deal`,
            contactId: lead.id,
            stage: 'Prospecting',
            value: 0,
            status: 'Open',
            description: `Potential deal from lead ${lead.firstName} ${lead.lastName}`,
            expectedCloseDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days from now
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          };
          await CRMClient.createDeal(deal);
        }
      }
      console.log('Leads successfully synced to CRM.');
    } catch (error) {
      console.error('Error syncing leads to CRM:', error);
      throw error;
    }
  }

  /**
   * Syncs lead sources and campaigns to CRM for reporting purposes.
   */
  async syncLeadSourcesAndCampaigns(): Promise<void> {
    try {
      const sources = await LeadGenerationClient.getLeadSources();
      const campaigns = await LeadGenerationClient.getLeadCampaigns();
      console.log(`Syncing ${sources.length} lead sources and ${campaigns.length} campaigns to CRM.`);
      // Implementation for syncing sources and campaigns can be expanded here
    } catch (error) {
      console.error('Error syncing lead sources and campaigns:', error);
      throw error;
    }
  }

  /**
   * Syncs CRM data to other VentAI systems (e.g., Price Intelligence, Supply Chain).
   */
  async syncCRMToVentAI(): Promise<void> {
    try {
      const contacts = await CRMClient.getContacts();
      const deals = await CRMClient.getDeals();
      console.log(`Syncing ${contacts.length} contacts and ${deals.length} deals to VentAI systems.`);
      // Implementation for syncing to other VentAI systems can be expanded here
    } catch (error) {
      console.error('Error syncing CRM data to VentAI systems:', error);
      throw error;
    }
  }
}

export const integrationService = new IntegrationService();
