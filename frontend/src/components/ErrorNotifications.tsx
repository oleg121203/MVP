import React from 'react';
import { useError } from '@/context/ErrorContext';

export const ErrorNotifications: React.FC = () => {
  const { errors, clearErrors } = useError();

  if (errors.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {errors.map((error: string, index: number) => (
        <div
          key={index}
          className="p-4 bg-red-100 border-l-4 border-red-500 text-red-700 rounded shadow-lg"
        >
          <div className="flex justify-between items-center">
            <p>{error}</p>
            <button onClick={() => clearErrors()} className="ml-4 text-red-900">
              Dismiss
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};
