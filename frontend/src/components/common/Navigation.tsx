import React, { useState } from 'react';
import { Box, Flex, IconButton, Drawer, DrawerBody, DrawerHeader, DrawerOverlay, DrawerContent, DrawerCloseButton, VStack, Link as ChakraLink, Text, useBreakpointValue } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { FaHome, FaCalculator, FaFolder, FaRobot, FaCog } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Navigation: React.FC = () => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const onClose = () => setIsOpen(false);
  const onOpen = () => setIsOpen(true);

  // Use responsive breakpoint to determine if mobile view
  const isMobile = useBreakpointValue({ base: true, md: false });

  // Navigation items
  const navItems = [
    { to: '/', icon: FaHome, label: t('nav.home') },
    { to: '/calculators', icon: FaCalculator, label: t('nav.calculators') },
    { to: '/projects', icon: FaFolder, label: t('nav.projects') },
    { to: '/project-management', icon: FaFolder, label: t('nav.projectManagement') },
    { to: '/ai-insights', icon: FaRobot, label: t('nav.aiInsights') },
    { to: '/settings', icon: FaCog, label: t('nav.settings') },
  ];

  // Navigation content to reuse in both desktop and mobile views
  const navContent = (
    <VStack spacing={4} align="stretch">
      {navItems.map((item) => (
        <Link to={item.to} key={item.to} style={{ textDecoration: 'none' }}>
          <ChakraLink as="span" _hover={{ color: 'brand.primary' }} display="flex" alignItems="center">
            <item.icon style={{ marginRight: '0.75rem' }} />
            <Text>{item.label}</Text>
          </ChakraLink>
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
          {navItems.map((item) => (
            <Link to={item.to} key={item.to} style={{ textDecoration: 'none' }}>
              <ChakraLink as="span" _hover={{ color: 'brand.primary' }} display="flex" alignItems="center">
                <item.icon style={{ marginRight: '0.5rem' }} />
                <Text>{item.label}</Text>
              </ChakraLink>
            </Link>
          ))}
        </Flex>
      )}
    </Box>
  );
};

export default Navigation;
