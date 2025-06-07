import React, { useState } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const HoodModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();

  // State for active sub-tab (round or rectangular)
  const [activeSubTab, setActiveSubTab] = useState('round');

  // State for round hood inputs
  const [roundDiameter, setRoundDiameter] = useState('');
  const [roundHeight, setRoundHeight] = useState('');
  const [roundPrice, setRoundPrice] = useState('');

  // State for rectangular hood inputs
  const [rectWidth, setRectWidth] = useState('');
  const [rectHeight, setRectHeight] = useState('');
  const [rectDepth, setRectDepth] = useState('');
  const [rectPrice, setRectPrice] = useState('');

  // State for calculation results
  const [roundResults, setRoundResults] = useState(null);
  const [rectResults, setRectResults] = useState(null);

  // Calculation functions
  const calculateRoundHood = () => {
    // Validate inputs
    if (
      !roundDiameter ||
      !roundHeight ||
      !roundPrice ||
      isNaN(parseFloat(roundDiameter)) ||
      isNaN(parseFloat(roundHeight)) ||
      isNaN(parseFloat(roundPrice))
    ) {
      error(t('alert_hood_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D_m = parseFloat(roundDiameter) / 1000;
    const H_m = parseFloat(roundHeight) / 1000;
    const price = parseFloat(roundPrice);

    // Calculate area: S = π * D * H + π * (D/2)²
    const sideArea = Math.PI * D_m * H_m;
    const topArea = Math.PI * Math.pow(D_m / 2, 2);
    const totalArea = sideArea + topArea;

    // Calculate cost
    const cost = totalArea * price;

    // Set results
    setRoundResults({
      sideArea: sideArea.toFixed(2),
      topArea: topArea.toFixed(2),
      totalArea: totalArea.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_hood') + ': ' + t('results_title'));
  };

  const calculateRectangularHood = () => {
    // Validate inputs
    if (
      !rectWidth ||
      !rectHeight ||
      !rectDepth ||
      !rectPrice ||
      isNaN(parseFloat(rectWidth)) ||
      isNaN(parseFloat(rectHeight)) ||
      isNaN(parseFloat(rectDepth)) ||
      isNaN(parseFloat(rectPrice))
    ) {
      error(t('alert_hood_rect_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_m = parseFloat(rectWidth) / 1000;
    const B_m = parseFloat(rectHeight) / 1000;
    const H_m = parseFloat(rectDepth) / 1000;
    const price = parseFloat(rectPrice);

    // Calculate area: S = 2 * (A + B) * H + A * B
    const sideArea = 2 * (A_m + B_m) * H_m;
    const topArea = A_m * B_m;
    const totalArea = sideArea + topArea;

    // Calculate cost
    const cost = totalArea * price;

    // Set results
    setRectResults({
      sideArea: sideArea.toFixed(2),
      topArea: topArea.toFixed(2),
      totalArea: totalArea.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_hood') + ': ' + t('results_title'));
  };

  return (
    <div className="hood-module">
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
        <div className="round-hood-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/hood_round_duct.svg" alt="Round Hood" />
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
            <label htmlFor="round-height">{t('height')} (mm):</label>
            <input
              id="round-height"
              type="number"
              value={roundHeight}
              onChange={(e) => setRoundHeight(e.target.value)}
              placeholder="300"
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

          <button className="calculate-button" onClick={calculateRoundHood}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {roundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('side_area')}:</span>
                <span>
                  {roundResults.sideArea} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('top_area')}:</span>
                <span>
                  {roundResults.topArea} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('total_area')}:</span>
                <span>
                  {roundResults.totalArea} {t('unit_sqm')}
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
        <div className="rectangular-hood-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/hood_rectangular_duct.svg" alt="Rectangular Hood" />
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
            <label htmlFor="rect-depth">{t('depth')} (mm):</label>
            <input
              id="rect-depth"
              type="number"
              value={rectDepth}
              onChange={(e) => setRectDepth(e.target.value)}
              placeholder="300"
            />
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

          <button className="calculate-button" onClick={calculateRectangularHood}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('side_area')}:</span>
                <span>
                  {rectResults.sideArea} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('top_area')}:</span>
                <span>
                  {rectResults.topArea} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('total_area')}:</span>
                <span>
                  {rectResults.totalArea} {t('unit_sqm')}
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

export default HoodModule;
