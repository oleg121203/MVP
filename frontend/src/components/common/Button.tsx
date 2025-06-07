import React from 'react';
import { Button as ChakraButton } from '@chakra-ui/react';

interface ButtonProps {
  loading?: boolean;
  loadingText?: string;
  children?: React.ReactNode;
  [key: string]: any; // Allow any additional props
}

const Button: React.FC<ButtonProps> = ({ children, loading, loadingText, ...props }) => {
  return (
    <ChakraButton isLoading={loading} loadingText={loadingText} {...props}>
      {children}
    </ChakraButton>
  );
};

export default Button;
