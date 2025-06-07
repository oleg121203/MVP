import React, { ReactNode } from 'react';
import { Box, BoxProps } from '@chakra-ui/react';

interface CardProps extends BoxProps {
  children: ReactNode;
}

const Card: React.FC<CardProps> = ({ children, ...props }) => {
  return (
    <Box bg="white" borderRadius="md" boxShadow="md" p={4} {...props}>
      {children}
    </Box>
  );
};

export default Card;
