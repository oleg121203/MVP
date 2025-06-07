import React, { useState, useEffect } from 'react';
import { useToast } from '../context/ToastContext';
import './CRMSettings.css';

const CRMSettings = () => {
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasStoredKey, setHasStoredKey] = useState(false);
  const { success, error, info } = useToast();

  const handleSaveApiKey = async () => {
    if (!apiKey.trim()) {
      error({
        title: 'Validation Error',
        message: 'Please enter a valid API key',
      });
      return;
    }

    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/users/me/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          crm_api_key: apiKey,
        }),
      });

      if (response.ok) {
        success({
          title: 'API Key Saved',
          message: 'HubSpot API key saved successfully and encrypted securely',
        });
        setApiKey('********'); // Show masked value instead of clearing
        setHasStoredKey(true);
      } else {
        const errorData = await response.json();
        error({
          title: 'Save Failed',
          message: errorData.detail || 'Failed to save API key',
        });
      }
    } catch (err) {
      error({
        title: 'Network Error',
        message: 'Could not save API key. Please check your connection.',
      });
      console.error('Failed to save API key:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestConnection = async () => {
    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      // This would be a test endpoint to verify HubSpot connection
      const response = await fetch('/api/crm/test-connection', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        success({
          title: 'Connection Successful',
          message: 'HubSpot connection test successful',
        });
      } else {
        const errorData = await response.json();
        error({
          title: 'Connection Failed',
          message: errorData.detail || 'HubSpot connection test failed',
        });
      }
    } catch (err) {
      error({
        title: 'Connection Error',
        message: 'Could not test connection. Please check your network.',
      });
      console.error('Failed to test connection:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="crm-settings">
      <div className="settings-header">
        <h2>CRM Integration Settings</h2>
        <p className="settings-description">
          Configure your HubSpot integration to automatically create deals from your projects.
        </p>
      </div>

      <div className="settings-section">
        <h3>HubSpot Configuration</h3>

        <div className="form-group">
          <label htmlFor="hubspot-api-key">
            HubSpot API Key
            <span className="required">*</span>
          </label>
          <input
            id="hubspot-api-key"
            type="password"
            value={apiKey}
            onChange={(e) => {
              setApiKey(e.target.value);
              // If user starts typing, we're no longer showing a masked stored key
              if (hasStoredKey && e.target.value !== '********') {
                setHasStoredKey(false);
              }
            }}
            placeholder={hasStoredKey ? 'API key is stored securely' : 'Enter your HubSpot API key'}
            className={`api-key-input ${hasStoredKey ? 'has-stored-key' : ''}`}
          />
          <small className="help-text">
            Your API key will be encrypted and stored securely.
            <a
              href="https://knowledge.hubspot.com/integrations/how-do-i-get-my-hubspot-api-key"
              target="_blank"
              rel="noopener noreferrer"
            >
              How to get your HubSpot API key
            </a>
          </small>
        </div>

        <div className="button-group">
          <button onClick={handleSaveApiKey} disabled={isLoading} className="btn btn-primary">
            {isLoading ? 'Saving...' : 'Save API Key'}
          </button>

          <button
            onClick={handleTestConnection}
            disabled={isLoading || !apiKey}
            className="btn btn-secondary"
          >
            {isLoading ? 'Testing...' : 'Test Connection'}
          </button>
        </div>

        {/* Toast notifications will be shown via the Toast context */}
      </div>

      <div className="settings-section">
        <h3>How It Works</h3>
        <div className="info-cards">
          <div className="info-card">
            <h4>🔐 Secure Storage</h4>
            <p>
              Your API key is encrypted using AES-256 encryption before being stored in our
              database.
            </p>
          </div>

          <div className="info-card">
            <h4>🎯 Automatic Deals</h4>
            <p>Create HubSpot deals directly from your Vent.AI projects with calculated amounts.</p>
          </div>

          <div className="info-card">
            <h4>📊 Data Sync</h4>
            <p>
              Project specifications and commercial proposals are automatically included in deal
              data.
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>Next Steps</h3>
        <ol className="steps-list">
          <li>Save your HubSpot API key above</li>
          <li>Create or open a project in Vent.AI</li>
          <li>Generate commercial proposals and specifications</li>
          <li>Use the "Create CRM Deal" button in your project to sync data to HubSpot</li>
        </ol>
      </div>
    </div>
  );
};

export default CRMSettings;
