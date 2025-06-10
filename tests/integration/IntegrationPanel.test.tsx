import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import IntegrationPanel from '../../src/components/IntegrationPanel';
import { integrationService } from '../../src/services/integrationService';

// Mock the integrationService to avoid actual API calls during testing
jest.mock('../../src/services/integrationService', () => {
  return {
    integrationService: {
      syncLeadsToCRM: jest.fn().mockResolvedValue(undefined),
      syncLeadSourcesAndCampaigns: jest.fn().mockResolvedValue(undefined),
      syncCRMToVentAI: jest.fn().mockResolvedValue(undefined),
    }
  };
});

describe('IntegrationPanel', () => {
  test('renders integration panel with synchronization buttons', () => {
    render(<IntegrationPanel />);
    expect(screen.getByText(/Integration Panel/i)).toBeInTheDocument();
    expect(screen.getByText(/Data Synchronization Controls/i)).toBeInTheDocument();
    expect(screen.getByText(/Sync Leads to CRM/i)).toBeInTheDocument();
    expect(screen.getByText(/Sync Sources & Campaigns/i)).toBeInTheDocument();
    expect(screen.getByText(/Sync CRM to VentAI/i)).toBeInTheDocument();
  });

  test('handles Sync Leads to CRM button click', async () => {
    render(<IntegrationPanel />);
    fireEvent.click(screen.getByText(/Sync Leads to CRM/i));
    await waitFor(() => expect(screen.getByText(/Leads successfully synced to CRM./i)).toBeInTheDocument());
    expect(integrationService.syncLeadsToCRM).toHaveBeenCalled();
  });

  test('handles Sync Sources & Campaigns button click', async () => {
    render(<IntegrationPanel />);
    fireEvent.click(screen.getByText(/Sync Sources & Campaigns/i));
    await waitFor(() => expect(screen.getByText(/Lead sources and campaigns successfully synced./i)).toBeInTheDocument());
    expect(integrationService.syncLeadSourcesAndCampaigns).toHaveBeenCalled();
  });

  test('handles Sync CRM to VentAI button click', async () => {
    render(<IntegrationPanel />);
    fireEvent.click(screen.getByText(/Sync CRM to VentAI/i));
    await waitFor(() => expect(screen.getByText(/CRM data successfully synced to VentAI systems./i)).toBeInTheDocument());
    expect(integrationService.syncCRMToVentAI).toHaveBeenCalled();
  });
}, 30000); // Set overall test timeout to 30 seconds
