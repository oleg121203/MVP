import React, { useState } from 'react';
import { Box, Flex, IconButton, Drawer, DrawerBody, DrawerHeader, DrawerOverlay, DrawerContent, DrawerCloseButton, VStack, Link as ChakraLink, Text, useBreakpointValue, Tooltip } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { FaHome, FaCalculator, FaFolder, FaRobot, FaCog, FaChartBar, FaBrain, FaTasks, FaLightbulb } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { IconType } from 'react-icons';
import ChakraIcon from './ChakraIcon';
import { useAuth } from '../../context/AuthContext'; 

// Define the expected shape of the Auth context
interface AuthContextType {
  user: { role?: string } | null;
  // Add other properties if needed
}

const Navigation: React.FC = () => {
  const { t } = useTranslation();
  const auth = useAuth() as unknown as AuthContextType;
  const user = auth.user;
  const isAdmin = user && user.role === 'admin';
  const [isOpen, setIsOpen] = useState(false);
  const onClose = () => setIsOpen(false);
  const onOpen = () => setIsOpen(true);

  // Use responsive breakpoint to determine if mobile view
  const isMobile = useBreakpointValue({ base: true, md: false });

  // Navigation items, conditionally rendered based on user role
  const navItems: Array<{ to: string; icon: IconType; label: string; adminOnly?: boolean }> = [
    { to: '/', icon: FaHome, label: t('navigation.home') },
    { to: '/calculators', icon: FaCalculator, label: t('navigation.calculators') },
    { to: '/dashboard', icon: FaChartBar, label: t('navigation.dashboard') },
    { to: '/ai-dashboard', icon: FaBrain, label: t('navigation.aiDashboard') },
    { to: '/projects', icon: FaFolder, label: t('navigation.projects') },
    { to: '/project-management', icon: FaTasks, label: t('navigation.projectManagement'), adminOnly: true },
    { to: '/ai-insights', icon: FaLightbulb, label: t('navigation.aiInsights'), adminOnly: true },
    { to: '/settings', icon: FaCog, label: t('navigation.settings') },
    { to: '/automation', icon: FaRobot, label: t('navigation.automation'), adminOnly: true },
  ];

  // Filter nav items based on user role
  const filteredNavItems = isAdmin ? navItems : navItems.filter(item => !item.adminOnly);

  // Navigation content to reuse in both desktop and mobile views
  const navContent = (
    <VStack spacing={4} align="stretch">
      {filteredNavItems.map((item) => (
        <Link to={item.to} key={item.to} style={{ textDecoration: 'none' }}>
          <Tooltip label={item.label}>
            <ChakraLink as="span" _hover={{ color: 'brand.primary' }} display="flex" alignItems="center" overflow="hidden">
              <ChakraIcon icon={item.icon} mr={3} flexShrink={0} />
              <Text overflow="hidden" textOverflow="ellipsis" whiteSpace="nowrap">{item.label}</Text>
            </ChakraLink>
          </Tooltip>
        </Link>
      ))}
    </VStack>
  );

  return (
    <Box>
      {/* Mobile View - Hamburger Menu with Drawer */}
      {isMobile ? (
        <>
          <IconButton
            icon={<HamburgerIcon />}
            onClick={onOpen}
            variant="outline"
            aria-label={t('nav.openMenu')}
            size="md"
          />
          <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
            <DrawerOverlay />
            <DrawerContent>
              <DrawerCloseButton />
              <DrawerHeader>{t('nav.menu')}</DrawerHeader>
              <DrawerBody>
                {navContent}
              </DrawerBody>
            </DrawerContent>
          </Drawer>
        </>
      ) : (
        /* Desktop View - Horizontal Navigation */
        <Flex as="nav" gap={6} align="center">
          {filteredNavItems.map((item) => (
            <Link to={item.to} key={item.to} style={{ textDecoration: 'none' }}>
              <Tooltip label={item.label}>
                <ChakraLink as="span" _hover={{ color: 'brand.primary' }} display="flex" alignItems="center" overflow="hidden">
                  <ChakraIcon icon={item.icon} mr={2} flexShrink={0} />
                  <Text overflow="hidden" textOverflow="ellipsis" whiteSpace="nowrap">{item.label}</Text>
                </ChakraLink>
              </Tooltip>
            </Link>
          ))}
        </Flex>
      )}
    </Box>
  );
};

export default Navigation;
