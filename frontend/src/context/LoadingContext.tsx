import React, { createContext, useContext, useState, ReactNode } from 'react';

interface LoadingContextProps {
  isLoading: boolean;
  withLoading: <T>(promise: () => Promise<T>) => Promise<T>;
}

const LoadingContext = createContext<LoadingContextProps | undefined>(undefined);

interface LoadingProviderProps {
  children: ReactNode;
}

export const LoadingProvider: React.FC<LoadingProviderProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(false);

  const withLoading = async <T,>(promise: () => Promise<T>): Promise<T> => {
    setIsLoading(true);
    try {
      const result = await promise();
      return result;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LoadingContext.Provider value={{ isLoading, withLoading }}>
      {children}
    </LoadingContext.Provider>
  );
};

export const useLoading = (): LoadingContextProps => {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error('useLoading must be used within a LoadingProvider');
  }
  return context;
};
