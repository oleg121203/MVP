import React from 'react';
import { useError } from '@/context/ErrorContext';

export const ErrorNotifications: React.FC = () => {
  const { errors, clearErrors } = useError();

  if (errors.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {errors.map((error, index) => (
        <div
          key={index}
          className="p-4 bg-red-100 border-l-4 border-red-500 text-red-700 rounded shadow-lg"
          role="alert"
        >
          <div className="flex justify-between">
            <span className="font-bold">Error</span>
            <button onClick={() => clearErrors()} className="text-red-700 hover:text-red-900">
              ×
            </button>
          </div>
          <p>{error.message}</p>
          {error.details && (
            <details className="mt-2 text-sm">
              <summary>Details</summary>
              <pre className="whitespace-pre-wrap mt-1">{error.details}</pre>
            </details>
          )}
        </div>
      ))}
    </div>
  );
};
