import React from 'react';
import { Button as ChakraButton, ButtonProps } from '@chakra-ui/react';

const Button: React.FC<ButtonProps> = ({ children, ...props }) => {
  return (
    <ChakraButton {...props}>
      {children}
    </ChakraButton>
  );
};

export default Button;
