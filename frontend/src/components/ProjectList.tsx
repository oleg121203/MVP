import React, { useEffect, useState } from 'react';
import { useLoading } from '../context/LoadingContext';
import { useTranslation } from 'react-i18next';

// Define the Project interface
interface Project {
  id: string; // Assuming id is a string, adjust if it's a number
  name: string;
  description: string;
  created_at: string; // Assuming created_at is a string (ISO date), adjust if it's a Date object
}

export const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState('');
  const { withLoading } = useLoading();
  const { t } = useTranslation();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        await withLoading(async () => {
          const response = await fetch('/api/projects');
          if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
          }
          const data = await response.json();
          setProjects(data);
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load projects');
      }
    };

    fetchProjects();
  }, [withLoading]);

  if (error) return <div className="text-red-500">{t('projects.error', { message: error })}</div>;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">{t('projects.title')}</h2>
      {projects.length === 0 ? (
        <div className="text-gray-500">{t('projects.noProjects')}</div>
      ) : (
        <ul className="space-y-2">
          {projects.map((project) => (
            <li key={project.id} className="p-4 border rounded-lg hover:bg-gray-50">
              <h3 className="font-medium">{project.name}</h3>
              <p className="text-gray-600">{project.description}</p>
              <p className="text-sm text-gray-400">
                Created: {new Date(project.created_at).toLocaleDateString()}
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
