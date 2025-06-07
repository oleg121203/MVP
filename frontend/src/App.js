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
const CalculatorsHomePage = ({ projects, addSpecToProject }) => (
  <>
    <AirExchangeCalculator projects={projects} addSpecToProject={addSpecToProject} />
    <DuctSizingCalculator projects={projects} addSpecToProject={addSpecToProject} />
    <SmokeRemovalCalculator projects={projects} addSpecToProject={addSpecToProject} />
    <DuctAreaCalculator projects={projects} addSpecToProject={addSpecToProject} />
  </>
);

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

    // Add event listener when dropdown is open
    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    // Cleanup
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

  // Define styles based on theme
  const headerStyle = {
    backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
    borderBottom: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
    padding: '1rem 1.5rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  };

  const logoStyle = {
    color: theme === 'dark' ? '#60a5fa' : '#2563eb',
    textDecoration: 'none',
  };

  const navLinkStyle = {
    color: theme === 'dark' ? '#60a5fa' : '#2563eb',
    fontWeight: '500',
    padding: '0.25rem 0.5rem',
    marginLeft: '1rem',
    textDecoration: 'none',
    transition: 'color 0.2s',
  };

  const navContainerStyle = {
    display: 'flex',
    alignItems: 'center',
  };

  const controlsContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
  };

  return (
    <header style={headerStyle}>
      <Link to="/" style={logoStyle}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>Vent.AI</h1>
      </Link>
      <div style={controlsContainerStyle}>
        <LanguageSwitcher />
        <ThemeToggle />
      </div>
      <nav style={navContainerStyle}>
        <NavLink to="/dashboard" style={navLinkStyle}>
          Dashboard
        </NavLink>
        <NavLink to="/market-research" style={navLinkStyle}>
          {t('navigation.market_research')}
        </NavLink>
        {user && user.is_admin && (
          <NavLink to="/admin" style={navLinkStyle}>
            {t('navigation.admin')}
          </NavLink>
        )}
        <div style={{ position: 'relative', display: 'inline-block' }} ref={dropdownRef}>
          <button
            onClick={toggleDropdown}
            style={{
              ...navLinkStyle,
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontFamily: 'inherit',
              fontSize: '1rem',
              padding: '0.25rem 0.5rem',
              marginLeft: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.25rem',
              color: theme === 'dark' ? '#60a5fa' : '#2563eb',
              ':hover': {
                color: theme === 'dark' ? '#93c5fd' : '#3b82f6',
              },
            }}
            aria-expanded={isDropdownOpen}
            aria-haspopup="true"
          >
            {t('navigation.calculators')} ▼
          </button>
          <div
            style={{
              position: 'absolute',
              backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
              minWidth: '220px',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              borderRadius: '0.5rem',
              zIndex: 50,
              padding: '0.5rem 0',
              border: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
              opacity: isDropdownOpen ? 1 : 0,
              transform: isDropdownOpen ? 'translateY(0)' : 'translateY(-10px)',
              visibility: isDropdownOpen ? 'visible' : 'hidden',
              transition: 'all 0.2s ease-in-out',
              pointerEvents: isDropdownOpen ? 'auto' : 'none',
            }}
            className="dropdown-menu"
            role="menu"
            aria-orientation="vertical"
            aria-labelledby="calculators-menu"
          >
            <div
              style={{
                padding: '0.5rem 1rem',
                color: theme === 'dark' ? '#9ca3af' : '#6b7280',
                fontSize: '0.875rem',
                fontWeight: '600',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                marginBottom: '0.25rem',
              }}
            >
              {t('navigation.calculators')}
            </div>
            <NavLink
              to="/calculators"
              style={({ isActive }) => ({
                display: 'block',
                margin: '0',
                padding: '0.5rem 1.5rem',
                color: isActive
                  ? theme === 'dark'
                    ? '#60a5fa'
                    : '#2563eb'
                  : theme === 'dark'
                    ? '#e5e7eb'
                    : '#1f2937',
                textDecoration: 'none',
                transition: 'all 0.2s',
                backgroundColor: isActive
                  ? theme === 'dark'
                    ? 'rgba(96, 165, 250, 0.1)'
                    : 'rgba(37, 99, 235, 0.1)'
                  : 'transparent',
                borderLeft: isActive
                  ? `3px solid ${theme === 'dark' ? '#60a5fa' : '#2563eb'}`
                  : '3px solid transparent',
                paddingLeft: isActive ? '1.75rem' : '1.5rem',
                ':hover': {
                  backgroundColor:
                    theme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.02)',
                  paddingLeft: '1.75rem',
                },
              })}
            >
              {t('navigation.all_calculators')}
            </NavLink>
            <NavLink
              to="/calculators/duct-area"
              style={({ isActive }) => ({
                display: 'block',
                margin: '0',
                padding: '0.5rem 1.5rem',
                color: isActive
                  ? theme === 'dark'
                    ? '#60a5fa'
                    : '#2563eb'
                  : theme === 'dark'
                    ? '#e5e7eb'
                    : '#1f2937',
                textDecoration: 'none',
                transition: 'all 0.2s',
                backgroundColor: isActive
                  ? theme === 'dark'
                    ? 'rgba(96, 165, 250, 0.1)'
                    : 'rgba(37, 99, 235, 0.1)'
                  : 'transparent',
                borderLeft: isActive
                  ? `3px solid ${theme === 'dark' ? '#60a5fa' : '#2563eb'}`
                  : '3px solid transparent',
                paddingLeft: isActive ? '1.75rem' : '1.5rem',
                ':hover': {
                  backgroundColor:
                    theme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.02)',
                  paddingLeft: '1.75rem',
                },
              })}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '24px',
                    height: '24px',
                    borderRadius: '6px',
                    backgroundColor:
                      theme === 'dark' ? 'rgba(96, 165, 250, 0.1)' : 'rgba(37, 99, 235, 0.1)',
                    color: theme === 'dark' ? '#60a5fa' : '#2563eb',
                    fontSize: '0.75rem',
                    fontWeight: '600',
                  }}
                >
                  DF
                </span>
                <span>Duct Area & Fittings</span>
              </div>
            </NavLink>
          </div>
        </div>
        <NavLink to="/projects" style={navLinkStyle}>
          {t('navigation.projects')}
        </NavLink>
        <NavLink to="/market-research" style={navLinkStyle}>
          Монітор цін / Price Monitor
        </NavLink>
        {token && user ? (
          <>
            {user.role === 'admin' && (
              <NavLink to="/admin" style={navLinkStyle}>
                {t('navigation.admin')}
              </NavLink>
            )}
            <span
              style={{ color: theme === 'dark' ? '#d1d5db' : '#4b5563', marginRight: '0.75rem' }}
            >
              Вітаю, {user.sub}! ({user.role})
            </span>
            <button
              onClick={logout}
              style={{
                backgroundColor: '#ef4444',
                color: 'white',
                padding: '0.5rem 0.75rem',
                borderRadius: '0.375rem',
                border: 'none',
                cursor: 'pointer',
                transition: 'background-color 0.2s',
              }}
            >
              {t('navigation.logout')}
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login" style={navLinkStyle}>
              {t('navigation.login')}
            </NavLink>
            <NavLink to="/register" style={navLinkStyle}>
              Реєстрація / Register
            </NavLink>
          </>
        )}
      </nav>
    </header>
  );
};

function AppContent() {
  const { token } = useAuth();
  const { theme } = useTheme();

  // Temporarily store project state here. Later this will be a database.
  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'Office Center "Class A"',
      description: 'Ventilation system for a 5-story building.',
    },
    {
      id: 2,
      name: 'Private house, Sokilnyky village',
      description: 'Supply and exhaust ventilation with recuperation.',
    },
  ]);

  const addSpecToProject = (projectId, specString) => {
    setProjects(
      projects.map((project) => {
        if (project.id === projectId) {
          return {
            ...project,
            specifications: [...(project.specifications || []), { content: specString }],
          };
        }
        return project;
      })
    );
  };

  // App container styles based on theme
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
        }}
      >
        <p> 2025 Vent.AI. Усі права захищені / All rights reserved.</p>
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
