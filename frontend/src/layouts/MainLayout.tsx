import React, { ReactNode } from 'react';
import { Box, Flex, VStack, HStack, Text, IconButton, useDisclosure, Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton, DrawerHeader, DrawerBody } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { Link } from 'react-router-dom';
import LanguageSwitcher from '../components/common/LanguageSwitcher';

interface MainLayoutProps {
  children: ReactNode;
  title?: string;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children, title = 'VentAI' }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Flex direction="column" minHeight="100vh" bg="gray.50">
      {/* Header */}
      <Box as="header" bg="teal.500" color="white" px={4} py={3} boxShadow="sm">
        <HStack justifyContent="space-between" alignItems="center">
          <HStack spacing={4}>
            <IconButton
              aria-label="Open menu"
              icon={<HamburgerIcon />}
              onClick={onOpen}
              display={{ base: 'block', md: 'none' }}
            />
            <Text fontSize="xl" fontWeight="bold">{title}</Text>
          </HStack>
          <HStack spacing={4}>
            <HStack spacing={4} display={{ base: 'none', md: 'flex' }}>
              <Link to="/">Home</Link>
              <Link to="/calculators">Calculators</Link>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/automation">Automation</Link>
            </HStack>
            <LanguageSwitcher />
          </HStack>
        </HStack>
      </Box>

      {/* Mobile Drawer */}
      <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">VentAI Menu</DrawerHeader>
          <DrawerBody>
            <VStack spacing={4} align="start">
              <Link to="/" onClick={onClose}>Home</Link>
              <Link to="/calculators" onClick={onClose}>Calculators</Link>
              <Link to="/dashboard" onClick={onClose}>Dashboard</Link>
              <Link to="/automation" onClick={onClose}>Automation</Link>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>

      {/* Main Content */}
      <Box as="main" flex="1" p={4} overflowY="auto">
        {children}
      </Box>

      {/* Footer */}
      <Box as="footer" bg="teal.500" color="white" textAlign="center" py={3} mt="auto">
        <Text>&copy; {new Date().getFullYear()} VentAI. All rights reserved.</Text>
      </Box>
    </Flex>
  );
};

export default MainLayout;
