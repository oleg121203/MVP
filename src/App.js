import React from 'react';
import ProjectAnalyticsDashboard from './components/ProjectAnalyticsDashboard';

export default function App() {
  return (
    <div className="app">
      <ProjectAnalyticsDashboard 
        projectId="PROJ-001" 
        onRefresh={() => window.location.reload()}
      />
    </div>
  );
}
