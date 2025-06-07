import React from 'react';
import { Button as ChakraButton, ButtonProps } from '@chakra-ui/react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: string;
  size?: string;
  isLoading?: boolean;
  leftIcon?: React.ReactElement;
  rightIcon?: React.ReactElement;
}

const Button: React.FC<ButtonProps & { loading?: boolean; loadingText?: string }> = ({ children, loading, loadingText, ...props }) => {
  return (
    <ChakraButton {...props as unknown} isLoading={loading} loadingText={loadingText}>
      {children}
    </ChakraButton>
  );
};

export default Button;
