import { ChakraProvider, ChakraProviderProps } from '@chakra-ui/react';
// Removed Next.js specific import
import theme from '../theme';

export default function App({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  );
}
