import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import CalculatorsPage from './pages/CalculatorsPage';
import DashboardPage from './pages/DashboardPage';
import AIDashboard from './pages/AIDashboard';
import AnalyticsPage from './pages/AnalyticsPage';
import AnalyticsDashboard from './components/AnalyticsDashboard';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path="calculators" element={<CalculatorsPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="ai-dashboard" element={<AIDashboard />} />
            <Route path="projects" element={<div>Projects Page (Placeholder)</div>} />
            <Route path="project-management" element={<div>Project Management Page (Placeholder)</div>} />
            <Route path="ai-insights" element={<div>AI Insights Page (Placeholder)</div>} />
            <Route path="settings" element={<div>Settings Page (Placeholder)</div>} />
            <Route path="automation" element={<div>Automation Page (Placeholder)</div>} />
            <Route path="analytics-dashboard" element={<AnalyticsDashboard projectId="sample-project-id" />} />
          </Route>
          <Route path="/analytics/:projectId" element={<AnalyticsPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
