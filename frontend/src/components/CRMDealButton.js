import React, { useState } from 'react';
import './CRMDealButton.css';

const CRMDealButton = ({ projectId, projectName }) => {
  const [isCreating, setIsCreating] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const createCRMDeal = async () => {
    setIsCreating(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/project/${projectId}/create-crm-deal`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ HubSpot deal created successfully! Deal ID: ${data.deal_id}`);
        setMessageType('success');
      } else {
        setMessage(`❌ ${data.detail || 'Failed to create deal'}`);
        setMessageType('error');
      }
    } catch (error) {
      setMessage('❌ Network error: Could not create deal');
      setMessageType('error');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="crm-deal-section">
      <div className="crm-header">
        <h3>🤝 CRM Integration</h3>
        <p>Create a deal in HubSpot based on this project's data and specifications</p>
      </div>

      <button
        onClick={createCRMDeal}
        disabled={isCreating}
        className={`crm-deal-btn ${isCreating ? 'loading' : ''}`}
      >
        {isCreating ? (
          <>
            <span className="spinner"></span>
            Creating Deal...
          </>
        ) : (
          <>📊 Create HubSpot Deal</>
        )}
      </button>

      {message && <div className={`crm-message ${messageType}`}>{message}</div>}

      <div className="crm-info">
        <h4>What gets included:</h4>
        <ul>
          <li>Project name and description</li>
          <li>Technical specifications</li>
          <li>Calculated project amount from market research</li>
          <li>Commercial proposal data</li>
        </ul>

        <p className="note">
          <strong>Note:</strong> Make sure you have configured your HubSpot API key in settings
          before creating deals.
        </p>
      </div>
    </div>
  );
};

export default CRMDealButton;
