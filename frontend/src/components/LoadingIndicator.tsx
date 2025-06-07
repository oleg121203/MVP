import React from 'react';
import { useLoading } from '@/context/LoadingContext';

export const LoadingIndicator: React.FC = () => {
  const { isLoading } = useLoading();

  if (!isLoading) return null;

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="p-3 bg-blue-500 text-white rounded-md shadow-lg flex items-center space-x-2">
        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <span>Loading...</span>
      </div>
    </div>
  );
};
