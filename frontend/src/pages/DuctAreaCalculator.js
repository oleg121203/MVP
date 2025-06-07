import React, { useState } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { useTheme } from './context/ThemeContext';
import './DuctAreaCalculator.css';

// Import calculator modules
import StraightDuctModule from './components/calculators/area/StraightDuctModule';
import BendDuctModule from './components/calculators/area/BendDuctModule';
import TransitionModule from './components/calculators/area/TransitionModule';
import TeeModule from './components/calculators/area/TeeModule';
import CapModule from './components/calculators/area/CapModule';
import CutinModule from './components/calculators/area/CutinModule';
import OffsetModule from './components/calculators/area/OffsetModule';
import HoodModule from './components/calculators/area/HoodModule';
import SummarySection from './components/calculators/area/SummarySection';

const DuctAreaCalculator = ({ projects = [], addSpecToProject }) => {
  // Get global localization and theme from contexts
  const { t } = useLocalization();
  const { theme } = useTheme();

  // State for active tab
  const [activeTab, setActiveTab] = useState('straight_duct');

  // State for calculation results from all modules
  const [calculationResults, setCalculationResults] = useState({});

  // State for selected project ID when saving to project
  const [selectedProjectId, setSelectedProjectId] = useState('');

  // State for save confirmation
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [saveStatus, setSaveStatus] = useState({ success: false, message: '' });

  // Use the global t function for translations
  // Function to handle saving to project
  const handleSaveToProject = () => {
    if (!selectedProjectId) {
      setSaveStatus({
        success: false,
        message: t('error.select_project'),
      });
      return;
    }

    try {
      // Create a specification object with all calculation results
      const specification = {
        type: 'duct_area_calculation',
        name: `Duct Area Calculation - ${new Date().toLocaleString()}`,
        timestamp: new Date().toISOString(),
        data: calculationResults,
      };

      // Call the addSpecToProject function passed from parent
      addSpecToProject(selectedProjectId, specification);

      // Show success message
      setSaveStatus({
        success: true,
        message: t('success.saved_to_project'),
      });

      // Hide the dialog after 3 seconds
      setTimeout(() => {
        setShowSaveDialog(false);
        setSaveStatus({ success: false, message: '' });
      }, 3000);
    } catch (error) {
      console.error('Error saving to project:', error);
      setSaveStatus({
        success: false,
        message: t('error.save_failed'),
      });
    }
  };

  // Function to update calculation results from any module
  const updateCalculationResults = (moduleKey, results) => {
    setCalculationResults((prevResults) => ({
      ...prevResults,
      [moduleKey]: results,
    }));
  };

  // Tabs configuration
  const tabs = [
    { id: 'straight_duct', translationKey: 'tab_straight_duct', component: StraightDuctModule },
    { id: 'bend', translationKey: 'tab_bend', component: BendDuctModule },
    { id: 'transition', translationKey: 'tab_transition', component: TransitionModule },
    { id: 'tee', translationKey: 'tab_tee', component: TeeModule },
    { id: 'cap', translationKey: 'tab_cap', component: CapModule },
    { id: 'cutin', translationKey: 'tab_cutin', component: CutinModule },
    { id: 'offset', translationKey: 'tab_offset', component: OffsetModule },
    { id: 'hood', translationKey: 'tab_hood', component: HoodModule },
  ];

  // Render tab content based on active tab
  const renderTabContent = () => {
    const activeTabConfig = tabs.find((tab) => tab.id === activeTab);
    if (!activeTabConfig) return null;

    const TabComponent = activeTabConfig.component;
    return (
      <div className="tab-content">
        <TabComponent
          t={t}
          onCalculate={(results) => updateCalculationResults(activeTab, results)}
        />
      </div>
    );
  };

  return (
    <div className="duct-area-calculator">
      <h2>{t('common.calculator_title')}</h2>

      {/* Main tabs navigation */}
      <div className="main-tabs-navigation">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {t(`common.${tab.translationKey}`)}
          </button>
        ))}
      </div>

      {/* Calculator content */}
      <div className="calculator-content">{renderTabContent()}</div>

      {/* Summary Section */}
      <SummarySection
        results={calculationResults}
        t={t}
        onSaveToProject={() => setShowSaveDialog(true)}
      />

      {/* Save to Project Dialog */}
      {showSaveDialog && (
        <div className="save-dialog-overlay" onClick={() => setShowSaveDialog(false)}>
          <div className="save-dialog" onClick={(e) => e.stopPropagation()}>
            <h3>{t('save_to_project')}</h3>

            {projects.length > 0 ? (
              <>
                <select
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                  className="project-select"
                >
                  <option value="">{t('common.select_project')}</option>
                  {projects.map((project) => (
                    <option key={project.id} value={project.id}>
                      {project.name}
                    </option>
                  ))}
                </select>

                {saveStatus.message && (
                  <div className={`status-message ${saveStatus.success ? 'success' : 'error'}`}>
                    {saveStatus.message}
                  </div>
                )}

                <div className="dialog-actions">
                  <button
                    onClick={handleSaveToProject}
                    disabled={!selectedProjectId}
                    className="save-button"
                  >
                    {t('common.save')}
                  </button>
                  <button onClick={() => setShowSaveDialog(false)} className="cancel-button">
                    {t('common.cancel')}
                  </button>
                </div>
              </>
            ) : (
              <div className="no-projects">
                <p>{t('common.no_projects_available')}</p>
                <button
                  onClick={() => {
                    setShowSaveDialog(false);
                    // You might want to navigate to projects page here
                  }}
                  className="create-project-button"
                >
                  {t('common.create_project')}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DuctAreaCalculator;
