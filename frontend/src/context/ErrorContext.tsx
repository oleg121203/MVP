import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useLoading } from './LoadingContext';

type ErrorType = {
  message: string;
  details?: string;
  timestamp: Date;
};

interface ErrorContextType {
  errors: ErrorType[];
  addError: (message: string, details?: string) => void;
  clearErrors: () => void;
}

const ErrorContext = createContext<ErrorContextType | null>(null);

export const ErrorProvider = ({ children }: { children: ReactNode }) => {
  const [errors, setErrors] = useState<ErrorType[]>([]);
  const { withLoading } = useLoading();

  const addError = (message: string, details?: string) => {
    withLoading(
      new Promise<void>((resolve) => {
        setErrors((prev) => [...prev, { message, details, timestamp: new Date() }]);
        resolve();
      })
    );
  };

  const clearErrors = () => {
    setErrors([]);
  };

  return (
    <ErrorContext.Provider value={{ errors, addError, clearErrors }}>
      {children}
    </ErrorContext.Provider>
  );
};

export const useError = () => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
};
