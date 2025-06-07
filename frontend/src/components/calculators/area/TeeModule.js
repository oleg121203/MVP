import React, { useState } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const TeeModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();

  // State for active sub-tab (round or rectangular)
  const [activeSubTab, setActiveSubTab] = useState('round');

  // State for round tee inputs
  const [roundMainDiameter, setRoundMainDiameter] = useState('');
  const [roundBranchDiameter, setRoundBranchDiameter] = useState('');
  const [roundPrice, setRoundPrice] = useState('');

  // State for rectangular tee inputs
  const [rectMainWidth, setRectMainWidth] = useState('');
  const [rectMainHeight, setRectMainHeight] = useState('');
  const [rectBranchWidth, setRectBranchWidth] = useState('');
  const [rectBranchHeight, setRectBranchHeight] = useState('');
  const [rectPrice, setRectPrice] = useState('');

  // State for calculation results
  const [roundResults, setRoundResults] = useState(null);
  const [rectResults, setRectResults] = useState(null);

  // Calculation functions
  const calculateRoundTee = () => {
    // Validate inputs
    if (
      !roundMainDiameter ||
      !roundBranchDiameter ||
      !roundPrice ||
      isNaN(parseFloat(roundMainDiameter)) ||
      isNaN(parseFloat(roundBranchDiameter)) ||
      isNaN(parseFloat(roundPrice))
    ) {
      error(t('alert_tee_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D_main_m = parseFloat(roundMainDiameter) / 1000;
    const D_branch_m = parseFloat(roundBranchDiameter) / 1000;
    const price = parseFloat(roundPrice);

    // Calculate area: S = π * D_main * (D_main/2) + π * D_branch * (D_branch/2)
    // This is an approximation formula for the surface area of a round tee
    const area = Math.PI * D_main_m * (D_main_m / 2) + Math.PI * D_branch_m * (D_branch_m / 2);

    // Calculate cost
    const cost = area * price;

    // Set results
    setRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_tee') + ': ' + t('results_title'));
  };

  const calculateRectangularTee = () => {
    // Validate inputs
    if (
      !rectMainWidth ||
      !rectMainHeight ||
      !rectBranchWidth ||
      !rectBranchHeight ||
      !rectPrice ||
      isNaN(parseFloat(rectMainWidth)) ||
      isNaN(parseFloat(rectMainHeight)) ||
      isNaN(parseFloat(rectBranchWidth)) ||
      isNaN(parseFloat(rectBranchHeight)) ||
      isNaN(parseFloat(rectPrice))
    ) {
      error(t('alert_tee_rect_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_main_m = parseFloat(rectMainWidth) / 1000;
    const B_main_m = parseFloat(rectMainHeight) / 1000;
    const A_branch_m = parseFloat(rectBranchWidth) / 1000;
    const B_branch_m = parseFloat(rectBranchHeight) / 1000;
    const price = parseFloat(rectPrice);

    // Calculate area: S = 2 * (A_main * B_main) + (A_branch * B_branch)
    // This is an approximation formula for the surface area of a rectangular tee
    const area = 2 * (A_main_m * B_main_m) + A_branch_m * B_branch_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_tee') + ': ' + t('results_title'));
  };

  return (
    <div className="tee-module">
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
        <div className="round-tee-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/tee_round_duct.svg" alt="Round Tee Duct" />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-main-diameter">{t('main_diameter')} (mm):</label>
                <input
                  id="round-main-diameter"
                  type="number"
                  value={roundMainDiameter}
                  onChange={(e) => setRoundMainDiameter(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-branch-diameter">{t('branch_diameter')} (mm):</label>
                <input
                  id="round-branch-diameter"
                  type="number"
                  value={roundBranchDiameter}
                  onChange={(e) => setRoundBranchDiameter(e.target.value)}
                  placeholder="150"
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

          <button className="calculate-button" onClick={calculateRoundTee}>
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
        <div className="rectangular-tee-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/tee_rectangular_duct.svg" alt="Rectangular Tee Duct" />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-main-width">{t('main_width')} (mm):</label>
                <input
                  id="rect-main-width"
                  type="number"
                  value={rectMainWidth}
                  onChange={(e) => setRectMainWidth(e.target.value)}
                  placeholder="400"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-main-height">{t('main_height')} (mm):</label>
                <input
                  id="rect-main-height"
                  type="number"
                  value={rectMainHeight}
                  onChange={(e) => setRectMainHeight(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
          </div>

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-branch-width">{t('branch_width')} (mm):</label>
                <input
                  id="rect-branch-width"
                  type="number"
                  value={rectBranchWidth}
                  onChange={(e) => setRectBranchWidth(e.target.value)}
                  placeholder="300"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-branch-height">{t('branch_height')} (mm):</label>
                <input
                  id="rect-branch-height"
                  type="number"
                  value={rectBranchHeight}
                  onChange={(e) => setRectBranchHeight(e.target.value)}
                  placeholder="150"
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

          <button className="calculate-button" onClick={calculateRectangularTee}>
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

export default TeeModule;
