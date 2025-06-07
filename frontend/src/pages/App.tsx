import { useAuth } from './context/AuthContext';
import { LoginForm } from './components/LoginForm';
import { ProjectList } from './components/ProjectList';
import { AIGeneration } from './components/AIGeneration';
import { ErrorNotifications } from './components/ErrorNotifications';
import { LoadingIndicator } from './components/LoadingIndicator';
import MainLayout from './layouts/MainLayout';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CalculatorsPage from './pages/CalculatorsPage';
import DashboardPage from './pages/DashboardPage';

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
