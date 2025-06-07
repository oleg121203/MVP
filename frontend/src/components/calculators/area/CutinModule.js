import React, { useState } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const CutinModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();

  // State for active sub-tab (round or rectangular)
  const [activeSubTab, setActiveSubTab] = useState('round');

  // State for round cut-in inputs
  const [roundDiameter, setRoundDiameter] = useState('');
  const [roundPrice, setRoundPrice] = useState('');

  // State for rectangular cut-in inputs
  const [rectWidth, setRectWidth] = useState('');
  const [rectHeight, setRectHeight] = useState('');
  const [rectPrice, setRectPrice] = useState('');

  // State for calculation results
  const [roundResults, setRoundResults] = useState(null);
  const [rectResults, setRectResults] = useState(null);

  // Calculation functions
  const calculateRoundCutin = () => {
    // Validate inputs
    if (
      !roundDiameter ||
      !roundPrice ||
      isNaN(parseFloat(roundDiameter)) ||
      isNaN(parseFloat(roundPrice))
    ) {
      error(t('alert_cutin_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D_m = parseFloat(roundDiameter) / 1000;
    const price = parseFloat(roundPrice);

    // Calculate area: S = π * D (simplified formula for a round cut-in collar)
    const area = Math.PI * D_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_cutin') + ': ' + t('results_title'));
  };

  const calculateRectangularCutin = () => {
    // Validate inputs
    if (
      !rectWidth ||
      !rectHeight ||
      !rectPrice ||
      isNaN(parseFloat(rectWidth)) ||
      isNaN(parseFloat(rectHeight)) ||
      isNaN(parseFloat(rectPrice))
    ) {
      error(t('alert_cutin_rect_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_m = parseFloat(rectWidth) / 1000;
    const B_m = parseFloat(rectHeight) / 1000;
    const price = parseFloat(rectPrice);

    // Calculate area: S = 2 * (A + B) (simplified formula for a rectangular cut-in collar)
    const area = 2 * (A_m + B_m);

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_cutin') + ': ' + t('results_title'));
  };

  return (
    <div className="cutin-module">
      {/* Sub-tabs for round and rectangular ducts */}
      <div className="sub-tabs-navigation">
        <button
          className={`tab-button ${activeSubTab === 'round' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('round')}
        >
          {t('subtab_round')}
        </button>
        <button
          className={`tab-button ${activeSubTab === 'rectangular' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('rectangular')}
        >
          {t('subtab_rectangular')}
        </button>
      </div>

      {/* Content for the active sub-tab */}
      {activeSubTab === 'round' ? (
        <div className="round-cutin-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/cutin_round_duct.svg" alt="Round Cut-in" />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-group">
            <label htmlFor="round-diameter">{t('diameter')} (mm):</label>
            <input
              id="round-diameter"
              type="number"
              value={roundDiameter}
              onChange={(e) => setRoundDiameter(e.target.value)}
              placeholder="200"
            />
          </div>

          <div className="input-group">
            <label htmlFor="round-price">
              {t('price_per_sqm')} ({t('unit_uah')})
            </label>
            <input
              id="round-price"
              type="number"
              value={roundPrice}
              onChange={(e) => setRoundPrice(e.target.value)}
              placeholder="500"
            />
          </div>

          <button className="calculate-button" onClick={calculateRoundCutin}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {roundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {roundResults.area} {t('unit_m')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('cost')}:</span>
                <span>
                  {roundResults.cost} {t('unit_uah')}
                </span>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="rectangular-cutin-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/cutin_rectangular_duct.svg" alt="Rectangular Cut-in" />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-width">{t('width')} (mm):</label>
                <input
                  id="rect-width"
                  type="number"
                  value={rectWidth}
                  onChange={(e) => setRectWidth(e.target.value)}
                  placeholder="400"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-height">{t('height')} (mm):</label>
                <input
                  id="rect-height"
                  type="number"
                  value={rectHeight}
                  onChange={(e) => setRectHeight(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="rect-price">
              {t('price_per_sqm')} ({t('unit_uah')})
            </label>
            <input
              id="rect-price"
              type="number"
              value={rectPrice}
              onChange={(e) => setRectPrice(e.target.value)}
              placeholder="500"
            />
          </div>

          <button className="calculate-button" onClick={calculateRectangularCutin}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {rectResults.area} {t('unit_m')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('cost')}:</span>
                <span>
                  {rectResults.cost} {t('unit_uah')}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CutinModule;
