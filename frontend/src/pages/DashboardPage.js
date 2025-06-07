import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Card, Button } from '../components/ui';
import './DashboardPage.css';

// Імпортуємо API_BASE_URL з apiService
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const DashboardPage = () => {
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const [recentProjects, setRecentProjects] = useState([]);
  const [stats, setStats] = useState({
    totalProjects: 0,
    totalDocuments: 0,
    totalProposals: 0,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(`${API_BASE_URL}/api/dashboard/summary`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      const data = await response.json();

      setRecentProjects(data.recentProjects || []);
      setStats({
        totalProjects: data.totalProjects || 0,
        totalDocuments: data.totalDocuments || 0,
        totalProposals: data.totalProposals || 0,
      });
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      toast.error('Failed to load dashboard data. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const navigateTo = (path) => {
    navigate(path);
  };

  return (
    <div className="dashboard-container">
      <h1>Welcome to Vent.AI Dashboard</h1>
      <p className="dashboard-subtitle">
        Your central hub for HVAC project management and market research
      </p>

      {/* Quick Access Widget */}
      <section className="dashboard-section">
        <h2>Quick Access</h2>
        <div className="quick-access-grid">
          <Card className="quick-access-card">
            <div className="quick-access-content">
              <h3>New Project</h3>
              <p>Create a new HVAC project from scratch</p>
              <Button
                variant="primary"
                onClick={() => navigateTo('/projects/new')}
                className="quick-access-button"
              >
                Create Project
              </Button>
            </div>
          </Card>

          <Card className="quick-access-card">
            <div className="quick-access-content">
              <h3>Market Research</h3>
              <p>Research prices for HVAC components</p>
              <Button
                variant="primary"
                onClick={() => navigateTo('/market-research')}
                className="quick-access-button"
              >
                Research Prices
              </Button>
            </div>
          </Card>

          <Card className="quick-access-card">
            <div className="quick-access-content">
              <h3>Engineering Tools</h3>
              <p>Access calculators and engineering tools</p>
              <Button
                variant="primary"
                onClick={() => navigateTo('/tools')}
                className="quick-access-button"
              >
                Open Tools
              </Button>
            </div>
          </Card>

          <Card className="quick-access-card">
            <div className="quick-access-content">
              <h3>All Projects</h3>
              <p>View and manage all your HVAC projects</p>
              <Button
                variant="primary"
                onClick={() => navigateTo('/projects')}
                className="quick-access-button"
              >
                View Projects
              </Button>
            </div>
          </Card>
        </div>
      </section>

      {/* Recent Projects Widget */}
      <section className="dashboard-section">
        <h2>Recent Projects</h2>
        <div className="recent-projects-grid">
          {isLoading ? (
            <p>Loading recent projects...</p>
          ) : recentProjects.length > 0 ? (
            recentProjects.map((project) => (
              <Card key={project.id} className="project-card">
                <div className="project-card-content">
                  <h3>{project.name}</h3>
                  <p className="project-description">{project.description}</p>
                  <div className="project-meta">
                    <span>Created: {new Date(project.created_at).toLocaleDateString()}</span>
                    <span className="project-status">{project.status}</span>
                  </div>
                  <Button
                    variant="secondary"
                    onClick={() => navigateTo(`/projects/${project.id}`)}
                    className="view-project-button"
                  >
                    View Details
                  </Button>
                </div>
              </Card>
            ))
          ) : (
            <p>No recent projects found. Create your first project to get started!</p>
          )}
        </div>
        {recentProjects.length > 0 && (
          <div className="view-all-container">
            <Button
              variant="text"
              onClick={() => navigateTo('/projects')}
              className="view-all-button"
            >
              View All Projects
            </Button>
          </div>
        )}
      </section>

      {/* Statistics Widget */}
      <section className="dashboard-section">
        <h2>Your Statistics</h2>
        <div className="stats-grid">
          <Card className="stat-card">
            <div className="stat-content">
              <h3>Total Projects</h3>
              <p className="stat-number">{stats.totalProjects}</p>
            </div>
          </Card>

          <Card className="stat-card">
            <div className="stat-content">
              <h3>Knowledge Base Documents</h3>
              <p className="stat-number">{stats.totalDocuments}</p>
            </div>
          </Card>

          <Card className="stat-card">
            <div className="stat-content">
              <h3>Generated Proposals</h3>
              <p className="stat-number">{stats.totalProposals}</p>
            </div>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
