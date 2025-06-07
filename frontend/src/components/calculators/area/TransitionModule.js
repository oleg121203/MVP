import React, { useState } from 'react';
import { useToast } from '../../../context/ToastContext';
import ThemedImage from '../../ui/ThemedImage';

const TransitionModule = ({ t }) => {
  // Get toast notification functions
  const { error, success } = useToast();

  // State for active sub-tab (round-to-round, rect-to-round, rect-to-rect)
  const [activeSubTab, setActiveSubTab] = useState('round-to-round');

  // State for round-to-round transition inputs
  const [roundToRoundDiameter1, setRoundToRoundDiameter1] = useState('');
  const [roundToRoundDiameter2, setRoundToRoundDiameter2] = useState('');
  const [roundToRoundLength, setRoundToRoundLength] = useState('');
  const [roundToRoundPrice, setRoundToRoundPrice] = useState('');

  // State for rectangular-to-round transition inputs
  const [rectToRoundWidth, setRectToRoundWidth] = useState('');
  const [rectToRoundHeight, setRectToRoundHeight] = useState('');
  const [rectToRoundDiameter, setRectToRoundDiameter] = useState('');
  const [rectToRoundLength, setRectToRoundLength] = useState('');
  const [rectToRoundPrice, setRectToRoundPrice] = useState('');

  // State for rectangular-to-rectangular transition inputs
  const [rectToRectWidth1, setRectToRectWidth1] = useState('');
  const [rectToRectHeight1, setRectToRectHeight1] = useState('');
  const [rectToRectWidth2, setRectToRectWidth2] = useState('');
  const [rectToRectHeight2, setRectToRectHeight2] = useState('');
  const [rectToRectLength, setRectToRectLength] = useState('');
  const [rectToRectPrice, setRectToRectPrice] = useState('');

  // State for calculation results
  const [roundToRoundResults, setRoundToRoundResults] = useState(null);
  const [rectToRoundResults, setRectToRoundResults] = useState(null);
  const [rectToRectResults, setRectToRectResults] = useState(null);

  // Calculation functions
  const calculateRoundToRound = () => {
    // Validate inputs
    if (
      !roundToRoundDiameter1 ||
      !roundToRoundDiameter2 ||
      !roundToRoundLength ||
      !roundToRoundPrice ||
      isNaN(parseFloat(roundToRoundDiameter1)) ||
      isNaN(parseFloat(roundToRoundDiameter2)) ||
      isNaN(parseFloat(roundToRoundLength)) ||
      isNaN(parseFloat(roundToRoundPrice))
    ) {
      error(t('alert_transition_round_to_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const D1_m = parseFloat(roundToRoundDiameter1) / 1000;
    const D2_m = parseFloat(roundToRoundDiameter2) / 1000;
    const L_m = parseFloat(roundToRoundLength) / 1000;
    const price = parseFloat(roundToRoundPrice);

    // Calculate area: S = π * (D1 + D2) / 2 * L
    // This is an approximation formula for the surface area of a truncated cone
    const area = Math.PI * ((D1_m + D2_m) / 2) * L_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRoundToRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_transition') + ': ' + t('results_title'));
  };

  const calculateRectToRound = () => {
    // Validate inputs
    if (
      !rectToRoundWidth ||
      !rectToRoundHeight ||
      !rectToRoundDiameter ||
      !rectToRoundLength ||
      !rectToRoundPrice ||
      isNaN(parseFloat(rectToRoundWidth)) ||
      isNaN(parseFloat(rectToRoundHeight)) ||
      isNaN(parseFloat(rectToRoundDiameter)) ||
      isNaN(parseFloat(rectToRoundLength)) ||
      isNaN(parseFloat(rectToRoundPrice))
    ) {
      error(t('alert_transition_rect_to_round_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A_m = parseFloat(rectToRoundWidth) / 1000;
    const B_m = parseFloat(rectToRoundHeight) / 1000;
    const D_m = parseFloat(rectToRoundDiameter) / 1000;
    const L_m = parseFloat(rectToRoundLength) / 1000;
    const price = parseFloat(rectToRoundPrice);

    // Calculate area: S = ((A + B) / 2 + π * D / 2) * L
    // This is an approximation formula for the surface area of a rectangular to round transition
    const area = ((A_m + B_m) / 2 + (Math.PI * D_m) / 2) * L_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectToRoundResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_transition') + ': ' + t('results_title'));
  };

  const calculateRectToRect = () => {
    // Validate inputs
    if (
      !rectToRectWidth1 ||
      !rectToRectHeight1 ||
      !rectToRectWidth2 ||
      !rectToRectHeight2 ||
      !rectToRectLength ||
      !rectToRectPrice ||
      isNaN(parseFloat(rectToRectWidth1)) ||
      isNaN(parseFloat(rectToRectHeight1)) ||
      isNaN(parseFloat(rectToRectWidth2)) ||
      isNaN(parseFloat(rectToRectHeight2)) ||
      isNaN(parseFloat(rectToRectLength)) ||
      isNaN(parseFloat(rectToRectPrice))
    ) {
      error(t('alert_transition_rect_to_rect_invalid_input'));
      return;
    }

    // Convert inputs to numbers and proper units (mm to m)
    const A1_m = parseFloat(rectToRectWidth1) / 1000;
    const B1_m = parseFloat(rectToRectHeight1) / 1000;
    const A2_m = parseFloat(rectToRectWidth2) / 1000;
    const B2_m = parseFloat(rectToRectHeight2) / 1000;
    const L_m = parseFloat(rectToRectLength) / 1000;
    const price = parseFloat(rectToRectPrice);

    // Calculate area: S = ((A1 + B1) / 2 + (A2 + B2) / 2) * L
    // This is an approximation formula for the surface area of a rectangular to rectangular transition
    const area = ((A1_m + B1_m) / 2 + (A2_m + B2_m) / 2) * L_m;

    // Calculate cost
    const cost = area * price;

    // Set results
    setRectToRectResults({
      area: area.toFixed(2),
      cost: cost.toFixed(2),
    });

    // Show success notification
    success(t('calculator_title') + ' - ' + t('tab_transition') + ': ' + t('results_title'));
  };

  return (
    <div className="transition-module">
      {/* Sub-tabs for different transition types */}
      <div className="sub-tabs-navigation">
        <button
          className={`tab-button ${activeSubTab === 'round-to-round' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('round-to-round')}
        >
          {t('subtab_round_to_round')}
        </button>
        <button
          className={`tab-button ${activeSubTab === 'rect-to-round' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('rect-to-round')}
        >
          {t('subtab_rect_to_round')}
        </button>
        <button
          className={`tab-button ${activeSubTab === 'rect-to-rect' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('rect-to-rect')}
        >
          {t('subtab_rect_to_rect')}
        </button>
      </div>

      {/* Content for the active sub-tab */}
      {activeSubTab === 'round-to-round' && (
        <div className="round-to-round-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage
              src="/images/transition_round_to_round.svg"
              alt="Round to Round Transition"
            />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-to-round-diameter1">{t('diameter')} 1 (mm):</label>
                <input
                  id="round-to-round-diameter1"
                  type="number"
                  value={roundToRoundDiameter1}
                  onChange={(e) => setRoundToRoundDiameter1(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-to-round-diameter2">{t('diameter')} 2 (mm):</label>
                <input
                  id="round-to-round-diameter2"
                  type="number"
                  value={roundToRoundDiameter2}
                  onChange={(e) => setRoundToRoundDiameter2(e.target.value)}
                  placeholder="300"
                />
              </div>
            </div>
          </div>

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-to-round-length">
                  {t('length_L')} ({t('unit_mm')})
                </label>
                <input
                  id="round-to-round-length"
                  type="number"
                  value={roundToRoundLength}
                  onChange={(e) => setRoundToRoundLength(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="round-to-round-price">
                  {t('price_per_sqm')} ({t('unit_uah')})
                </label>
                <input
                  id="round-to-round-price"
                  type="number"
                  value={roundToRoundPrice}
                  onChange={(e) => setRoundToRoundPrice(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
          </div>

          <button className="calculate-button" onClick={calculateRoundToRound}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {roundToRoundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {roundToRoundResults.area} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('cost')}:</span>
                <span>
                  {roundToRoundResults.cost} {t('unit_uah')}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {activeSubTab === 'rect-to-round' && (
        <div className="rect-to-round-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage
              src="/images/transition_rect_to_round.svg"
              alt="Rectangular to Round Transition"
            />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-round-width">{t('width')} (mm):</label>
                <input
                  id="rect-to-round-width"
                  type="number"
                  value={rectToRoundWidth}
                  onChange={(e) => setRectToRoundWidth(e.target.value)}
                  placeholder="400"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-round-height">{t('height')} (mm):</label>
                <input
                  id="rect-to-round-height"
                  type="number"
                  value={rectToRoundHeight}
                  onChange={(e) => setRectToRoundHeight(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
          </div>

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-round-diameter">{t('diameter')} (mm):</label>
                <input
                  id="rect-to-round-diameter"
                  type="number"
                  value={rectToRoundDiameter}
                  onChange={(e) => setRectToRoundDiameter(e.target.value)}
                  placeholder="300"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-round-length">
                  {t('length_L')} ({t('unit_mm')})
                </label>
                <input
                  id="rect-to-round-length"
                  type="number"
                  value={rectToRoundLength}
                  onChange={(e) => setRectToRoundLength(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="rect-to-round-price">
              {t('price_per_sqm')} ({t('unit_uah')})
            </label>
            <input
              id="rect-to-round-price"
              type="number"
              value={rectToRoundPrice}
              onChange={(e) => setRectToRoundPrice(e.target.value)}
              placeholder="500"
            />
          </div>

          <button className="calculate-button" onClick={calculateRectToRound}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectToRoundResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {rectToRoundResults.area} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('cost')}:</span>
                <span>
                  {rectToRoundResults.cost} {t('unit_uah')}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {activeSubTab === 'rect-to-rect' && (
        <div className="rect-to-rect-content">
          {/* Schematic image */}
          <div className="schematic-image">
            <ThemedImage
              src="/images/transition_rect_to_rect.svg"
              alt="Rectangular to Rectangular Transition"
            />
          </div>

          {/* Input form */}
          <h3>{t('input_data_title')}</h3>
          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-width1">{t('width')} 1 (mm):</label>
                <input
                  id="rect-to-rect-width1"
                  type="number"
                  value={rectToRectWidth1}
                  onChange={(e) => setRectToRectWidth1(e.target.value)}
                  placeholder="400"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-height1">{t('height')} 1 (mm):</label>
                <input
                  id="rect-to-rect-height1"
                  type="number"
                  value={rectToRectHeight1}
                  onChange={(e) => setRectToRectHeight1(e.target.value)}
                  placeholder="200"
                />
              </div>
            </div>
          </div>

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-width2">{t('width')} 2 (mm):</label>
                <input
                  id="rect-to-rect-width2"
                  type="number"
                  value={rectToRectWidth2}
                  onChange={(e) => setRectToRectWidth2(e.target.value)}
                  placeholder="300"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-height2">{t('height')} 2 (mm):</label>
                <input
                  id="rect-to-rect-height2"
                  type="number"
                  value={rectToRectHeight2}
                  onChange={(e) => setRectToRectHeight2(e.target.value)}
                  placeholder="150"
                />
              </div>
            </div>
          </div>

          <div className="input-row">
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-length">
                  {t('length_L')} ({t('unit_mm')})
                </label>
                <input
                  id="rect-to-rect-length"
                  type="number"
                  value={rectToRectLength}
                  onChange={(e) => setRectToRectLength(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
            <div className="input-col">
              <div className="input-group">
                <label htmlFor="rect-to-rect-price">
                  {t('price_per_sqm')} ({t('unit_uah')})
                </label>
                <input
                  id="rect-to-rect-price"
                  type="number"
                  value={rectToRectPrice}
                  onChange={(e) => setRectToRectPrice(e.target.value)}
                  placeholder="500"
                />
              </div>
            </div>
          </div>

          <button className="calculate-button" onClick={calculateRectToRect}>
            {t('calculate_button')}
          </button>

          {/* Results section */}
          {rectToRectResults && (
            <div className="results-section">
              <h3>{t('results_title')}</h3>
              <div className="result-row">
                <span className="result-label">{t('area_S')}:</span>
                <span>
                  {rectToRectResults.area} {t('unit_sqm')}
                </span>
              </div>
              <div className="result-row">
                <span className="result-label">{t('cost')}:</span>
                <span>
                  {rectToRectResults.cost} {t('unit_uah')}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TransitionModule;
