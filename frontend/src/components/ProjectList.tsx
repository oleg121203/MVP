import React, { useEffect, useState } from 'react';
import { apiClient, GetProjectsResponse, Project } from '@/api/client';
import { useLoading } from '@/context/LoadingContext';

export const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState('');
  const { withLoading } = useLoading();

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const { projects } = await withLoading(apiClient.getProjects<GetProjectsResponse>());
        setProjects(projects);
      } catch (err: unknown) {
        setError('Failed to load projects');
        console.error(err);
      }
    };

    fetchProjects();
  }, [withLoading]);

  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Your Projects</h2>
      {projects.length === 0 ? (
        <div className="text-gray-500">No projects found</div>
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
