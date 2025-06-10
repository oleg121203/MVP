import React from 'react';
import { Layout } from 'antd';
import AnalyticsDashboard from '../components/analytics/AnalyticsDashboard';

export default function AnalyticsPage() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Layout.Content style={{ padding: '24px' }}>
        <h1>VentAI Analytics Dashboard</h1>
        <AnalyticsDashboard />
      </Layout.Content>
    </Layout>
  );
}
