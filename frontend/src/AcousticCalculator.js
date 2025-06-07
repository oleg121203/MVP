import React, { useState } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { Button, Input, Form, FormGroup } from './components/ui';
import { useTheme } from './context/ThemeContext';

const AcousticCalculator = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [fanPowerLevel, setFanPowerLevel] = useState('');
  const [requiredRoomLevel, setRequiredRoomLevel] = useState('35');
  const [ductLength, setDuctLength] = useState('');
  const [elbowCount, setElbowCount] = useState('');
  const [errors, setErrors] = useState({});

  const [result, setResult] = useState(null);
  const [showAnimation, setShowAnimation] = useState(false);
  const [selectedProjectId, setSelectedProjectId] = useState(
    projects?.length > 0 ? projects[0].id : ''
  );

  // Constants for calculation (simplified)
  const ATTENUATION_PER_METER = 0.5; // dBA/m
  const ATTENUATION_PER_ELBOW = 2; // dBA
  const ATTENUATION_END_REFLECTION = 6; // dBA

  const handleCalculate = () => {
    // Reset errors
    setErrors({});

    const lw_fan = parseFloat(fanPowerLevel);
    const lp_req = parseFloat(requiredRoomLevel);
    const length = parseFloat(ductLength);
    const elbows = parseFloat(elbowCount);

    // Validate inputs
    const newErrors = {};
    if (isNaN(lw_fan) || lw_fan < 0) newErrors.fanPowerLevel = t('acoustic.invalidFanPowerLevel');
    if (isNaN(lp_req) || lp_req < 0) newErrors.requiredRoomLevel = t('acoustic.invalidRoomLevel');
    if (isNaN(length) || length < 0) newErrors.ductLength = t('acoustic.invalidDuctLength');
    if (isNaN(elbows) || elbows < 0) newErrors.elbowCount = t('acoustic.invalidElbowCount');

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // 1. Calculate natural noise attenuation in the network
    const naturalAttenuation =
      length * ATTENUATION_PER_METER + elbows * ATTENUATION_PER_ELBOW + ATTENUATION_END_REFLECTION;

    // 2. Calculate noise level at the grille
    const levelAtGrille = lw_fan - naturalAttenuation;

    // 3. Calculate required noise reduction
    const requiredAttenuation = levelAtGrille - lp_req;

    let recommendation = '';
    if (requiredAttenuation <= 5) {
      recommendation = t('acoustic.noSilencerNeeded');
    } else {
      recommendation = t('acoustic.silencerRecommendation', {
        attenuation: requiredAttenuation.toFixed(0),
      });
    }

    setResult({
      attenuation: requiredAttenuation > 0 ? requiredAttenuation.toFixed(0) : 0,
      recommendation: recommendation,
      naturalAttenuation: naturalAttenuation.toFixed(1),
      levelAtGrille: levelAtGrille.toFixed(1),
    });

    // Trigger animation
    setShowAnimation(true);
  };

  const handleSaveToProject = () => {
    if (!result || !selectedProjectId) return;
    const specString =
      `${t('acoustic.title')}:\n` +
      `${t('acoustic.fanPowerLevel')}: ${fanPowerLevel} ${t('common.dBA')}\n` +
      `${t('acoustic.requiredRoomLevel')}: ${requiredRoomLevel} ${t('common.dBA')}\n` +
      `${t('acoustic.ductLength')}: ${ductLength} ${t('common.meter')}\n` +
      `${t('acoustic.elbowCount')}: ${elbowCount}\n` +
      `${t('acoustic.requiredAttenuation')}: ${result.attenuation} ${t('common.dBA')}\n` +
      `${result.recommendation}`;

    addSpecToProject(parseInt(selectedProjectId), specString);
  };

  return (
    <div className="max-w-3xl mx-auto my-8 p-8 bg-base-100 dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100 mb-6">
        {t('acoustic.title')}
      </h2>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
        <Form>
          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label={`${t('acoustic.fanPowerLevel')}:`}
                value={fanPowerLevel}
                onChange={(e) => setFanPowerLevel(e.target.value)}
                placeholder={t('acoustic.fanPowerLevelPlaceholder')}
                min="0"
                step="1"
                error={errors.fanPowerLevel}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                {t('common.dBA')}
              </span>
            </div>
          </FormGroup>

          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label={`${t('acoustic.requiredRoomLevel')}:`}
                value={requiredRoomLevel}
                onChange={(e) => setRequiredRoomLevel(e.target.value)}
                min="0"
                step="1"
                error={errors.requiredRoomLevel}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                {t('common.dBA')}
              </span>
            </div>
            <small className="block mt-2 text-gray-500 dark:text-gray-400">
              {t('acoustic.roomLevelExamples')}
            </small>
          </FormGroup>

          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label={`${t('acoustic.ductLength')}:`}
                value={ductLength}
                onChange={(e) => setDuctLength(e.target.value)}
                min="0"
                step="0.1"
                error={errors.ductLength}
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
                label={`${t('acoustic.elbowCount')}:`}
                value={elbowCount}
                onChange={(e) => setElbowCount(e.target.value)}
                placeholder={t('acoustic.elbowCountPlaceholder')}
                min="0"
                step="1"
                error={errors.elbowCount}
              />
            </div>
          </FormGroup>

          <Button onClick={handleCalculate} variant="primary" className="w-full mt-6 mb-6">
            {t('common.calculate')}
          </Button>
        </Form>
      </div>

      {result && (
        <>
          <div
            className={`bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8 ${showAnimation ? 'animate-fadeIn' : ''}`}
          >
            <div className="text-center">
              <div className="text-lg mb-2">{t('acoustic.requiredAttenuation')}:</div>
              <span className="block text-3xl font-bold text-green-600 dark:text-green-400 my-2">
                {result.attenuation} {t('common.dBA')}
              </span>
              <div className="text-base bg-gray-200 dark:bg-gray-600 p-3 rounded-md leading-relaxed mt-6">
                {result.recommendation}
              </div>

              <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                <div className="bg-gray-200 dark:bg-gray-600 p-3 rounded-md text-center">
                  <div className="text-gray-600 dark:text-gray-400">
                    {t('acoustic.naturalAttenuation')}
                  </div>
                  <div className="font-bold mt-1">
                    {result.naturalAttenuation} {t('common.dBA')}
                  </div>
                </div>

                <div className="bg-gray-200 dark:bg-gray-600 p-3 rounded-md text-center">
                  <div className="text-gray-600 dark:text-gray-400">
                    {t('acoustic.levelAtGrille')}
                  </div>
                  <div className="font-bold mt-1">
                    {result.levelAtGrille} {t('common.dBA')}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {projects?.length > 0 && (
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 animate-fadeIn">
              <h4 className="text-center text-lg font-medium mb-4">{t('common.saveToProject')}</h4>

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
  );
};

export default AcousticCalculator;
