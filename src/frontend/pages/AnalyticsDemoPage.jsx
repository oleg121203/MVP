import React from 'react';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import '../styles/analytics.css';

export default function AnalyticsDemoPage() {
  return (
    <div className="app-container">
      <header>
        <h1>VentAI Analytics Dashboard Demo</h1>
      </header>
      <main>
        <AnalyticsDashboard projectId={1} />
      </main>
    </div>
  );
}
