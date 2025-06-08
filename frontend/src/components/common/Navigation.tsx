import React from 'react';
import { Flex, VStack, Link as ChakraLink, Text, Tooltip } from '@chakra-ui/react';
import { FaHome, FaCalculator, FaFolder, FaRobot, FaCog, FaChartBar, FaBrain, FaTasks, FaLightbulb } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { IconType } from 'react-icons';
import ChakraIcon from './ChakraIcon';
import { useAuth } from '../../context/AuthContext'; 

interface NavigationProps {
  isMobile?: boolean;
}

const Navigation: React.FC<NavigationProps> = ({ isMobile = false }) => {
  const { t } = useTranslation();
  
  // Safe auth context usage
  let auth;
  let user = null;
  let isAdmin = false;
  
  try {
    auth = useAuth();
    user = auth?.user || null;
    isAdmin = Boolean(user && user.role === 'admin');
  } catch (error) {
    console.error('Auth context not available:', error);
    auth = null;
    user = null;
    isAdmin = false;
  }

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

  // Render mobile vertical navigation or desktop horizontal navigation
  if (isMobile) {
    return (
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
  }

  return (
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
  );
};

export default Navigation;
