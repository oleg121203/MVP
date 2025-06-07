import React, { useState, useEffect } from 'react';
import { useLocalization } from '../context/LocalizationContext';
import { useTheme } from '../context/ThemeContext';
import AutomationPanel from '../components/AutomationPanel';

// Mock data for AI insights
const mockInsights = [
  { id: 1, title: 'Project Cost Optimization', description: 'AI suggests reducing material costs by 15% through alternative supplier selection based on current market data.', status: 'Active' },
  { id: 2, title: 'Compliance Check', description: 'All project parameters comply with Ukrainian legislation (ДБН В.2.5-67:2013).', status: 'Completed' },
  { id: 3, title: 'Procurement Automation', description: 'Automated procurement process initiated for 3 projects, optimizing for location and delivery time.', status: 'In Progress' },
  { id: 4, title: 'Energy Efficiency Analysis', description: 'AI recommends adjusting HVAC parameters for 20% energy savings.', status: 'Active' }
];

const mockProjects = [
  { id: 101, name: 'Residential Complex Ventilation', status: 'In Progress', compliance: 'Compliant', costSavings: '12%' },
  { id: 102, name: 'Industrial Plant HVAC', status: 'Under Review', compliance: 'Issues Detected', costSavings: '8%' },
  { id: 103, name: 'Office Building Redesign', status: 'Completed', compliance: 'Compliant', costSavings: '15%' }
];

const AIDashboard = () => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [insights, setInsights] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setInsights(mockInsights);
      setProjects(mockProjects);
      setLoading(false);
    }, 1000);
  }, []);

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

  const subTitleStyle = {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
    color: theme === 'dark' ? '#f9fafb' : '#111827'
  };

  const textStyle = {
    color: theme === 'dark' ? '#d1d5db' : '#4b5563'
  };

  const statusBadgeStyle = (status) => ({
    display: 'inline-block',
    padding: '0.25rem 0.5rem',
    borderRadius: '0.25rem',
    fontSize: '0.75rem',
    marginLeft: '0.5rem',
    backgroundColor: status === 'Active' ? '#dcfce7' : status === 'In Progress' ? '#fff7ed' : '#f3f4f6',
    color: status === 'Active' ? '#16a34a' : status === 'In Progress' ? '#f59e0b' : '#1f2937'
  });

  const complianceBadgeStyle = (compliance) => ({
    display: 'inline-block',
    padding: '0.25rem 0.5rem',
    borderRadius: '0.25rem',
    fontSize: '0.75rem',
    backgroundColor: compliance === 'Compliant' ? '#dcfce7' : '#fee2e2',
    color: compliance === 'Compliant' ? '#16a34a' : '#dc2626'
  });

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem', ...textStyle }}>
        {t('dashboard.loading')}
      </div>
    );
  }

  return (
    <div>
      <h1 style={titleStyle}>{t('dashboard.title')}</h1>
      <p style={textStyle}>{t('dashboard.description')}</p>

      <AutomationPanel />

      <h2 style={subTitleStyle}>{t('dashboard.insights')}</h2>
      <div style={{ marginBottom: '2rem' }}>
        {insights.map(insight => (
          <div key={insight.id} style={cardStyle}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem', color: theme === 'dark' ? '#f9fafb' : '#111827' }}>
              {insight.title}
              <span style={statusBadgeStyle(insight.status)}>{insight.status}</span>
            </h3>
            <p style={textStyle}>{insight.description}</p>
          </div>
        ))}
      </div>

      <h2 style={subTitleStyle}>{t('dashboard.recentProjects')}</h2>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', ...cardStyle }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left', padding: '0.75rem', borderBottom: `2px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`, color: theme === 'dark' ? '#f9fafb' : '#111827', fontWeight: '600' }}>{t('dashboard.projectName')}</th>
              <th style={{ textAlign: 'left', padding: '0.75rem', borderBottom: `2px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`, color: theme === 'dark' ? '#f9fafb' : '#111827', fontWeight: '600' }}>{t('dashboard.status')}</th>
              <th style={{ textAlign: 'left', padding: '0.75rem', borderBottom: `2px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`, color: theme === 'dark' ? '#f9fafb' : '#111827', fontWeight: '600' }}>{t('dashboard.compliance')}</th>
              <th style={{ textAlign: 'left', padding: '0.75rem', borderBottom: `2px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`, color: theme === 'dark' ? '#f9fafb' : '#111827', fontWeight: '600' }}>{t('dashboard.costSavings')}</th>
            </tr>
          </thead>
          <tbody>
            {projects.map(project => (
              <tr key={project.id} style={{ borderBottom: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}` }}>
                <td style={{ padding: '0.75rem', ...textStyle }}>{project.name}</td>
                <td style={{ padding: '0.75rem', ...textStyle }}>{project.status}</td>
                <td style={{ padding: '0.75rem', ...textStyle }}><span style={complianceBadgeStyle(project.compliance)}>{project.compliance}</span></td>
                <td style={{ padding: '0.75rem', ...textStyle }}>{project.costSavings}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AIDashboard;
