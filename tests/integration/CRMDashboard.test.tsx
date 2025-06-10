import React from 'react';
import { render, screen, act } from '@testing-library/react';
import CRMDashboard from '../../src/components/CRMDashboard';
import { CRMClient } from '../../src/api/crmClient';

// Mock the CRMClient to avoid actual API calls during testing
jest.mock('../../src/api/crmClient');

const mockGetContacts = jest.fn().mockResolvedValue([
  { id: '1', firstName: 'John', lastName: 'Doe', email: 'john.doe@example.com' },
  { id: '2', firstName: 'Jane', lastName: 'Smith', email: 'jane.smith@example.com' },
]);

const mockGetDeals = jest.fn().mockResolvedValue([
  { id: '1', title: 'Deal 1', value: 10000 },
  { id: '2', title: 'Deal 2', value: 25000 },
]);

const mockGetTasks = jest.fn().mockResolvedValue([
  { id: '1', title: 'Follow up', dueDate: '2025-06-15' },
  { id: '2', title: 'Send proposal', dueDate: '2025-06-12' },
]);

CRMClient.getContacts = mockGetContacts;
CRMClient.getDeals = mockGetDeals;
CRMClient.getTasks = mockGetTasks;

describe('CRMDashboard', () => {
  test('renders CRM dashboard with contacts, deals, and tasks', async () => {
    render(<CRMDashboard />);

    // Wait for loading to complete
    await screen.findByText(/Loading.../i, {}, { timeout: 5000 });
    await screen.findByText(/CRM Dashboard/i, {}, { timeout: 5000 });

    // Check if the dashboard title is rendered
    expect(screen.getByText(/CRM Dashboard/i)).toBeInTheDocument();

    // Check if contacts are rendered
    expect(await screen.findByText(/John Doe/i)).toBeInTheDocument();
    expect(await screen.findByText(/Jane Smith/i)).toBeInTheDocument();

    // Check if deals are rendered
    expect(await screen.findByText(/Deal 1/i)).toBeInTheDocument();
    expect(await screen.findByText(/Deal 2/i)).toBeInTheDocument();

    // Check if tasks are rendered
    expect(await screen.findByText(/Follow up/i)).toBeInTheDocument();
    expect(await screen.findByText(/Send proposal/i)).toBeInTheDocument();
  });
});
