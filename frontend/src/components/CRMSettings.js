import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useToast } from '../context/ToastContext';
import './CRMSettings.css';

const CRMSettings = () => {
  const { t } = useTranslation();
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasStoredKey, setHasStoredKey] = useState(false);
  const { success, error, info } = useToast();

  const handleSaveApiKey = async () => {
    if (!apiKey.trim()) {
      error({
        title: t('settings.crm.apiKey.validationError'),
        message: t('settings.crm.apiKey.validationErrorMessage'),
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
          title: t('settings.crm.apiKey.saved'),
          message: t('settings.crm.apiKey.savedMessage'),
        });
        setApiKey('********'); // Show masked value instead of clearing
        setHasStoredKey(true);
      } else {
        const errorData = await response.json();
        error({
          title: t('settings.crm.apiKey.saveFailed'),
          message: errorData.detail || t('settings.crm.apiKey.saveFailedMessage'),
        });
      }
    } catch (err) {
      error({
        title: t('settings.crm.apiKey.networkError'),
        message: t('settings.crm.apiKey.networkErrorMessage'),
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
          title: t('settings.crm.testConnection.success'),
          message: t('settings.crm.testConnection.successMessage'),
        });
      } else {
        const errorData = await response.json();
        error({
          title: t('settings.crm.testConnection.error'),
          message: errorData.detail || t('settings.crm.testConnection.errorMessage'),
        });
      }
    } catch (err) {
      error({
        title: t('settings.crm.testConnection.networkError'),
        message: t('settings.crm.testConnection.networkErrorMessage'),
      });
      console.error('Failed to test connection:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="crm-settings">
      <div className="settings-header">
        <h2>{t('settings.crm.title')}</h2>
        <p className="settings-description">
          {t('settings.crm.description')}
        </p>
      </div>

      <div className="settings-section">
        <h3>{t('settings.crm.apiKey.label')}</h3>

        <div className="form-group">
          <label htmlFor="hubspot-api-key">
            {t('settings.crm.apiKey.label')}
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
            placeholder={hasStoredKey ? t('settings.crm.apiKey.storedPlaceholder') : t('settings.crm.apiKey.placeholder')}
            className={`api-key-input ${hasStoredKey ? 'has-stored-key' : ''}`}
          />
          <small className="help-text">
            {t('settings.crm.apiKey.helpText')}
            <a
              href="https://knowledge.hubspot.com/integrations/how-do-i-get-my-hubspot-api-key"
              target="_blank"
              rel="noopener noreferrer"
            >
              {t('settings.crm.apiKey.helpLink')}
            </a>
          </small>
        </div>

        <div className="button-group">
          <button onClick={handleSaveApiKey} disabled={isLoading} className="btn btn-primary">
            {isLoading ? t('settings.crm.apiKey.saving') : t('settings.crm.apiKey.save')}
          </button>

          <button
            onClick={handleTestConnection}
            disabled={isLoading || !apiKey}
            className="btn btn-secondary"
          >
            {isLoading ? t('settings.crm.testConnection.testing') : t('settings.crm.testConnection.button')}
          </button>
        </div>

        {/* Toast notifications will be shown via the Toast context */}
      </div>

      <div className="settings-section">
        <h3>{t('settings.crm.howItWorks.title')}</h3>
        <div className="info-cards">
          <div className="info-card">
            <h4>{t('settings.crm.howItWorks.secureStorage.title')}</h4>
            <p>
              {t('settings.crm.howItWorks.secureStorage.description')}
            </p>
          </div>

          <div className="info-card">
            <h4>{t('settings.crm.howItWorks.automaticDeals.title')}</h4>
            <p>
              {t('settings.crm.howItWorks.automaticDeals.description')}
            </p>
          </div>

          <div className="info-card">
            <h4>{t('settings.crm.howItWorks.dataSync.title')}</h4>
            <p>
              {t('settings.crm.howItWorks.dataSync.description')}
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>{t('settings.crm.nextSteps.title')}</h3>
        <ol className="steps-list">
          <li>{t('settings.crm.nextSteps.step1')}</li>
          <li>{t('settings.crm.nextSteps.step2')}</li>
          <li>{t('settings.crm.nextSteps.step3')}</li>
          <li>{t('settings.crm.nextSteps.step4')}</li>
        </ol>
      </div>
    </div>
  );
};

export default CRMSettings;
