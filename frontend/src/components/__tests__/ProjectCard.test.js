import React from 'react';
import { render, screen } from '@testing-library/react';
import ProjectCard from '../ProjectCard';

test('renders project card with title', () => {
  const project = {
    id: 1,
    title: 'Test Project',
    description: 'This is a test project',
    status: 'In Progress'
  };

  render(<ProjectCard project={project} />);
  const titleElement = screen.getByText(/Test Project/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders project card with description', () => {
  const project = {
    id: 1,
    title: 'Test Project',
    description: 'This is a test project',
    status: 'In Progress'
  };

  render(<ProjectCard project={project} />);
  const descriptionElement = screen.getByText(/This is a test project/i);
  expect(descriptionElement).toBeInTheDocument();
});

test('renders project card with status', () => {
  const project = {
    id: 1,
    title: 'Test Project',
    description: 'This is a test project',
    status: 'In Progress'
  };

  render(<ProjectCard project={project} />);
  const statusElement = screen.getByText(/In Progress/i);
  expect(statusElement).toBeInTheDocument();
});
