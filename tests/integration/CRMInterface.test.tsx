import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import CRMInterface from '../../src/components/CRMInterface';
import { CRMClient } from '../../src/api/crmClient';

// Mock the CRMClient to avoid actual API calls during testing
jest.mock('../../src/api/crmClient', () => {
  return {
    CRMClient: {
      getContacts: jest.fn().mockResolvedValue([
        { id: '1', firstName: 'John', lastName: 'Doe', email: 'john.doe@example.com', phone: '123-456-7890', company: '', jobTitle: '', address: '', notes: '', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
        { id: '2', firstName: 'Jane', lastName: 'Smith', email: 'jane.smith@example.com', phone: '987-654-3210', company: '', jobTitle: '', address: '', notes: '', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
      ]),
      getDeals: jest.fn().mockResolvedValue([
        { id: 'deal-1', title: 'John Doe - Potential Deal', contactId: '1', stage: 'Prospecting', value: 5000, status: 'Open', description: 'Potential deal', expectedCloseDate: '2025-07-10T00:00:00Z', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
        { id: 'deal-2', title: 'Jane Smith - Potential Deal', contactId: '2', stage: 'Negotiation', value: 10000, status: 'Open', description: 'Potential deal', expectedCloseDate: '2025-07-10T00:00:00Z', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
      ]),
      getTasks: jest.fn().mockResolvedValue([
        { id: 'task-1', subject: 'Follow up with John', dueDate: '2025-06-15T00:00:00Z', status: 'Not Started', contactId: '1', description: 'Follow up call', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
        { id: 'task-2', subject: 'Send proposal to Jane', dueDate: '2025-06-12T00:00:00Z', status: 'In Progress', contactId: '2', description: 'Send initial proposal', createdAt: '2025-06-10T00:00:00Z', updatedAt: '2025-06-10T00:00:00Z' },
      ]),
    }
  };
});

// Use fake timers to control setTimeout
jest.useFakeTimers();

describe('CRMInterface', () => {
  test('renders CRM interface with tabs for contacts, deals, and tasks', async () => {
    render(<CRMInterface />);

    // Wait for loading to appear and then disappear
    await screen.findByText(/Loading.../i, {}, { timeout: 10000 });
    await screen.findByText(/CRM Interface/i, {}, { timeout: 10000 });
    
    // Advance timers to simulate setTimeout completion
    jest.advanceTimersByTime(5000);

    // Check if the tabs are rendered
    expect(screen.getByText(/Contacts/i)).toBeInTheDocument();
    expect(screen.getByText(/Deals/i)).toBeInTheDocument();
    expect(screen.getByText(/Tasks/i)).toBeInTheDocument();

    // Check if contacts are rendered by default (first tab)
    await waitFor(() => {
      expect(screen.getAllByText(/John Doe/i).length).toBeGreaterThan(0);
      expect(screen.getAllByText(/Jane Smith/i).length).toBeGreaterThan(0);
    }, { timeout: 10000 });
  }, 30000); // Set overall test timeout to 30 seconds
});
