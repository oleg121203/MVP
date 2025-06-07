import React, { createContext, useContext, useState, ReactNode } from 'react';

type ErrorContextType = {
  errors: string[];
  setError: (error: string) => void;
  clearErrors: () => void;
};

const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

interface ErrorProviderProps {
  children: ReactNode;
}

export const ErrorProvider: React.FC<ErrorProviderProps> = ({ children }) => {
  const [errors, setErrors] = useState<string[]>([]);

  const setError = (error: string) => setErrors(prev => [...prev, error]);
  const clearErrors = () => setErrors([]);

  return (
    <ErrorContext.Provider value={{ errors, setError, clearErrors }}>
      {children}
    </ErrorContext.Provider>
  );
};

export const useError = () => {
  const context = useContext(ErrorContext);
  if (context === undefined) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
};
