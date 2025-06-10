import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface CRMLead {
  id: number;
  name: string;
  email: string;
  status: string;
  created_at: string;
}

const CrmDashboard: React.FC = () => {
  const [leads, setLeads] = useState<CRMLead[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const response = await axios.get<CRMLead[]>('http://localhost:8001/crm/leads/');
        setLeads(response.data);
      } catch (err) {
        setError('Failed to fetch leads.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchLeads();
  }, []);

  if (loading) return <div>Loading CRM Leads...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="crm-dashboard">
      <h2>All CRM Leads</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td>{lead.id}</td>
              <td>{lead.name}</td>
              <td>{lead.email}</td>
              <td>{lead.status}</td>
              <td>{new Date(lead.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CrmDashboard;
