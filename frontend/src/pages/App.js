import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';

import DuctSizingCalculator from './DuctSizingCalculator';
import AirExchangeCalculator from './AirExchangeCalculator';
import SmokeRemovalCalculator from './SmokeRemovalCalculator';
import WaterHeaterCalculator from './WaterHeaterCalculator';
import DuctAreaCalculator from './DuctAreaCalculator';
import ProjectsPage from './pages/ProjectsPage';
import ProjectDetailPage from './pages/ProjectDetailPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AdminPage from './pages/AdminPage';
import MarketResearchPage from './pages/MarketResearchPage';
import DashboardPage from './pages/DashboardPage';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LocalizationProvider, useLocalization } from './context/LocalizationContext';
import { ToastProvider, useToast } from './context/ToastContext';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import ThemeToggle from './components/ThemeToggle';
import LanguageSwitcher from './components/LanguageSwitcher';
import ToastContainer from './components/ui/ToastContainer';
import ForgotPassword from './components/ForgotPassword';

import './App.css';

// Main page with calculators
const CalculatorsHomePage = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  return (
    <div className="calculators-home">
      <h2 className="text-2xl font-bold mb-6">{t('calculators.title')}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="calculator-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{t('calculators.airExchange')}</h3>
          <AirExchangeCalculator projects={projects} addSpecToProject={addSpecToProject} />
        </div>
        <div className="calculator-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{t('calculators.ductSizing')}</h3>
          <DuctSizingCalculator projects={projects} addSpecToProject={addSpecToProject} />
        </div>
        <div className="calculator-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{t('calculators.smokeRemoval')}</h3>
          <SmokeRemovalCalculator projects={projects} addSpecToProject={addSpecToProject} />
        </div>
        <div className="calculator-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{t('calculators.ductArea')}</h3>
          <DuctAreaCalculator projects={projects} addSpecToProject={addSpecToProject} />
        </div>
        <div className="calculator-card p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-2">{t('calculators.waterHeater')}</h3>
          <WaterHeaterCalculator projects={projects} addSpecToProject={addSpecToProject} />
        </div>
      </div>
    </div>
  );
};

// Navigation component with authentication state
const Navigation = () => {
  const { token, logout, user } = useAuth();
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [isDropdownOpen, setIsDropdownOpen] = React.useState(false);
  const dropdownRef = React.useRef(null);

  // Close dropdown when clicking outside
  React.useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    }

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  // Close dropdown when route changes
  React.useEffect(() => {
    setIsDropdownOpen(false);
  }, [window.location.pathname]);

  // Define styles based on theme with modernized look
  const headerStyle = {
    backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
    borderBottom: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
    padding: '1rem 1.5rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    position: 'sticky',
    top: 0,
    zIndex: 50
  };

  const logoStyle = {
    color: theme === 'dark' ? '#60a5fa' : '#2563eb',
    textDecoration: 'none',
    fontSize: '1.75rem',
    fontWeight: 'bold',
    margin: 0,
    display: 'flex',
    alignItems: 'center'
  };

  const navLinkStyle = {
    color: theme === 'dark' ? '#60a5fa' : '#2563eb',
    fontWeight: '500',
    padding: '0.5rem 1rem',
    marginLeft: '1.5rem',
    textDecoration: 'none',
    transition: 'color 0.2s, background-color 0.2s',
    borderRadius: '0.375rem',
    '&:hover': {
      backgroundColor: theme === 'dark' ? '#374151' : '#eff6ff'
    }
  };

  const navContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    flexWrap: 'wrap'
  };

  const controlsContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginLeft: '1.5rem'
  };

  return (
    <header style={headerStyle}>
      <Link to="/" style={logoStyle}>
        <h1>Vent.AI</h1>
      </Link>
      <div style={controlsContainerStyle}>
        <LanguageSwitcher />
        <ThemeToggle />
      </div>
      <nav style={navContainerStyle}>
        <NavLink to="/dashboard" style={navLinkStyle}>{t('nav.dashboard')}</NavLink>
        <NavLink to="/calculators" style={navLinkStyle}>{t('nav.calculators')}</NavLink>
        <NavLink to="/projects" style={navLinkStyle}>{t('nav.projects')}</NavLink>
        {token ? (
          <div style={{ position: 'relative', marginLeft: '1.5rem' }} ref={dropdownRef}>
            <button onClick={toggleDropdown} style={{ 
              color: theme === 'dark' ? '#60a5fa' : '#2563eb', 
              fontWeight: '500', 
              padding: '0.5rem 1rem',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center'
            }}>
              {user?.email || t('nav.account')}
            </button>
            {isDropdownOpen && (
              <div style={{
                position: 'absolute',
                top: '100%',
                right: 0,
                marginTop: '0.5rem',
                backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
                border: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
                borderRadius: '0.375rem',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                minWidth: '200px',
                zIndex: 100
              }}>
                <Link to="/market-research" style={{
                  display: 'block',
                  padding: '0.75rem 1.5rem',
                  color: theme === 'dark' ? '#f9fafb' : '#111827',
                  textDecoration: 'none',
                  '&:hover': {
                    backgroundColor: theme === 'dark' ? '#374151' : '#eff6ff'
                  }
                }}>{t('nav.marketResearch')}</Link>
                {user?.isAdmin && (
                  <Link to="/admin" style={{
                    display: 'block',
                    padding: '0.75rem 1.5rem',
                    color: theme === 'dark' ? '#f9fafb' : '#111827',
                    textDecoration: 'none',
                    '&:hover': {
                      backgroundColor: theme === 'dark' ? '#374151' : '#eff6ff'
                    }
                  }}>{t('nav.admin')}</Link>
                )}
                <button onClick={logout} style={{
                  display: 'block',
                  width: '100%',
                  textAlign: 'left',
                  padding: '0.75rem 1.5rem',
                  color: theme === 'dark' ? '#f87171' : '#dc2626',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  '&:hover': {
                    backgroundColor: theme === 'dark' ? '#374151' : '#eff6ff'
                  }
                }}>{t('nav.logout')}</button>
              </div>
            )}
          </div>
        ) : (
          <NavLink to="/login" style={navLinkStyle}>{t('nav.login')}</NavLink>
        )}
      </nav>
    </header>
  );
};

function AppContent() {
  const [projects, setProjects] = useState([]);
  const { token } = useAuth();
  const { theme } = useTheme();

  // Function to add specification to a project
  const addSpecToProject = (projectId, specString) => {
    setProjects(prevProjects => {
      const updatedProjects = prevProjects.map(project => {
        if (project.id === projectId) {
          const specs = project.specifications || [];
          return { ...project, specifications: [...specs, specString] };
        }
        return project;
      });
      return updatedProjects;
    });
  };

  const appContainerStyle = {
    minHeight: '100vh',
    backgroundColor: theme === 'dark' ? '#111827' : '#f9fafb',
    color: theme === 'dark' ? '#f9fafb' : '#111827',
  };

  const mainContentStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '1.5rem 1rem',
  };

  // Get the toast context
  const { toasts, removeToast } = useToast();

  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          await getProfile();
        }
      } catch (error) {
        console.log('Not authenticated');
      }
    };
    checkAuth();
  }, []);

  const getProfile = async () => {
    // Mock function, implement actual API call if needed
    console.log('Getting profile...');
  };

  return (
    <div style={appContainerStyle}>
      <ToastContainer toasts={toasts} position="top-right" onCloseToast={removeToast} />
      <Navigation />

      <main style={mainContentStyle}>
        <Routes>
          <Route
            path="/"
            element={
              token ? (
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              ) : (
                <CalculatorsHomePage projects={projects} addSpecToProject={addSpecToProject} />
              )
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/calculators"
            element={
              <CalculatorsHomePage projects={projects} addSpecToProject={addSpecToProject} />
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/projects"
            element={
              <ProtectedRoute>
                <ProjectsPage projects={projects} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:id"
            element={
              <ProtectedRoute>
                <ProjectDetailPage projects={projects} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              // Updated prop to adminOnly
              <ProtectedRoute adminOnly={true}>
                <AdminPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/market-research"
            element={
              <ProtectedRoute>
                <MarketResearchPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/calculators/water-heater"
            element={
              <ProtectedRoute>
                <WaterHeaterCalculator projects={projects} addSpecToProject={addSpecToProject} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/calculators/duct-area"
            element={
              <ProtectedRoute>
                <DuctAreaCalculator projects={projects} addSpecToProject={addSpecToProject} />
              </ProtectedRoute>
            }
          />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </main>

      <footer
        style={{
          marginTop: '3rem',
          padding: '1.5rem 0',
          textAlign: 'center',
          color: theme === 'dark' ? '#9ca3af' : '#4b5563',
          fontSize: '0.875rem',
          backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
          borderTop: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`
        }}
      >
        <p> 2025 Vent.AI. {t('footer.rights')}</p>
      </footer>
    </div>
  );
}

// Wrap AppContent with providers
export default function App() {
  return (
    <div className="App">
      <ThemeProvider>
        <LocalizationProvider>
          <AuthProvider>
            <ToastProvider position="top-right">
              <Router>
                <AppContent />
              </Router>
            </ToastProvider>
          </AuthProvider>
        </LocalizationProvider>
      </ThemeProvider>
    </div>
  );
}
