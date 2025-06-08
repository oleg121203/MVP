import React, { useState } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { useTheme } from './context/ThemeContext';
import { Button, Input, Form, FormGroup } from './components/ui';
import SimpleAIWrapper from './components/ai/SimpleAIWrapper';

const DuctSizingCalculator = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [airflow, setAirflow] = useState('');
  const [velocity, setVelocity] = useState('');
  const [results, setResults] = useState(null);
  const [errors, setErrors] = useState({});
  const [selectedProjectId, setSelectedProjectId] = useState(
    projects?.length > 0 ? projects[0].id : ''
  );
  const [showAnimation, setShowAnimation] = useState(false);

  // AI Enhancement data
  const inputData = { airflow, velocity };

  const handleCalculate = () => {
    // Reset errors and animation state
    setErrors({});
    setShowAnimation(false);

    try {
      // Parse and validate inputs with more robust error handling
      let q, v;

      // Clean input - remove any non-numeric characters except decimal point
      const cleanAirflow = airflow.toString().replace(/[^\d.-]/g, '');
      const cleanVelocity = velocity.toString().replace(/[^\d.-]/g, '');

      // Parse values
      q = parseFloat(cleanAirflow); // m³/h
      v = parseFloat(cleanVelocity); // m/s

      // Comprehensive validation
      const newErrors = {};

      // Airflow validation
      if (isNaN(q)) {
        newErrors.airflow = t('ductSizing.invalidAirflow');
      } else if (q <= 0) {
        newErrors.airflow = t('ductSizing.positiveAirflow');
      } else if (q > 100000) {
        newErrors.airflow = t('ductSizing.airflowTooLarge');
      }

      // Velocity validation
      if (isNaN(v)) {
        newErrors.velocity = t('ductSizing.invalidVelocity');
      } else if (v <= 0) {
        newErrors.velocity = t('ductSizing.positiveVelocity');
      } else if (v > 30) {
        newErrors.velocity = t('ductSizing.velocityTooHigh');
      }

      // If any errors, stop calculation
      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setResults(null);
        return;
      }

      // Convert m³/h to m³/s
      const qms = q / 3600;

      // Calculate area A = Q/v
      const area = qms / v; // m²

      // Validate calculated area is reasonable
      if (area <= 0 || area > 100) {
        setErrors({
          calculation: t('ductSizing.invalidCalculation'),
        });
        setResults(null);
        return;
      }

      // Calculate diameter
      const diameter = Math.sqrt((4 * area) / Math.PI) * 1000; // Convert to mm

      // Check DBN compliance for velocity ranges
      let velocityCompliance = '';
      if (v >= 2 && v <= 5) velocityCompliance = 'residential'; // Житлові будівлі
      if (v >= 4 && v <= 7) velocityCompliance = 'office'; // Офісні будівлі
      if (v >= 6 && v <= 12) velocityCompliance = 'industrial'; // Промислові

      // Calculate rectangular duct options
      const rectangularOptions = [];
      // Generate a few rectangular options with different aspect ratios
      const aspectRatios = [1, 1.5, 2, 3, 4];

      for (const ratio of aspectRatios) {
        const width = Math.sqrt(area * ratio) * 1000; // in mm
        const height = (area * 1000) / width; // in mm

        // Add with proper rounding for better precision
        rectangularOptions.push({
          width: Math.round(width),
          height: Math.round(height),
          ratio: ratio.toFixed(1),
          area: ((Math.round(width) * Math.round(height)) / 1000000).toFixed(4), // Recalculated actual area
        });
      }

      // Create results object with more complete data
      setResults({
        diameter: Math.round(diameter),
        area: area.toFixed(4),
        airflow: q,
        velocity: v,
        velocityCompliance,
        rectangularOptions,
        timestamp: new Date().toISOString(),
      });

      // Trigger animation only if calculation succeeded
      setShowAnimation(true);
    } catch (error) {
      console.error('Calculation error:', error);
      setErrors({
        calculation: t('common.calculationError'),
      });
      setResults(null);
    }
  };

  const handleSaveToProject = () => {
    if (!results || !selectedProjectId) return;

    const rectangularOption = results.rectangularOptions[1]; // Get the option with 1.5:1 ratio
    const specString =
      `${t('ductSizing.title')}:\n` +
      `${t('ductSizing.airflow')}: ${airflow} ${t('common.cubicMeterPerHour')}\n` +
      `${t('ductSizing.airVelocity')}: ${velocity} ${t('common.meterPerSecond')}\n` +
      `${t('ductSizing.roundDuct')}: Ø ${results.diameter} ${t('common.millimeter')}\n` +
      `${t('ductSizing.rectangularOption')}: ${rectangularOption.width} × ${rectangularOption.height} ${t('common.millimeter')}\n` +
      `${t('ductSizing.ductArea')}: ${results.area} ${t('common.squareMeter')}`;

    addSpecToProject(parseInt(selectedProjectId), specString);
  };

  return (
    <SimpleAIWrapper
      calculatorType="duct_sizing"
      inputData={inputData}
      results={results}
    >
      <div className="max-w-3xl mx-auto my-8 p-8 bg-base-100 dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100 mb-6">
        {t('ductSizing.title')}
      </h2>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
        <Form>
          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label={`${t('ductSizing.airflow')}:`}
                value={airflow}
                onChange={(e) => setAirflow(e.target.value)}
                placeholder={t('ductSizing.airflowPlaceholder')}
                error={errors.airflow}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                {t('common.cubicMeterPerHour')}
              </span>
            </div>
          </FormGroup>

          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label={`${t('ductSizing.airVelocity')}:`}
                value={velocity}
                onChange={(e) => setVelocity(e.target.value)}
                placeholder={t('ductSizing.velocityPlaceholder')}
                error={errors.velocity}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                {t('common.meterPerSecond')}
              </span>
            </div>
            <small className="block mt-2 text-sm text-gray-600 dark:text-gray-400">
              {t('ductSizing.velocityRecommendations')}
            </small>
          </FormGroup>

          <Button onClick={handleCalculate} variant="primary" className="w-full mt-6">
            {t('common.calculate')}
          </Button>
        </Form>
      </div>

      {results && (
        <div
          className={`bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8 ${showAnimation ? 'animate-fadeIn' : ''}`}
        >
          <div className="mb-6 text-center">
            <h3 className="m-0 mb-4 text-gray-900 dark:text-gray-100">
              {t('ductSizing.roundDuct')}
            </h3>
            <div className="text-2xl font-bold text-success inline-block min-w-[180px] p-3 bg-gray-200 dark:bg-gray-600 rounded-lg">
              Ø {results.diameter} {t('common.millimeter')}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="m-0 mb-4 text-center text-gray-900 dark:text-gray-100">
              {t('ductSizing.rectangularDucts')}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {results.rectangularOptions.map((option, index) => (
                <div
                  key={index}
                  className="p-3 bg-white dark:bg-gray-600 rounded-lg text-center shadow-sm border border-gray-200 dark:border-gray-500 transition-transform duration-200 cursor-pointer animate-fadeIn hover:scale-105"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="font-bold text-lg text-gray-900 dark:text-gray-100">
                    {option.width} × {option.height} {t('common.millimeter')}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {t('ductSizing.ratio')} {option.ratio}:1
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="text-center mb-4 text-sm text-gray-500 dark:text-gray-400">
            {t('ductSizing.ductArea')}: {results.area} {t('common.squareMeter')}
          </div>

          {results.velocityCompliance && (
            <div className="flex items-center justify-center gap-3 mb-4 flex-wrap">
              <div className="px-3 py-2 bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-100 rounded font-semibold text-sm">
                ДБН {results.velocityCompliance === 'residential' && 'V.2.2-15:2019'}
                {results.velocityCompliance === 'office' && 'V.2.5-67:2013'}
                {results.velocityCompliance === 'industrial' && 'V.2.5-67:2013'}
              </div>
              <span className="text-gray-700 dark:text-gray-300">
                {results.velocityCompliance === 'residential' &&
                  t('ductSizing.residentialCompliance')}
                {results.velocityCompliance === 'office' && t('ductSizing.officeCompliance')}
                {results.velocityCompliance === 'industrial' &&
                  t('ductSizing.industrialCompliance')}
              </span>
            </div>
          )}

          <div className="text-center text-sm text-gray-500 dark:text-gray-400 italic mt-6">
            {t('ductSizing.standardsNote')}
          </div>
        </div>
      )}

      {results && projects?.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 animate-fadeIn">
          <h4 className="text-center m-0 mb-4 font-medium text-gray-900 dark:text-gray-100">
            {t('common.saveToProject')}
          </h4>

          <div className="mb-4">
            <select
              onChange={(e) => setSelectedProjectId(e.target.value)}
              value={selectedProjectId}
              className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-600 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary focus:border-primary dark:focus:ring-primary dark:focus:border-primary"
            >
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
          </div>

          <Button onClick={handleSaveToProject} variant="secondary" className="w-full">
            {t('common.save')}
          </Button>
        </div>
      )}
    </div>
    </SimpleAIWrapper>
  );
};

export default DuctSizingCalculator;
