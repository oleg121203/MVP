import React, { ReactNode } from 'react';
import { Button as ChakraButton, ButtonProps } from '@chakra-ui/react';

interface CustomButtonProps extends ButtonProps {
  children: ReactNode;
}

const Button: React.FC<CustomButtonProps> = ({ children, ...props }) => {
  return (
    <ChakraButton {...props}>
      {children}
    </ChakraButton>
  );
};

export default Button;
