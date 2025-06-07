import { ChakraProvider } from '@chakra-ui/react';
import theme from '../theme';

interface AppProps {
  Component: React.ComponentType<any>;
  pageProps: Record<string, any>;
}

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  );
}
