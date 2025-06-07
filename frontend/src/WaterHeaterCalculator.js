import React, { useState } from 'react';
import './WaterHeaterCalculator.css';
import { Input, FormGroup, Tabs } from './components/ui';
import PowerSelectionForm from './components/calculators/PowerSelectionForm';
import TemperatureSelectionForm from './components/calculators/TemperatureSelectionForm';
import { useToast } from './context/ToastContext';

const WaterHeaterCalculator = () => {
  // State to manage which tab is currently active. 'power' is the default.
  const [activeTab, setActiveTab] = useState('power');
  const { addToast } = useToast();

  // State for input values
  const [inputs, setInputs] = useState({
    // Common inputs for both tabs
    airFlow: '',
    inletAirTemp: '',
    inletWaterTemp: '',
    heatCarrierType: 'water', // 'water' or 'glycol'
    glycolPercent: '0',

    // Tab-specific inputs
    power: '', // For 'power' tab
    outletAirTemp: '', // For 'temperature' tab
  });

  // Placeholder for calculation results
  const [results, setResults] = useState(null);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setResults(null); // Reset results when changing tabs
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs((prev) => ({ ...prev, [name]: value }));
  };

  const handleCalculate = () => {
    // --- Input Validation ---
    const requiredFields = {
      power: ['airFlow', 'power', 'inletAirTemp', 'inletWaterTemp'],
      temperature: ['airFlow', 'inletAirTemp', 'outletAirTemp', 'inletWaterTemp'],
    };

    for (const field of requiredFields[activeTab]) {
      if (inputs[field] === '' || isNaN(parseFloat(inputs[field]))) {
        addToast('Please fill all fields with valid numbers.', 'error');
        setResults(null);
        return;
      }
    }

    // --- Constants ---
    const RHO_AIR = 1.2; // Density of air in kg/m³
    const CP_AIR = 1.006; // Specific heat capacity of air in kJ/kg°C
    const CP_WATER = 4.186; // Specific heat capacity of water in kJ/kg°C
    const RHO_WATER = 1000; // Density of water in kg/m³
    const DELTA_T_WATER_ASSUMED = 20; // Assumed 90/70°C or 80/60°C system

    // --- Parsing Inputs ---
    const L = parseFloat(inputs.airFlow); // Airflow in m³/h
    const t_in_air = parseFloat(inputs.inletAirTemp);
    const t_in_water = parseFloat(inputs.inletWaterTemp);

    let Q_kw; // To hold the calculated or given power in kW
    let calculatedResults = {};

    // --- Air-Side Calculation ---
    if (activeTab === 'power') {
      Q_kw = parseFloat(inputs.power);
      const delta_T_air = Q_kw / ((L / 3600) * RHO_AIR * CP_AIR);
      const t_out_air = t_in_air + delta_T_air;
      calculatedResults.calculatedOutletAirTemp = t_out_air.toFixed(2);
    } else {
      // activeTab === 'temperature'
      const t_out_air = parseFloat(inputs.outletAirTemp);
      if (t_out_air <= t_in_air) {
        addToast('Outlet air temperature must be higher than inlet temperature.', 'error');
        setResults(null);
        return;
      }
      Q_kw = (L / 3600) * RHO_AIR * CP_AIR * (t_out_air - t_in_air);
      calculatedResults.calculatedPower = Q_kw.toFixed(2);
    }

    // --- Water-Side Calculation (Simplified) ---
    if (inputs.heatCarrierType === 'glycol') {
      // Glycol calculations are more complex and depend on concentration.
      // We will implement this as a future enhancement.
      calculatedResults.outletWaterTemp = 'N/A (Glycol)';
      calculatedResults.waterFlow = 'N/A (Glycol)';
    } else {
      // For water:
      const t_out_water = t_in_water - DELTA_T_WATER_ASSUMED;

      // m_water (mass flow) = Q / (Cp_water * delta_T_water)
      const m_water_kg_s = Q_kw / (CP_WATER * DELTA_T_WATER_ASSUMED);

      // V_water (volume flow) = (m_water / rho_water) * 3600
      const v_water_m3_h = (m_water_kg_s / RHO_WATER) * 3600;

      calculatedResults.outletWaterTemp = `${t_out_water.toFixed(2)} °C`;
      calculatedResults.waterFlow = `${v_water_m3_h.toFixed(3)} m³/h`;
    }

    setResults(calculatedResults);
  };

  const TABS_CONFIG = [
    { id: 'power', label: 'Selection by Power' },
    { id: 'temperature', label: 'Selection by Temperature' },
    // The following tabs will be enabled in later steps
    // { id: 'result', label: 'Selection Result' },
    // { id: 'resistance', label: 'Hydraulic Resistance' },
    // { id: 'other_conditions', label: 'Power Under Other Conditions' },
    // { id: 'graph', label: 'Graph' },
  ];

  return (
    <div className="calculator-container water-heater-calculator">
      <div className="calculator-header">
        {/* The title will be dynamic based on localization later */}
        <h2>Water Heater Calculator</h2>
      </div>

      <div className="calculator-content">
        {/* Tabs component for navigation between calculator modes */}
        <div className="calculator-tabs">
          <Tabs tabs={TABS_CONFIG} activeTab={activeTab} onTabChange={handleTabChange} />
        </div>

        <div className="calculator-form">
          {activeTab === 'power' && (
            <PowerSelectionForm inputs={inputs} onInputChange={handleInputChange} />
          )}
          {activeTab === 'temperature' && (
            <TemperatureSelectionForm inputs={inputs} onInputChange={handleInputChange} />
          )}
        </div>

        <div className="controls">
          {/* We will use our custom Button component later */}
          <button onClick={handleCalculate} className="calculate-button">
            Calculate
          </button>
        </div>

        {results && (
          <div className="results-section">
            <h3>Calculation Results</h3>
            <div className="results-grid">
              {activeTab === 'temperature' && results.calculatedPower && (
                <div className="result-item">
                  <span className="result-label">Required Power</span>
                  <span className="result-value">{results.calculatedPower} kW</span>
                </div>
              )}
              {activeTab === 'power' && results.calculatedOutletAirTemp && (
                <div className="result-item">
                  <span className="result-label">Outlet Air Temperature</span>
                  <span className="result-value">{results.calculatedOutletAirTemp} °C</span>
                </div>
              )}
              <div className="result-item">
                <span className="result-label">Outlet Water Temperature</span>
                <span className="result-value">{results.outletWaterTemp}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Water Flow</span>
                <span className="result-value">{results.waterFlow}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WaterHeaterCalculator;
