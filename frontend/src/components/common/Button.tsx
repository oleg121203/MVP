import React from 'react';
import { Button as ChakraButton, ButtonProps } from '@chakra-ui/react';

const Button: React.FC<ButtonProps & { loading?: boolean; loadingText?: string }> = ({ children, loading, loadingText, ...props }) => {
  return (
    <ChakraButton {...props as any} isLoading={loading} loadingText={loadingText}>
      {children}
    </ChakraButton>
  );
};

export default Button;
