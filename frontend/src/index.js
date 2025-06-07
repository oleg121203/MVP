import React from 'react';
import ReactDOM from 'react-dom/client'; // Updated import for React 18
import App from './App';
import { ChakraProvider } from '@chakra-ui/react';
// Optional: if you have a custom theme
// import theme from './theme'; 

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <ChakraProvider> {/* Optional: theme={theme} */}
      <App />
    </ChakraProvider>
  </React.StrictMode>
);
