import React from 'react';
import { Box, Flex, IconButton, Menu, MenuButton, MenuList, MenuItem, useDisclosure, Drawer, DrawerBody, DrawerHeader, DrawerOverlay, DrawerContent, DrawerCloseButton, VStack, Link as ChakraLink } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { FaHome, FaCalculator, FaProjectDiagram, FaRobot, FaCog } from 'react-icons/fa';

const Navigation: React.FC = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const navItems = [
    { label: t('navigation.home'), path: '/', icon: <FaHome /> },
    { label: t('navigation.calculators'), path: '/calculators', icon: <FaCalculator /> },
    { label: t('navigation.projects'), path: '/projects', icon: <FaProjectDiagram /> },
    { label: t('navigation.aiInsights'), path: '/ai-insights', icon: <FaRobot /> },
    { label: t('navigation.settings'), path: '/settings', icon: <FaCog /> },
  ];

  return (
    <Box>
      {/* Desktop Navigation */}
      <Flex display={{ base: 'none', md: 'flex' }} align="center" justify="space-between" bg="brand.background" boxShadow="sm" p={4}>
        <Flex align="center" gap={6} ml={6}>
          {navItems.map((item) => (
            <ChakraLink
              as={Link}
              to={item.path}
              key={item.path}
              fontWeight={location.pathname === item.path ? 'bold' : 'normal'}
              color={location.pathname === item.path ? 'brand.primary' : 'text.primary'}
              display="flex"
              alignItems="center"
              gap={2}
              _hover={{ color: 'brand.primary', textDecoration: 'none' }}
            >
              {item.icon}
              {item.label}
            </ChakraLink>
          ))}
        </Flex>
      </Flex>

      {/* Mobile Navigation */}
      <Flex display={{ base: 'flex', md: 'none' }} align="center" justify="space-between" bg="brand.background" boxShadow="sm" p={4}>
        <Menu>
          <MenuButton
            as={IconButton}
            aria-label={t('navigation.menu')}
            icon={<HamburgerIcon />}
            variant="outline"
            onClick={onOpen}
          />
          <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
            <DrawerOverlay />
            <DrawerContent>
              <DrawerCloseButton />
              <DrawerHeader>{t('navigation.title')}</DrawerHeader>
              <DrawerBody>
                <VStack spacing={4} align="stretch">
                  {navItems.map((item) => (
                    <ChakraLink
                      as={Link}
                      to={item.path}
                      key={item.path}
                      fontWeight={location.pathname === item.path ? 'bold' : 'normal'}
                      color={location.pathname === item.path ? 'brand.primary' : 'text.primary'}
                      display="flex"
                      alignItems="center"
                      gap={2}
                      _hover={{ color: 'brand.primary', textDecoration: 'none' }}
                      onClick={onClose}
                    >
                      {item.icon}
                      {item.label}
                    </ChakraLink>
                  ))}
                </VStack>
              </DrawerBody>
            </DrawerContent>
          </Drawer>
        </Menu>
      </Flex>
    </Box>
  );
};

export default Navigation;
