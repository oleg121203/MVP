import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * A wrapper component that redirects to the login page if the user is not authenticated
 * Can also verify if the user has admin role if adminOnly is true
 */
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { token, user } = useAuth();
  const location = useLocation();

  if (!token) {
    // Redirect to login page but save the location they were trying to access
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If this route requires admin privileges and the user is not an admin
  if (adminOnly && (!user || user.role !== 'admin')) {
    // Redirect to projects page if they're authenticated but not an admin
    return <Navigate to="/projects" replace />;
  }

  return children;
};

export default ProtectedRoute;
