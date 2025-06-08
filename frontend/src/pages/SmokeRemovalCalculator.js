import React, { useState } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { useTheme } from './context/ThemeContext';
import { Button, Input, Form, FormGroup } from './components/ui';
import SimpleAIWrapper from '../components/ai/SimpleAIWrapper';

const SmokeRemovalCalculator = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [mode, setMode] = useState('corridor'); // 'corridor' або 'room'

  // Стан для розрахунку для коридору
  const [corridorWidth, setCorridorWidth] = useState('');
  const [corridorHeight, setCorridorHeight] = useState('');
  const [airVelocity, setAirVelocity] = useState('1');

  // Стан для розрахунку для приміщення
  const [firePerimeter, setFirePerimeter] = useState('');
  const [smokeFreeHeight, setSmokeFreeHeight] = useState('2.5');

  // Загальний стан для результатів та збереження
  const [result, setResult] = useState(null);
  const [complianceInfo, setComplianceInfo] = useState(null);
  const [selectedProjectId, setSelectedProjectId] = useState(
    projects?.length > 0 ? projects[0].id : ''
  );
  const [errors, setErrors] = useState({});
  const [showAnimation, setShowAnimation] = useState(false);

  const handleCalculate = () => {
    // Reset errors and animation state
    setErrors({});

    let calculatedL = 0;
    let complianceInfo = null;
    const newErrors = {};

    if (mode === 'corridor') {
      const b = parseFloat(corridorWidth);
      const h = parseFloat(corridorHeight);
      const v = parseFloat(airVelocity);

      // Validate inputs
      if (isNaN(b) || b <= 0) newErrors.corridorWidth = t('smokeRemoval.invalidWidth');
      if (isNaN(h) || h <= 0) newErrors.corridorHeight = t('smokeRemoval.invalidHeight');
      if (isNaN(v) || v <= 0) newErrors.airVelocity = t('smokeRemoval.invalidVelocity');

      if (Object.keys(newErrors).length === 0) {
        calculatedL = b * h * v * 3600;

        // Check DBN compliance for corridor velocity (ДБН В.1.1-7:2016)
        complianceInfo = {
          velocity: v,
          corridorWidth: b,
          corridorHeight: h,
          isVelocityCompliant: v >= 0.5 && v <= 2.0, // Рекомендовані швидкості для коридорів
          isGeometryCompliant: b >= 1.2 && h >= 2.1, // Мінімальні геометричні параметри
        };
      }
    } else if (mode === 'room') {
      const p = parseFloat(firePerimeter);
      const y = parseFloat(smokeFreeHeight);
      const K = 0.36; // Коефіцієнт згідно ДСТУ 8828:2019
      const smokeDensity = 1.1; // Густина диму, кг/м³

      // Validate inputs
      if (isNaN(p) || p <= 0) newErrors.firePerimeter = t('smokeRemoval.invalidPerimeter');
      if (isNaN(y) || y <= 0) newErrors.smokeFreeHeight = t('smokeRemoval.invalidHeight');

      if (Object.keys(newErrors).length === 0) {
        const massFlowG = K * p * Math.pow(y, 1.5);
        calculatedL = (massFlowG / smokeDensity) * 3600;

        // Check DSTU compliance for room parameters
        complianceInfo = {
          firePerimeter: p,
          smokeFreeHeight: y,
          massFlow: massFlowG,
          isHeightCompliant: y >= 2.0, // Мінімальна висота вільного шару
          isPerimeterRealistic: p >= 2 && p <= 50, // Реалістичні межі периметра пожежі
        };
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setResult(null);
      setComplianceInfo(null);
      return;
    }

    if (calculatedL > 0) {
      setResult(calculatedL.toFixed(0));
      setComplianceInfo(complianceInfo);
      setShowAnimation(true);
    } else {
      setErrors({ general: t('smokeRemoval.errorMessage') });
      setResult(null);
      setComplianceInfo(null);
    }
  };

  const handleSaveToProject = () => {
    if (result === null || !selectedProjectId) return;

    const specString = t('smokeRemoval.saveMessage', { result });
    addSpecToProject(parseInt(selectedProjectId), specString);
  };

  return (
    <SimpleAIWrapper 
      calculatorType="smoke-removal"
      currentInputData={{
        mode,
        corridorWidth,
        corridorHeight,
        airVelocity,
        firePerimeter,
        smokeFreeHeight
      }}
    >
      <div className="max-w-3xl mx-auto my-8 p-8 bg-base-100 dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100 mb-6">
        {t('smokeRemoval.title')}
      </h2>

      <div className="flex justify-center mb-6 gap-2">
        <Button
          onClick={() => {
            setMode('corridor');
            setErrors({});
          }}
          variant={mode === 'corridor' ? 'primary' : 'secondary'}
        >
          {t('smokeRemoval.corridorMode')}
        </Button>
        <Button
          onClick={() => {
            setMode('room');
            setErrors({});
          }}
          variant={mode === 'room' ? 'primary' : 'secondary'}
        >
          {t('smokeRemoval.roomMode')}
        </Button>
      </div>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
        <Form>
          {errors.general && (
            <div className="text-error mb-4 text-center p-2 bg-error/5 dark:bg-error/10 rounded">
              {errors.general}
            </div>
          )}

          {mode === 'corridor' ? (
            <div className="animate-fadeIn">
              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('smokeRemoval.corridorWidth')}:`}
                    value={corridorWidth}
                    onChange={(e) => setCorridorWidth(e.target.value)}
                    min="0.1"
                    step="0.1"
                    placeholder={t('smokeRemoval.corridorWidthPlaceholder')}
                    error={errors.corridorWidth}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.meter')}
                  </span>
                </div>
              </FormGroup>

              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('smokeRemoval.corridorHeight')}:`}
                    value={corridorHeight}
                    onChange={(e) => setCorridorHeight(e.target.value)}
                    min="0.1"
                    step="0.1"
                    placeholder={t('smokeRemoval.corridorHeightPlaceholder')}
                    error={errors.corridorHeight}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.meter')}
                  </span>
                </div>
              </FormGroup>

              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('smokeRemoval.airVelocity')}:`}
                    value={airVelocity}
                    onChange={(e) => setAirVelocity(e.target.value)}
                    min="0.1"
                    step="0.1"
                    placeholder={t('smokeRemoval.airVelocityPlaceholder')}
                    error={errors.airVelocity}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.meterPerSecond')}
                  </span>
                </div>
                <small className="block mt-2 text-sm text-gray-600 dark:text-gray-400">
                  {t('smokeRemoval.velocityNote')}
                </small>
              </FormGroup>
            </div>
          ) : (
            <div className="animate-fadeIn">
              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('smokeRemoval.firePerimeter')}:`}
                    value={firePerimeter}
                    onChange={(e) => setFirePerimeter(e.target.value)}
                    min="0.1"
                    step="0.1"
                    placeholder={t('smokeRemoval.firePerimeterPlaceholder')}
                    error={errors.firePerimeter}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.meter')}
                  </span>
                </div>
              </FormGroup>

              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('smokeRemoval.smokeFreeHeight')}:`}
                    value={smokeFreeHeight}
                    onChange={(e) => setSmokeFreeHeight(e.target.value)}
                    min="0.1"
                    step="0.1"
                    placeholder={t('smokeRemoval.smokeFreeHeightPlaceholder')}
                    error={errors.smokeFreeHeight}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.meter')}
                  </span>
                </div>
                <small className="block mt-2 text-sm text-gray-600 dark:text-gray-400">
                  {t('smokeRemoval.heightNote')}
                </small>
              </FormGroup>
            </div>
          )}

          <Button onClick={handleCalculate} variant="primary" className="w-full mt-6">
            {t('common.calculate')}
          </Button>
        </Form>
      </div>

      {result !== null && (
        <>
          <div
            className={`bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8 ${showAnimation ? 'animate-fadeIn' : ''}`}
          >
            <div className="text-center mb-6">
              <h3 className="m-0 mb-2 text-gray-900 dark:text-gray-300">
                {t('smokeRemoval.requiredSmokeExhaust')}
              </h3>
              <div className="text-3xl font-bold text-emerald-600 dark:text-emerald-400 py-3 px-4 bg-gray-200 dark:bg-gray-600 rounded-md inline-block min-w-[200px]">
                {result} {t('common.cubicMeterPerHour')}
              </div>
            </div>

            {complianceInfo && (
              <div className="mb-6">
                {mode === 'corridor' ? (
                  <div className="text-center">
                    {complianceInfo.isVelocityCompliant && (
                      <div className="py-2 px-3 bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 rounded font-bold text-sm inline-block mb-3">
                        ДБН В.1.1-7:2016
                      </div>
                    )}
                    <div className="text-sm text-gray-700 dark:text-gray-300 p-2 bg-gray-200 dark:bg-gray-600 rounded">
                      {complianceInfo.isVelocityCompliant
                        ? t('smokeRemoval.velocityCompliant')
                        : t('smokeRemoval.velocityNonCompliant')}
                      {complianceInfo.isGeometryCompliant
                        ? `, ${t('smokeRemoval.geometryCompliant')}`
                        : `, ${t('smokeRemoval.geometryNonCompliant')}`}
                    </div>
                  </div>
                ) : (
                  <div className="text-center">
                    {complianceInfo.isHeightCompliant && complianceInfo.isPerimeterRealistic && (
                      <div className="py-2 px-3 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded font-bold text-sm inline-block mb-3">
                        ДСТУ 8828:2019
                      </div>
                    )}
                    <div className="text-sm text-gray-700 dark:text-gray-300 p-2 bg-gray-200 dark:bg-gray-600 rounded">
                      {complianceInfo.isHeightCompliant
                        ? t('smokeRemoval.heightCompliant')
                        : t('smokeRemoval.heightNonCompliant')}
                      {complianceInfo.isPerimeterRealistic
                        ? `, ${t('smokeRemoval.perimeterCompliant')}`
                        : `, ${t('smokeRemoval.perimeterNonCompliant')}`}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="text-center text-sm text-gray-500 dark:text-gray-400 italic">
              {t('smokeRemoval.standardsNote')}
            </div>
          </div>

          {projects?.length > 0 && (
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 animate-fadeIn">
              <h4 className="text-center m-0 mb-4">{t('common.saveToProject')}</h4>

              <div className="mb-4">
                <select
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                  value={selectedProjectId}
                  className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
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
        </>
      )}
    </div>
    </SimpleAIWrapper>
  );
};

export default SmokeRemovalCalculator;
