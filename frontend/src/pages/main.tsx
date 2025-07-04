import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '../App';
import { AuthProvider } from '../context/AuthContext';
import { ErrorProvider } from '../context/ErrorContext';
import { LoadingProvider } from '../context/LoadingContext';
import { ErrorBoundary } from '../components/ErrorBoundary';
import { ChakraProvider } from '@chakra-ui/react';
import '../index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorProvider>
      <LoadingProvider>
        <AuthProvider>
          <ErrorBoundary>
            <ChakraProvider>
              <App />
            </ChakraProvider>
          </ErrorBoundary>
        </AuthProvider>
      </LoadingProvider>
    </ErrorProvider>
  </React.StrictMode>
);
