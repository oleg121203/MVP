import React, { useState } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const BendDuctModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();
  // State for active sub-tab (round or rectangular)
  const [activeSubTab, setActiveSubTab] = useState('round');

  // State for round bend inputs
  const [roundDiameter, setRoundDiameter] = useState('');
  const [roundAngle, setRoundAngle] = useState('90');
  const [roundPrice, setRoundPrice] = useState('');

  // State for rectangular bend inputs
  const [rectWidth, setRectWidth] = useState('');
  const [rectHeight, setRectHeight] = useState('');
  const [rectAngle, setRectAngle] = useState('90');
  const [rectPrice, setRectPrice] = useState('');

  // State for calculation results
  const [roundResults, setRoundResults] = useState(null);
  const [rectResults, setRectResults] = useState(null);

  // Calculation functions
  const calculateRoundBend = () => {
    // Validate inputs
    if (
      !roundDiameter ||
      !roundAngle ||
      !roundPrice ||
      isNaN(parseFloat(roundDiameter)) ||
      isNaN(parseFloat(roundAngle)) ||
      isNaN(parseFloat(roundPrice))
    ) {
      error(t('alert_bend_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D_m = parseFloat(roundDiameter) / 1000;
    const angle = parseFloat(roundAngle);
    const price = parseFloat(roundPrice);

    // Calculate area: S = π * D * (π * D * angle / 360)
    // This is an approximation formula for the surface area of a round bend
    const area = Math.PI * D_m * ((Math.PI * D_m * angle) / 360);

    // Calculate cost
    const cost = area * price;

    // Set results
    setRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_bend') + ': ' + t('results_title'));
  };

  const calculateRectangularBend = () => {
    // Validate inputs
    if (
      !rectWidth ||
      !rectHeight ||
      !rectAngle ||
      !rectPrice ||
      isNaN(parseFloat(rectWidth)) ||
      isNaN(parseFloat(rectHeight)) ||
      isNaN(parseFloat(rectAngle)) ||
      isNaN(parseFloat(rectPrice))
    ) {
      error(t('alert_bend_rectangular_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_m = parseFloat(rectWidth) / 1000;
    const B_m = parseFloat(rectHeight) / 1000;
    const angle = parseFloat(rectAngle);
    const price = parseFloat(rectPrice);

    // Calculate area: S = (A + B) * (π * (A + B) * angle / 360)
    // This is an approximation formula for the surface area of a rectangular bend
    const area = (A_m + B_m) * ((Math.PI * (A_m + B_m) * angle) / 360);

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_bend') + ': ' + t('results_title'));
  };

  return (
    <div className="bend-duct-module">
      {/* Sub-tabs for round and rectangular ducts */}
      <div className="sub-tabs-navigation">
        <button
          className={`tab-button ${activeSubTab === 'round' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('round')}
        >
          {t('subtab_round')}
          <p>{t('bend_duct_round_help')}</p>
        </button>
        <button
          className={`tab-button ${activeSubTab === 'rectangular' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('rectangular')}
        >
          {t('subtab_rectangular')}
          <p>{t('bend_duct_rect_formula')}</p>
        </button>
      </div>

      {/* Content for the active sub-tab */}
      {activeSubTab === 'round' ? (
        <div className="round-bend-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/bend_round_duct.svg" alt="Round Bend Duct" />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
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
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-angle">{t('angle_alpha_deg')}</label>
                <input
                  id="round-angle"
                  type="number"
                  value={roundAngle}
                  onChange={(e) => setRoundAngle(e.target.value)}
                  placeholder="90"
                  min="0"
                  max="180"
                />
              </div>
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="round-price">
              {t('price_per_sqm')} ({t('unit_uah')}):
            </label>
            <input
              id="round-price"
              type="number"
              value={roundPrice}
              onChange={(e) => setRoundPrice(e.target.value)}
              placeholder="500"
            />
          </div>

          <button className="calculate-button" onClick={calculateRoundBend}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {roundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {roundResults.area} {t('unit_sqm')}
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
        <div className="rectangular-bend-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/bend_rectangular_duct.svg" alt="Rectangular Bend Duct" />
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

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-angle">{t('angle_alpha_deg')}</label>
                <input
                  id="rect-angle"
                  type="number"
                  value={rectAngle}
                  onChange={(e) => setRectAngle(e.target.value)}
                  placeholder="90"
                  min="0"
                  max="180"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-price">
                  {t('price_per_m2')} ({t('unit_uah')}):
                </label>
                <input
                  id="rect-price"
                  type="number"
                  value={rectPrice}
                  onChange={(e) => setRectPrice(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
          </div>

          <button className="calculate-button" onClick={calculateRectangularBend}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {rectResults.area} {t('unit_sqm')}
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

export default BendDuctModule;
