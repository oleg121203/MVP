import { useAuth } from '../context/AuthContext';
import { LoginForm } from '../components/LoginForm';
import { ProjectList } from '../components/ProjectList';
import { AIGeneration } from '../components/AIGeneration';
import { ErrorNotifications } from '../components/ErrorNotifications';
import { LoadingIndicator } from '../components/LoadingIndicator';
import MainLayout from '../layouts/MainLayout';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import CalculatorsPage from '../pages/CalculatorsPage';
import DashboardPage from '../pages/DashboardPage';
import AIDashboard from '../pages/AIDashboard';
import ProjectsPage from '../pages/ProjectsPage';
import SettingsPage from '../pages/SettingsPage';
import ProjectManagementPage from '../pages/ProjectManagementPage';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <MainLayout>
            <HomePage />
          </MainLayout>
        } />
        <Route path="/calculators" element={
          <MainLayout>
            <CalculatorsPage />
          </MainLayout>
        } />
        <Route path="/dashboard" element={
          <MainLayout>
            <DashboardPage />
          </MainLayout>
        } />
        <Route path="/ai-dashboard" element={
          <MainLayout>
            <AIDashboard />
          </MainLayout>
        } />
        <Route path="/projects" element={
          <MainLayout>
            <ProjectsPage />
          </MainLayout>
        } />
        <Route path="/project-management" element={
          <MainLayout>
            <ProjectManagementPage />
          </MainLayout>
        } />
        <Route path="/ai-insights" element={
          <MainLayout>
            <div>AI Insights Page (Placeholder)</div>
          </MainLayout>
        } />
        <Route path="/settings" element={
          <MainLayout>
            <SettingsPage />
          </MainLayout>
        } />
        <Route path="/automation" element={
          <MainLayout>
            <div>Automation Page (Placeholder)</div>
          </MainLayout>
        } />
        <Route path="*" element={
          <MainLayout>
            <LoadingIndicator />
            <ErrorNotifications />
            {isAuthenticated ? (
              <div className="max-w-4xl mx-auto space-y-8">
                <ProjectList />
                <AIGeneration />
              </div>
            ) : (
              <LoginForm />
            )}
          </MainLayout>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
