import React from 'react';
import { Input, FormGroup } from '../ui';

const TemperatureSelectionForm = ({ inputs, onInputChange }) => {
  return (
    <div className="form-grid">
      <FormGroup label="Airflow (m³/h)" htmlFor="airFlow">
        <Input
          type="number"
          id="airFlow"
          name="airFlow"
          value={inputs.airFlow}
          onChange={onInputChange}
          placeholder="e.g., 1500"
        />
      </FormGroup>

      <FormGroup label="Inlet Air Temp (°C)" htmlFor="inletAirTemp">
        <Input
          type="number"
          id="inletAirTemp"
          name="inletAirTemp"
          value={inputs.inletAirTemp}
          onChange={onInputChange}
          placeholder="e.g., -5"
        />
      </FormGroup>

      <FormGroup label="Outlet Air Temp (°C)" htmlFor="outletAirTemp">
        <Input
          type="number"
          id="outletAirTemp"
          name="outletAirTemp"
          value={inputs.outletAirTemp}
          onChange={onInputChange}
          placeholder="e.g., 20"
        />
      </FormGroup>

      <FormGroup label="Inlet Water Temp (°C)" htmlFor="inletWaterTemp">
        <Input
          type="number"
          id="inletWaterTemp"
          name="inletWaterTemp"
          value={inputs.inletWaterTemp}
          onChange={onInputChange}
          placeholder="e.g., 90"
        />
      </FormGroup>

      <FormGroup label="Heat Carrier Type" htmlFor="heatCarrierType">
        <select
          id="heatCarrierType"
          name="heatCarrierType"
          className="custom-select"
          value={inputs.heatCarrierType}
          onChange={onInputChange}
        >
          <option value="water">Water</option>
          <option value="glycol">Glycol</option>
        </select>
      </FormGroup>

      {inputs.heatCarrierType === 'glycol' && (
        <FormGroup label="Glycol %" htmlFor="glycolPercent">
          <Input
            type="number"
            id="glycolPercent"
            name="glycolPercent"
            value={inputs.glycolPercent}
            onChange={onInputChange}
            placeholder="e.g., 30"
          />
        </FormGroup>
      )}
    </div>
  );
};

export default TemperatureSelectionForm;
