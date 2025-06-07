import React, { useState, useEffect } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const OffsetModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();

  // State for active sub-tab (round or rectangular)
  const [activeSubTab, setActiveSubTab] = useState('round');

  // State for round offset inputs
  const [roundDiameter, setRoundDiameter] = useState('');
  const [roundOffset, setRoundOffset] = useState('');
  const [roundLength, setRoundLength] = useState('');
  const [roundPrice, setRoundPrice] = useState('');

  // State for rectangular offset inputs
  const [rectWidth, setRectWidth] = useState('');
  const [rectHeight, setRectHeight] = useState('');
  const [rectOffset, setRectOffset] = useState('');
  const [rectLength, setRectLength] = useState('');
  const [rectPrice, setRectPrice] = useState('');

  // State for calculation results
  const [roundResults, setRoundResults] = useState(null);
  const [rectResults, setRectResults] = useState(null);

  // Auto-calculate length for round offset when diameter and offset change
  useEffect(() => {
    if (
      roundDiameter &&
      roundOffset &&
      !isNaN(parseFloat(roundDiameter)) &&
      !isNaN(parseFloat(roundOffset))
    ) {
      // Simplified formula: L = sqrt(offset² + (3*D)²)
      const D = parseFloat(roundDiameter) / 1000; // Convert to meters
      const offset = parseFloat(roundOffset) / 1000; // Convert to meters
      const calculatedLength = Math.sqrt(Math.pow(offset, 2) + Math.pow(3 * D, 2));
      setRoundLength(Math.round(calculatedLength * 1000)); // Convert back to mm and round
    }
  }, [roundDiameter, roundOffset]);

  // Auto-calculate length for rectangular offset when dimensions and offset change
  useEffect(() => {
    if (
      rectWidth &&
      rectHeight &&
      rectOffset &&
      !isNaN(parseFloat(rectWidth)) &&
      !isNaN(parseFloat(rectHeight)) &&
      !isNaN(parseFloat(rectOffset))
    ) {
      // Simplified formula: L = sqrt(offset² + (3*max(A,B))²)
      const A = parseFloat(rectWidth) / 1000; // Convert to meters
      const B = parseFloat(rectHeight) / 1000; // Convert to meters
      const offset = parseFloat(rectOffset) / 1000; // Convert to meters
      const maxDimension = Math.max(A, B);
      const calculatedLength = Math.sqrt(Math.pow(offset, 2) + Math.pow(3 * maxDimension, 2));
      setRectLength(Math.round(calculatedLength * 1000)); // Convert back to mm and round
    }
  }, [rectWidth, rectHeight, rectOffset]);

  // Calculation functions
  const calculateRoundOffset = () => {
    // Validate inputs
    if (
      !roundDiameter ||
      !roundOffset ||
      !roundLength ||
      !roundPrice ||
      isNaN(parseFloat(roundDiameter)) ||
      isNaN(parseFloat(roundOffset)) ||
      isNaN(parseFloat(roundLength)) ||
      isNaN(parseFloat(roundPrice))
    ) {
      error(t('alert_offset_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D_m = parseFloat(roundDiameter) / 1000;
    const offset_m = parseFloat(roundOffset) / 1000;
    const length_m = parseFloat(roundLength) / 1000;
    const price = parseFloat(roundPrice);

    // Calculate area: S = π * D * L
    const area = Math.PI * D_m * length_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
      offset: offset_m.toFixed(2),
      length: length_m.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_offset') + ': ' + t('results_title'));
  };

  const calculateRectangularOffset = () => {
    // Validate inputs
    if (
      !rectWidth ||
      !rectHeight ||
      !rectOffset ||
      !rectLength ||
      !rectPrice ||
      isNaN(parseFloat(rectWidth)) ||
      isNaN(parseFloat(rectHeight)) ||
      isNaN(parseFloat(rectOffset)) ||
      isNaN(parseFloat(rectLength)) ||
      isNaN(parseFloat(rectPrice))
    ) {
      error(t('alert_offset_rectangular_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_m = parseFloat(rectWidth) / 1000;
    const B_m = parseFloat(rectHeight) / 1000;
    const offset_m = parseFloat(rectOffset) / 1000;
    const length_m = parseFloat(rectLength) / 1000;
    const price = parseFloat(rectPrice);

    // Calculate area: S = 2 * (A + B) * L
    const area = 2 * (A_m + B_m) * length_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
      offset: offset_m.toFixed(2),
      length: length_m.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_offset') + ': ' + t('results_title'));
  };

  return (
    <div className="offset-module">
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
        <div className="round-offset-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/offset_round_duct.svg" alt="Round Offset" />
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
            <label htmlFor="round-offset">
              {t('offset')} ({t('unit_mm')})
            </label>
            <input
              id="round-offset"
              type="number"
              value={roundOffset}
              onChange={(e) => setRoundOffset(e.target.value)}
              placeholder="300"
            />
          </div>

          <div className="input-group">
            <label htmlFor="round-length">
              {t('length_L')} ({t('unit_mm')})
            </label>
            <input
              id="round-length"
              type="number"
              value={roundLength}
              onChange={(e) => setRoundLength(e.target.value)}
              placeholder="1000"
              readOnly
            />
            <small className="helper-text">{t('auto_calculated')}</small>
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

          <button className="calculate-button" onClick={calculateRoundOffset}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {roundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('offset')}:</span>
                <span>
                  {roundResults.offset} {t('unit_m')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('length_L')}:</span>
                <span>
                  {roundResults.length} {t('unit_m')}
                </span>
              </div>
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
        <div className="rectangular-offset-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage src="/images/offset_rectangular_duct.svg" alt="Rectangular Offset" />
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
            <label htmlFor="rect-offset">
              {t('offset')} ({t('unit_mm')})
            </label>
            <input
              id="rect-offset"
              type="number"
              value={rectOffset}
              onChange={(e) => setRectOffset(e.target.value)}
              placeholder="300"
            />
          </div>

          <div className="input-group">
            <label htmlFor="rect-length">
              {t('length_L')} ({t('unit_mm')})
            </label>
            <input
              id="rect-length"
              type="number"
              value={rectLength}
              onChange={(e) => setRectLength(e.target.value)}
              placeholder="1000"
              readOnly
            />
            <small className="helper-text">{t('auto_calculated')}</small>
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

          <button className="calculate-button" onClick={calculateRectangularOffset}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('offset')}:</span>
                <span>
                  {rectResults.offset} {t('unit_m')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('length_L')}:</span>
                <span>
                  {rectResults.length} {t('unit_m')}
                </span>
              </div>
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

export default OffsetModule;
