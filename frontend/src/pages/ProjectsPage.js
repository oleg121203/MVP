import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { useToast } from '../context/ToastContext';
import { useLocalization } from '../context/LocalizationContext';
import { Button, Modal, Form, FormGroup, Input, SearchBar } from '../components/ui';
import ProjectForm from '../components/ProjectForm';
import { createProject, updateProject, deleteProject } from '../services/apiService';

const ProjectsPage = ({ projects }) => {
  const { theme } = useTheme();
  const { t } = useLocalization();
  const { success, error, warning } = useToast();

  // State for project modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create' or 'edit'
  const [currentProject, setCurrentProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    client: '',
    status: 'planning', // Default status
  });
  const [formErrors, setFormErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // State for filtering and sorting
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('updatedAt');
  const [sortOrder, setSortOrder] = useState('desc');
  const [isSearching, setIsSearching] = useState(false);

  // Confirmation modal state
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState(null);

  // Filter and sort projects
  const filteredProjects = projects
    .filter((project) => {
      const matchesSearch =
        !searchQuery ||
        project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (project.description &&
          project.description.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (project.client && project.client.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchesStatus = statusFilter === 'all' || project.status === statusFilter;

      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      let comparison = 0;

      // Handle different sort fields
      if (sortBy === 'name') {
        comparison = a.name.localeCompare(b.name);
      } else if (sortBy === 'createdAt') {
        comparison = new Date(a.createdAt) - new Date(b.createdAt);
      } else if (sortBy === 'updatedAt') {
        comparison = new Date(a.updatedAt) - new Date(b.updatedAt);
      }

      // Apply sort order
      return sortOrder === 'asc' ? comparison : -comparison;
    });

  // Handle input changes for the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error for this field if it exists
    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  // Validate form data
  const validateForm = () => {
    const errors = {};

    if (!formData.name.trim()) {
      errors.name = t('Project name is required');
    }

    if (!formData.description.trim()) {
      errors.description = t('Project description is required');
    }

    return errors;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setIsSubmitting(true);

    try {
      if (modalMode === 'create') {
        // Create new project
        await createProject(formData);
        success(t('Project created successfully'));
      } else {
        // Update existing project
        await updateProject(currentProject.id, formData);
        success(t('Project updated successfully'));
      }

      // Close modal and reset form
      setIsModalOpen(false);
      resetForm();

      // Refresh projects list - in a real app, you would update the projects state
      // For now, we'll reload the page to get fresh data
      setTimeout(() => window.location.reload(), 500);
    } catch (err) {
      error(t('Error: ') + (err.message || t('Failed to save project')));
    } finally {
      setIsSubmitting(false);
    }
  };

  // Open modal for creating a new project
  const handleCreateProject = () => {
    setModalMode('create');
    resetForm();
    setIsModalOpen(true);
  };

  // Open modal for editing an existing project
  const handleEditProject = (project) => {
    setModalMode('edit');
    setCurrentProject(project);
    setFormData({
      name: project.name || '',
      description: project.description || '',
      client: project.client || '',
      status: project.status || 'planning',
    });
    setIsModalOpen(true);
  };

  // Handle project deletion
  const handleDeleteProject = (project) => {
    setProjectToDelete(project);
    setIsConfirmModalOpen(true);
  };

  // Confirm and execute project deletion
  const confirmDeleteProject = async () => {
    if (!projectToDelete) return;

    try {
      await deleteProject(projectToDelete.id);
      success(t('Project deleted successfully'));

      // Refresh projects list
      setTimeout(() => window.location.reload(), 500);
    } catch (err) {
      error(t('Error: ') + (err.message || t('Failed to delete project')));
    } finally {
      setIsConfirmModalOpen(false);
      setProjectToDelete(null);
    }
  };

  // Reset form data and errors
  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      client: '',
      status: 'planning',
    });
    setFormErrors({});
    setCurrentProject(null);
  };

  // Handle search
  const handleSearch = (query) => {
    setIsSearching(true);
    setSearchQuery(query);
    setTimeout(() => setIsSearching(false), 300);
  };

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return '';

    const date = new Date(dateString);
    return new Intl.DateTimeFormat('uk-UA', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  // Get status badge color based on status
  const getStatusColor = (status) => {
    switch (status) {
      case 'planning':
        return {
          bg: theme === 'dark' ? '#374151' : '#e5e7eb',
          text: theme === 'dark' ? '#f9fafb' : '#111827',
        };
      case 'in_progress':
        return { bg: theme === 'dark' ? '#1e40af' : '#3b82f6', text: '#ffffff' };
      case 'completed':
        return { bg: theme === 'dark' ? '#065f46' : '#10b981', text: '#ffffff' };
      case 'on_hold':
        return { bg: theme === 'dark' ? '#92400e' : '#f59e0b', text: '#ffffff' };
      default:
        return {
          bg: theme === 'dark' ? '#374151' : '#e5e7eb',
          text: theme === 'dark' ? '#f9fafb' : '#111827',
        };
    }
  };

  // Get status label
  const getStatusLabel = (status) => {
    switch (status) {
      case 'planning':
        return t('Planning');
      case 'in_progress':
        return t('In Progress');
      case 'completed':
        return t('Completed');
      case 'on_hold':
        return t('On Hold');
      default:
        return status;
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 md:p-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">
        {t('My Projects')}
      </h1>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <Button
          variant="primary"
          className="px-4 py-2 flex items-center gap-2"
          onClick={handleCreateProject}
        >
          <span className="text-lg">+</span> {t('Create New Project')}
        </Button>

        <div className="flex flex-col sm:flex-row items-stretch gap-4 w-full md:w-auto">
          <SearchBar
            placeholder={t('Search projects...')}
            onSearch={handleSearch}
            isLoading={isSearching}
            className="w-full sm:w-64"
            autoFocus={false}
          />

          <div className="flex items-center gap-2">
            <select
              className="p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              aria-label={t('Filter by status')}
            >
              <option value="all">{t('All Statuses')}</option>
              <option value="planning">{t('Planning')}</option>
              <option value="in_progress">{t('In Progress')}</option>
              <option value="completed">{t('Completed')}</option>
              <option value="on_hold">{t('On Hold')}</option>
            </select>

            <select
              className="p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              aria-label={t('Sort by')}
            >
              <option value="updatedAt">{t('Last Updated')}</option>
              <option value="createdAt">{t('Creation Date')}</option>
              <option value="name">{t('Name')}</option>
            </select>

            <button
              className="p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 w-10 flex justify-center"
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              aria-label={t('Toggle sort order')}
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.length === 0 ? (
          <div className="col-span-full text-center py-12 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">{t('No projects found.')}</p>
          </div>
        ) : (
          filteredProjects.map((project) => (
            <div
              key={project.id}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-shadow duration-300 flex flex-col"
            >
              <div className="p-5 border-b border-gray-200 dark:border-gray-700 flex justify-between items-start">
                <div className="flex-1">
                  <Link to={`/projects/${project.id}`} className="hover:underline">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                      {project.name}
                    </h3>
                  </Link>
                  <div
                    className="inline-block px-2 py-1 text-xs font-medium rounded-full"
                    style={{
                      backgroundColor: getStatusColor(project.status).bg,
                      color: getStatusColor(project.status).text,
                    }}
                  >
                    {getStatusLabel(project.status)}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    className="p-1.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    onClick={() => handleEditProject(project)}
                    aria-label={t('Edit project')}
                  >
                    ✏️
                  </button>
                  <button
                    className="p-1.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    onClick={() => handleDeleteProject(project)}
                    aria-label={t('Delete project')}
                  >
                    🗑️
                  </button>
                </div>
              </div>

              <div className="p-5 flex-1">
                <p className="text-gray-700 dark:text-gray-300 mb-4">{project.description}</p>
                {project.client && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <span className="font-medium">{t('Client')}:</span> {project.client}
                  </p>
                )}
              </div>

              <div className="p-5 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
                <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                  <div className="flex justify-between">
                    <span className="font-medium">{t('Created')}:</span>
                    <span>{formatDate(project.createdAt)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">{t('Updated')}:</span>
                    <span>{formatDate(project.updatedAt)}</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Project Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={modalMode === 'create' ? t('Create New Project') : t('Edit Project')}
      >
        <ProjectForm
          onSave={async (projectData) => {
            setIsSubmitting(true);
            try {
              if (modalMode === 'create') {
                // Create new project
                await createProject({
                  ...projectData,
                  client: '',
                  status: 'planning',
                });
                success(t('Project created successfully'));
              } else {
                // Update existing project
                await updateProject(currentProject.id, {
                  ...projectData,
                  client: currentProject.client || '',
                  status: currentProject.status || 'planning',
                });
                success(t('Project updated successfully'));
              }

              // Close modal and reset form
              setIsModalOpen(false);
              resetForm();

              // Refresh projects list
              setTimeout(() => window.location.reload(), 500);
            } catch (err) {
              error(t('Error: ') + (err.message || t('Failed to save project')));
            } finally {
              setIsSubmitting(false);
            }
          }}
          onCancel={() => {
            setIsModalOpen(false);
            resetForm();
          }}
          project={modalMode === 'edit' ? currentProject : null}
          isLoading={isSubmitting}
        />
      </Modal>

      {/* Confirmation Modal */}
      <Modal
        isOpen={isConfirmModalOpen}
        onClose={() => {
          setIsConfirmModalOpen(false);
          setProjectToDelete(null);
        }}
        title={t('Confirm Deletion')}
        size="small"
      >
        <div className="confirm-modal-content">
          <p>{t('Are you sure you want to delete this project?')}</p>
          <p className="warning-text">{t('This action cannot be undone.')}</p>

          <div className="form-actions">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsConfirmModalOpen(false);
                setProjectToDelete(null);
              }}
            >
              {t('Cancel')}
            </Button>
            <Button type="button" variant="danger" onClick={confirmDeleteProject}>
              {t('Delete')}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ProjectsPage;
