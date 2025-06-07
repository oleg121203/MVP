import React from 'react';
import { Box, BoxProps } from '@chakra-ui/react';
import { IconType } from 'react-icons';

interface ChakraIconProps extends Omit<BoxProps, 'children'> {
  icon: IconType;
}

const ChakraIcon: React.FC<ChakraIconProps> = ({ icon: IconComponent, ...props }) => {
  const IconElement = IconComponent as React.ComponentType<any>;
  return (
    <Box {...props}>
      <IconElement />
    </Box>
  );
};

export default ChakraIcon;
