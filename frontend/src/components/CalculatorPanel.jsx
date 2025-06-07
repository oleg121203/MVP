import { useState } from 'react';
import { FaFan, FaThermometerHalf, FaTint, FaWind } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';
import {
  calculateAirflow,
  calculateHeatTransfer,
  calculatePressureDrop,
} from '../utils/calculations';

export default function CalculatorPanel() {
  const { t } = useTranslation();
  const [inputs, setInputs] = useState({
    velocity: 2.5,
    ductDiameter: 0.3,
    density: 1.2,
    tempDiff: 10,
    specificHeat: 1.005,
  });

  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleCalculate = () => {
    try {
      if (inputs.velocity <= 0 || inputs.ductDiameter <= 0) {
        throw new Error('Velocity and duct diameter must be positive values');
      }

      const airflow = calculateAirflow(
        inputs.velocity,
        Math.PI * Math.pow(inputs.ductDiameter / 2, 2)
      );
      const heatTransfer = calculateHeatTransfer(
        airflow,
        inputs.density,
        inputs.specificHeat,
        inputs.tempDiff
      );
      const pressureDrop = calculatePressureDrop(
        airflow,
        inputs.ductDiameter,
        10, // ductLength (m)
        0.00015 // roughness (m)
      );

      setResults({
        airflow: airflow.toFixed(2),
        heatTransfer: heatTransfer.toFixed(0),
        pressureDrop: pressureDrop.toFixed(2),
      });
      setError(null);
    } catch (error) {
      setError(error.message);
      setResults(null);
    }
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-2xl p-6 border border-vent-secondary/20">
      <h2 className="text-2xl font-bold mb-6 text-vent-dark flex items-center">
        <FaFan className="mr-2 text-vent-primary" />
        {t('hvacPerformanceCalculator')}
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <h3 className="font-semibold text-vent-primary flex items-center">
            <FaWind className="mr-2" /> {t('airflowParameters')}
          </h3>
          <InputField
            icon={<FaTint />}
            label={t('airVelocity')}
            value={inputs.velocity}
            onChange={(v) => setInputs({ ...inputs, velocity: v })}
          />
          <InputField
            icon={<FaTint />}
            label={t('ductDiameter')}
            value={inputs.ductDiameter}
            onChange={(v) => setInputs({ ...inputs, ductDiameter: v })}
          />
        </div>

        <div className="space-y-4">
          <h3 className="font-semibold text-vent-primary flex items-center">
            <FaThermometerHalf className="mr-2" /> {t('thermalParameters')}
          </h3>
          <InputField
            icon={<FaThermometerHalf />}
            label={t('temperatureDiff')}
            value={inputs.tempDiff}
            onChange={(v) => setInputs({ ...inputs, tempDiff: v })}
          />
          <InputField
            icon={<FaThermometerHalf />}
            label={t('airDensity')}
            value={inputs.density}
            onChange={(v) => setInputs({ ...inputs, density: v })}
          />
        </div>
      </div>

      <button
        onClick={handleCalculate}
        className="mt-6 w-full bg-vent-primary hover:bg-vent-dark text-white font-bold py-3 px-4 rounded-lg transition-all"
      >
        {t('calculateSystemPerformance')}
      </button>

      {error && (
        <div className="mt-8 p-4 bg-red-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-vent-dark">{t('error')}</h3>
          <div className="text-red-600">{error}</div>
        </div>
      )}

      {results && (
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-vent-dark">{t('results')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ResultCard
              icon={<FaWind />}
              label={t('airflowRate')}
              value={`${results.airflow} m³/s`}
            />
            <ResultCard
              icon={<FaThermometerHalf />}
              label={t('heatTransfer')}
              value={`${results.heatTransfer} W`}
            />
            <ResultCard
              icon={<FaTint />}
              label={t('pressureDrop')}
              value={`${results.pressureDrop} Pa/m`}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function InputField({ icon, label, value, onChange }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        <span className="inline-flex items-center">
          {icon} <span className="ml-2">{label}</span>
        </span>
      </label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-vent-primary focus:border-transparent"
      />
    </div>
  );
}

function ResultCard({ icon, label, value }) {
  return (
    <div className="bg-white p-3 rounded shadow-sm">
      <div className="flex items-center text-sm text-vent-primary">
        {icon} <span className="ml-2">{label}</span>
      </div>
      <div className="mt-2 text-xl font-mono">{value}</div>
    </div>
  );
}
