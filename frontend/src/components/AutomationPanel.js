import React, { useState } from 'react';
import { useLocalization } from '../context/LocalizationContext';
import { useTheme } from '../context/ThemeContext';

const AutomationPanel = () => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [automationStatus, setAutomationStatus] = useState({
    projectAnalysis: false,
    complianceCheck: false,
    costOptimization: false,
    procurement: false
  });

  const toggleAutomation = (key) => {
    setAutomationStatus(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const cardStyle = {
    backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
    border: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
    borderRadius: '0.5rem',
    padding: '1.5rem',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    marginBottom: '1.5rem'
  };

  const titleStyle = {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginBottom: '1.5rem',
    color: theme === 'dark' ? '#f9fafb' : '#111827'
  };

  const textStyle = {
    color: theme === 'dark' ? '#d1d5db' : '#4b5563'
  };

  const buttonStyle = (isActive) => ({
    backgroundColor: isActive ? '#2563eb' : theme === 'dark' ? '#374151' : '#e5e7eb',
    color: isActive ? '#ffffff' : theme === 'dark' ? '#f9fafb' : '#111827',
    padding: '0.5rem 1rem',
    border: 'none',
    borderRadius: '0.375rem',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  });

  return (
    <div style={cardStyle}>
      <h2 style={titleStyle}>{t('dashboard.automationPanel')}</h2>
      <p style={textStyle}>{t('dashboard.automationDescription')}</p>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
        <div style={cardStyle}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem', color: theme === 'dark' ? '#f9fafb' : '#111827' }}>{t('dashboard.projectAnalysis')}</h3>
          <p style={textStyle}>{t('dashboard.projectAnalysisDesc')}</p>
          <button style={buttonStyle(automationStatus.projectAnalysis)} onClick={() => toggleAutomation('projectAnalysis')}>
            {automationStatus.projectAnalysis ? t('dashboard.enabled') : t('dashboard.disabled')}
          </button>
        </div>
        <div style={cardStyle}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem', color: theme === 'dark' ? '#f9fafb' : '#111827' }}>{t('dashboard.complianceCheck')}</h3>
          <p style={textStyle}>{t('dashboard.complianceCheckDesc')}</p>
          <button style={buttonStyle(automationStatus.complianceCheck)} onClick={() => toggleAutomation('complianceCheck')}>
            {automationStatus.complianceCheck ? t('dashboard.enabled') : t('dashboard.disabled')}
          </button>
        </div>
        <div style={cardStyle}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem', color: theme === 'dark' ? '#f9fafb' : '#111827' }}>{t('dashboard.costOptimization')}</h3>
          <p style={textStyle}>{t('dashboard.costOptimizationDesc')}</p>
          <button style={buttonStyle(automationStatus.costOptimization)} onClick={() => toggleAutomation('costOptimization')}>
            {automationStatus.costOptimization ? t('dashboard.enabled') : t('dashboard.disabled')}
          </button>
        </div>
        <div style={cardStyle}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem', color: theme === 'dark' ? '#f9fafb' : '#111827' }}>{t('dashboard.procurementAutomation')}</h3>
          <p style={textStyle}>{t('dashboard.procurementAutomationDesc')}</p>
          <button style={buttonStyle(automationStatus.procurement)} onClick={() => toggleAutomation('procurement')}>
            {automationStatus.procurement ? t('dashboard.enabled') : t('dashboard.disabled')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AutomationPanel;
