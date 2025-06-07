import React, { useState, useEffect } from 'react';
import './Tabs.css';

/**
 * Tabs component for creating tabbed navigation between different content sections
 *
 * @param {Object} props - Component props
 * @param {Array<{id: string, label: string, content: React.ReactNode}>} props.tabs - Array of tab objects
 * @param {string} [props.defaultActiveTabId] - ID of the tab that should be active by default
 * @param {Function} [props.onTabChange] - Callback function called when active tab changes
 * @param {string} [props.className] - Additional CSS classes for the tabs container
 * @param {('horizontal'|'vertical')} [props.orientation='horizontal'] - Orientation of the tabs
 * @returns {JSX.Element} Tabs component
 */
const Tabs = ({
  tabs,
  defaultActiveTabId,
  onTabChange,
  className = '',
  orientation = 'horizontal',
}) => {
  // Set initial active tab (default to first tab if not specified)
  const [activeTabId, setActiveTabId] = useState(
    defaultActiveTabId || (tabs.length > 0 ? tabs[0].id : null)
  );

  // Update active tab if defaultActiveTabId changes
  useEffect(() => {
    if (defaultActiveTabId) {
      setActiveTabId(defaultActiveTabId);
    }
  }, [defaultActiveTabId]);

  // Handle tab click
  const handleTabClick = (tabId) => {
    setActiveTabId(tabId);
    if (onTabChange) {
      onTabChange(tabId);
    }
  };

  // Find the content of the active tab
  const activeTabContent = tabs.find((tab) => tab.id === activeTabId)?.content;

  return (
    <div className={`tabs-container ${orientation} ${className}`}>
      <div className="tabs-header" role="tablist" aria-orientation={orientation}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTabId === tab.id}
            aria-controls={`tabpanel-${tab.id}`}
            id={`tab-${tab.id}`}
            className={`tab-button ${activeTabId === tab.id ? 'active' : ''}`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div
        className="tab-content-panel"
        role="tabpanel"
        id={`tabpanel-${activeTabId}`}
        aria-labelledby={`tab-${activeTabId}`}
      >
        {activeTabContent}
      </div>
    </div>
  );
};

export default Tabs;
