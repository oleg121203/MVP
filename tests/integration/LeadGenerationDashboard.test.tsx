import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import LeadGenerationDashboard from '../../src/components/LeadGenerationDashboard';
import { LeadGenerationClient } from '../../src/api/leadGenerationClient';

// Mock the LeadGenerationClient to avoid actual API calls during testing
jest.mock('../../src/api/leadGenerationClient');

// Use fake timers to control setTimeout
jest.useFakeTimers();

const mockGetLeads = jest.fn().mockResolvedValue([
  { id: '1', firstName: 'John', lastName: 'Doe', email: 'john.doe@example.com' },
  { id: '2', firstName: 'Jane', lastName: 'Smith', email: 'jane.smith@example.com' },
]);

const mockGetLeadSources = jest.fn().mockResolvedValue([
  { id: '1', name: 'Website', description: 'Company Website' },
  { id: '2', name: 'Referral', description: 'Referral Program' },
]);

const mockGetLeadCampaigns = jest.fn().mockResolvedValue([
  { id: '1', name: 'Summer Campaign', status: 'Active' },
  { id: '2', name: 'Winter Campaign', status: 'Completed' },
]);

LeadGenerationClient.getLeads = mockGetLeads;
LeadGenerationClient.getLeadSources = mockGetLeadSources;
LeadGenerationClient.getLeadCampaigns = mockGetLeadCampaigns;

describe('LeadGenerationDashboard', () => {
  test('renders Lead Generation dashboard with leads, sources, and campaigns', async () => {
    render(<LeadGenerationDashboard />);

    // Wait for loading to appear and then disappear
    await screen.findByText(/Loading.../i, {}, { timeout: 10000 });
    await screen.findByText(/Lead Generation Dashboard/i, {}, { timeout: 10000 });
    
    // Advance timers to simulate setTimeout completion
    jest.advanceTimersByTime(5000);

    // Use waitFor with a custom query to ensure data is rendered
    await waitFor(() => {
      expect(screen.getAllByText(/John Doe/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Jane Smith/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Website/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Referral/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Summer Campaign/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Winter Campaign/i).length).toBeGreaterThan(0);
    }, { timeout: 15000 });
  }, 60000); // Keep the overall test timeout at 60 seconds
});
