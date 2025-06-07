import React, { useState, useEffect } from 'react';
import { useTheme } from '../../../context/ThemeContext';
import PrintView from './PrintView';

const SummarySection = ({ t, calculationResults, onSaveToProject }) => {
  const [showPrintView, setShowPrintView] = useState(false);
  const { theme } = useTheme();
  const isDarkMode = theme === 'dark';
  const [isVisible, setIsVisible] = useState(false);
  const [totalArea, setTotalArea] = useState(0);
  const [totalCost, setTotalCost] = useState(0);
  const [itemsCount, setItemsCount] = useState(0);

  useEffect(() => {
    // Calculate totals when calculationResults change
    if (calculationResults && Object.keys(calculationResults).length > 0) {
      let area = 0;
      let cost = 0;
      let count = 0;

      Object.keys(calculationResults).forEach((key) => {
        const result = calculationResults[key];
        if (result) {
          area += parseFloat(result.area || 0);
          cost += parseFloat(result.cost || 0);
          count++;
        }
      });

      setTotalArea(area);
      setTotalCost(cost);
      setItemsCount(count);
      setIsVisible(count > 0);
    } else {
      setIsVisible(false);
    }
  }, [calculationResults]);

  if (!isVisible) return null;

  const handlePrintClick = () => {
    setShowPrintView(true);
  };

  const handleClosePrintView = () => {
    setShowPrintView(false);
  };

  return (
    <>
      <div className={`summary-section ${isDarkMode ? 'dark' : ''}`}>
        <div className="summary-header">
          <h3>{t('summary_title')}</h3>
          <button
            className="print-summary-button"
            onClick={handlePrintClick}
            title={t('print_summary')}
          >
            <button className="print-button" onClick={handlePrintClick}>
              {t('print')}
            </button>
          </button>
        </div>

        <div className="summary-content">
          <div className="summary-item">
            <span className="label">{t('items_count')}:</span>
            <span className="summary-value">{itemsCount}</span>
          </div>

          <div className="summary-item">
            <span className="label">{t('total_area')}:</span>
            <span className="value">
              {totalArea.toFixed(2)} {t('unit_sqm')}
            </span>
          </div>

          <div className="summary-item">
            <span className="label">{t('total_cost')}:</span>
            <span className="value">
              {totalCost.toFixed(2)} {t('unit_uah')}
            </span>
          </div>
        </div>

        <div className="summary-actions">
          <button
            className="save-button"
            onClick={() => {
              // Future implementation: save to project or export
              alert(t('feature_coming_soon'));
            }}
          >
            {t('save_to_project')}
          </button>

          <button
            className="export-button"
            onClick={() => {
              // Future implementation: export to PDF or CSV
              alert(t('feature_coming_soon'));
            }}
          >
            {t('export_results')}
          </button>
        </div>
      </div>

      {showPrintView && (
        <PrintView t={t} calculationResults={calculationResults} onClose={handleClosePrintView} />
      )}
    </>
  );
};

export default SummarySection;
