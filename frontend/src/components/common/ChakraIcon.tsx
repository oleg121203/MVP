import React from 'react';
import { Box, BoxProps } from '@chakra-ui/react';
import { IconType } from 'react-icons';

interface ChakraIconProps extends BoxProps {
  icon: IconType;
}

const ChakraIcon: React.FC<ChakraIconProps> = ({ icon: IconComponent, ...props }) => {
  return <Box as={IconComponent} {...props} />;
};

export default ChakraIcon;
