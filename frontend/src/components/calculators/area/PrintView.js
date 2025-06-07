import React, { useRef } from 'react';
import { useTheme } from '../../../context/ThemeContext';

const PrintView = ({ t, calculationResults, onClose }) => {
  const { theme } = useTheme();
  const isDarkMode = theme === 'dark';
  const printRef = useRef();

  // Function to handle printing
  const handlePrint = () => {
    const printContent = printRef.current;
    const originalContents = document.body.innerHTML;

    // Create a print-friendly version
    document.body.innerHTML = printContent.innerHTML;

    // Add print-specific styles
    const style = document.createElement('style');
    style.innerHTML = `
      @media print {
        body {
          font-family: Arial, sans-serif;
          color: #000;
          background-color: #fff;
        }
        .print-header {
          text-align: center;
          margin-bottom: 20px;
        }
        .print-date {
          text-align: right;
          margin-bottom: 20px;
          font-size: 0.9rem;
        }
        .print-section {
          margin-bottom: 15px;
          page-break-inside: avoid;
        }
        .print-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 20px;
        }
        .print-table th, .print-table td {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: left;
        }
        .print-table th {
          background-color: #f2f2f2;
        }
        .print-footer {
          text-align: center;
          margin-top: 30px;
          font-size: 0.8rem;
          color: #666;
        }
        .no-print {
          display: none;
        }
      }
    `;
    document.head.appendChild(style);

    // Print the document
    window.print();

    // Restore original content
    document.body.innerHTML = originalContents;
  };

  // Function to get current date in localized format
  const getCurrentDate = () => {
    const now = new Date();
    return now.toLocaleDateString(t('locale_code') || 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Function to get module name from key
  const getModuleName = (key) => {
    const moduleMap = {
      straight_duct: t('tab_straight_duct'),
      bend: t('tab_bend'),
      transition: t('tab_transition'),
      tee: t('tab_tee'),
      cap: t('tab_cap'),
      cutin: t('tab_cutin'),
      offset: t('tab_offset'),
      hood: t('tab_hood'),
    };
    return moduleMap[key] || key;
  };

  // Calculate totals
  const calculateTotals = () => {
    let totalArea = 0;
    let totalCost = 0;
    let itemCount = 0;

    Object.keys(calculationResults).forEach((key) => {
      const result = calculationResults[key];
      if (result) {
        totalArea += parseFloat(result.area || 0);
        totalCost += parseFloat(result.cost || 0);
        itemCount++;
      }
    });

    return { totalArea, totalCost, itemCount };
  };

  const { totalArea, totalCost, itemCount } = calculateTotals();

  return (
    <div className={`print-view-overlay ${isDarkMode ? 'dark' : ''}`}>
      <div className="print-view-container">
        <div className="print-view-header">
          <h1>{t('print_summary_title')}</h1>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="print-view-content" ref={printRef}>
          <div className="print-header">
            <h1>{t('duct_calculator_title')}</h1>
          </div>

          <div className="print-date">
            {t('print_date')}: {new Date().toLocaleString()}
          </div>

          {itemCount > 0 ? (
            <>
              <div className="print-section">
                <h2>{t('calculation_details')}</h2>
                <table className="print-table">
                  <thead>
                    <tr>
                      <th>{t('item_type')}</th>
                      <th>
                        {t('area')} ({t('unit_sqm')})
                      </th>
                      <th>
                        {t('cost')} ({t('unit_uah')})
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.keys(calculationResults).map((key) => {
                      const result = calculationResults[key];
                      if (!result) return null;

                      return (
                        <tr key={key}>
                          <td>{getModuleName(key)}</td>
                          <td>{parseFloat(result.area || 0).toFixed(2)}</td>
                          <td>{parseFloat(result.cost || 0).toFixed(2)}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                  <tfoot>
                    <tr>
                      <th>{t('item')}</th>
                      <th>{totalArea.toFixed(2)}</th>
                      <th>{totalCost.toFixed(2)}</th>
                    </tr>
                  </tfoot>
                </table>
              </div>

              <div className="print-totals">
                <div className="print-total-item">
                  <span className="print-total-label">{t('total_area')}:</span>
                  <span className="print-total-value">
                    {totalArea.toFixed(2)} {t('unit_sqm')}
                  </span>
                </div>
                <div className="print-total-item">
                  <span className="print-total-label">{t('total_cost')}:</span>
                  <span className="print-total-value">
                    {totalCost.toFixed(2)} {t('unit_uah')}
                  </span>
                </div>
                {t('print_footer')}
              </div>
            </>
          ) : (
            <div className="no-results">{t('no_calculations')}</div>
          )}
        </div>

        <div className="print-view-actions no-print">
          <button className="print-button" onClick={handlePrint}>
            {t('print')}
          </button>
          <button className="print-close-button" onClick={onClose}>
            {t('close')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PrintView;
