import { useState } from 'react';
import { Button, Form, FormGroup, Input } from './components/ui';
import { useLocalization } from './context/LocalizationContext';
import { useTheme } from './context/ThemeContext';

const AirExchangeCalculator = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [mode, setMode] = useState('byRate'); // 'byRate' or 'byPeople'

  // State for calculation by rate
  const [length, setLength] = useState('');
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [airChangeRate, setAirChangeRate] = useState('');

  // State for calculation by people
  const [peopleCount, setPeopleCount] = useState('');
  const [airPerPerson, setAirPerPerson] = useState('30'); // Default standard

  // State for results and UI
  const [results, setResults] = useState(null);
  const [errors, setErrors] = useState({});
  const [showAnimation, setShowAnimation] = useState(false);
  const [selectedProjectId, setSelectedProjectId] = useState(
    projects?.length > 0 ? projects[0].id : ''
  );

  const handleCalculate = () => {
    // Reset errors and animation state
    setErrors({});
    setShowAnimation(false);

    try {
      // Validate inputs based on mode with robust error handling
      const newErrors = {};

      // Clean inputs - remove any non-numeric characters except decimal point
      const cleanInputs = (val) => val.toString().replace(/[^\d.-]/g, '');

      if (mode === 'byRate') {
        // Parse and clean inputs
        const l = parseFloat(cleanInputs(length));
        const w = parseFloat(cleanInputs(width));
        const h = parseFloat(cleanInputs(height));
        const rate = parseFloat(cleanInputs(airChangeRate));

        // Comprehensive validation
        if (isNaN(l)) {
          newErrors.length = t('airExchange.invalidLength');
        } else if (l <= 0) {
          newErrors.length = t('airExchange.positiveLength');
        } else if (l > 1000) {
          newErrors.length = t('airExchange.lengthTooLarge');
        }

        if (isNaN(w)) {
          newErrors.width = t('airExchange.invalidWidth');
        } else if (w <= 0) {
          newErrors.width = t('airExchange.positiveWidth');
        } else if (w > 1000) {
          newErrors.width = t('airExchange.widthTooLarge');
        }

        if (isNaN(h)) {
          newErrors.height = t('airExchange.invalidHeight');
        } else if (h <= 0) {
          newErrors.height = t('airExchange.positiveHeight');
        } else if (h > 100) {
          newErrors.height = t('airExchange.heightTooLarge');
        }

        if (isNaN(rate)) {
          newErrors.airChangeRate = t('airExchange.invalidRate');
        } else if (rate <= 0) {
          newErrors.airChangeRate = t('airExchange.positiveRate');
        } else if (rate > 100) {
          newErrors.airChangeRate = t('airExchange.rateTooHigh');
        }
      } else {
        // By People mode
        const people = parseFloat(cleanInputs(peopleCount));
        const norm = parseFloat(cleanInputs(airPerPerson));

        if (isNaN(people)) {
          newErrors.peopleCount = t('airExchange.invalidPeopleCount');
        } else if (people <= 0) {
          newErrors.peopleCount = t('airExchange.positivePeopleCount');
        } else if (people > 10000) {
          newErrors.peopleCount = t('airExchange.peopleCountTooLarge');
        } else if (!Number.isInteger(people)) {
          // Ensure people count is an integer
          newErrors.peopleCount = t('airExchange.wholePeopleCount');
        }

        if (isNaN(norm)) {
          newErrors.airPerPerson = t('airExchange.invalidAirPerPerson');
        } else if (norm <= 0) {
          newErrors.airPerPerson = t('airExchange.positiveAirPerPerson');
        } else if (norm > 200) {
          newErrors.airPerPerson = t('airExchange.airPerPersonTooHigh');
        }
      }

      // If any errors, stop calculation
      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        setResults(null);
        return;
      }

      // Proceed with calculation (using cleaned inputs)
      const l = parseFloat(cleanInputs(length));
      const w = parseFloat(cleanInputs(width));
      const h = parseFloat(cleanInputs(height));
      const rate = parseFloat(cleanInputs(airChangeRate));

      const people = parseFloat(cleanInputs(peopleCount));
      const norm = parseFloat(cleanInputs(airPerPerson));

      let resultByRate = 0;
      let dbnCompliance = false;

      // Air exchange by room volume and rate
      if (mode === 'byRate' && !isNaN(l) && !isNaN(w) && !isNaN(h) && !isNaN(rate)) {
        const volume = l * w * h;
        resultByRate = volume * rate;

        // Check DBN compliance for different room types
        if (rate >= 2 && rate <= 4) dbnCompliance = true; // Office spaces
        if (rate >= 6 && rate <= 8) dbnCompliance = true; // Bathrooms
        if (rate >= 10 && rate <= 15) dbnCompliance = true; // Kitchens
      }

      let resultByPeople = 0;
      let dstuCompliance = false;

      // Air exchange by people count and air per person
      if (!isNaN(people) && !isNaN(norm) && people > 0 && norm > 0) {
        resultByPeople = people * norm;

        // Check DSTU compliance for fresh air per person
        if (norm >= 30) dstuCompliance = true; // DSTU B EN 16798-1:2018
      }

      const finalResult = Math.max(resultByRate, resultByPeople);

      if (finalResult > 0) {
        setResults({
          byRate: resultByRate.toFixed(1),
          byPeople: resultByPeople.toFixed(1),
          final: finalResult.toFixed(1),
          dbnCompliance,
          dstuCompliance,
          volume: !isNaN(l) && !isNaN(w) && !isNaN(h) ? (l * w * h).toFixed(1) : null,
        });

        // Trigger animation
        setShowAnimation(true);
      } else {
        setErrors({ general: t('airExchange.errorMessage') });
        setResults(null);
      }
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

    const specString =
      `${t('airExchange.title')}:\n` +
      `${t('airExchange.recommendedExchange')}: ${results.final} ${t('common.cubicMeterPerHour')}\n` +
      (results.volume
        ? `${t('airExchange.roomVolume')}: ${results.volume} ${t('common.cubicMeter')}\n`
        : '') +
      `${t('airExchange.calculationMethod')}: ${mode === 'byRate' ? t('airExchange.byRateMode') : t('airExchange.byPeopleMode')}\n` +
      (mode === 'byRate'
        ? `${t('airExchange.dimensions')}: ${length}×${width}×${height} ${t('common.meter')}\n` +
          `${t('airExchange.airChangeRate')}: ${airChangeRate} ${t('airExchange.changesPerHour')}`
        : `${t('airExchange.numberOfPeople')}: ${peopleCount}\n` +
          `${t('airExchange.airPerPerson')}: ${airPerPerson} ${t('common.cubicMeterPerHour')}`);

    addSpecToProject(parseInt(selectedProjectId), specString);
  };

  return (
    <div className="max-w-3xl mx-auto my-8 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-bold text-center text-neutral dark:text-white mb-6">
        {t('airExchange.title')}
      </h2>

      <div className="flex justify-center gap-2 mb-6">
        <Button
          onClick={() => {
            setMode('byRate');
            setErrors({});
          }}
          variant={mode === 'byRate' ? 'primary' : 'secondary'}
        >
          {t('airExchange.byRateMode')}
        </Button>
        <Button
          onClick={() => {
            setMode('byPeople');
            setErrors({});
          }}
          variant={mode === 'byPeople' ? 'primary' : 'secondary'}
        >
          {t('airExchange.byPeopleMode')}
        </Button>
      </div>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-6">
        <Form>
          {errors.general && (
            <div className="text-error bg-error/10 dark:bg-error/20 mb-4 p-2 text-center rounded">
              {errors.general}
            </div>
          )}

          {/* --- Form for calculation by rate --- */}
          {mode === 'byRate' && (
            <div className="transition-all duration-300 opacity-100 transform translate-y-0">
              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('airExchange.roomLength')}:`}
                    value={length}
                    onChange={(e) => setLength(e.target.value)}
                    placeholder={t('airExchange.lengthPlaceholder')}
                    error={errors.length}
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
                    label={`${t('airExchange.roomWidth')}:`}
                    value={width}
                    onChange={(e) => setWidth(e.target.value)}
                    placeholder={t('airExchange.widthPlaceholder')}
                    error={errors.width}
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
                    label={`${t('airExchange.ceilingHeight')}:`}
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                    placeholder={t('airExchange.heightPlaceholder')}
                    error={errors.height}
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
                    label={`${t('airExchange.airChangeRate')}:`}
                    value={airChangeRate}
                    onChange={(e) => setAirChangeRate(e.target.value)}
                    placeholder={t('airExchange.ratePlaceholder')}
                    error={errors.airChangeRate}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('airExchange.changesPerHour')}
                  </span>
                </div>
                <p className="text-xs mt-2 text-gray-500 dark:text-gray-400">
                  {t('airExchange.rateExamples')}
                </p>
              </FormGroup>
            </div>
          )}

          {/* --- Form for calculation by people --- */}
          {mode === 'byPeople' && (
            <div className="transition-all duration-300 opacity-100 transform translate-y-0">
              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('airExchange.numberOfPeople')}:`}
                    value={peopleCount}
                    onChange={(e) => setPeopleCount(e.target.value)}
                    placeholder={t('airExchange.peoplePlaceholder')}
                    error={errors.peopleCount}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.people')}
                  </span>
                </div>
              </FormGroup>

              <FormGroup>
                <div className="relative">
                  <Input
                    type="number"
                    label={`${t('airExchange.airPerPerson')}:`}
                    value={airPerPerson}
                    onChange={(e) => setAirPerPerson(e.target.value)}
                    placeholder={t('airExchange.airPerPersonPlaceholder')}
                    error={errors.airPerPerson}
                  />
                  <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                    {t('common.cubicMeterPerHour')}
                  </span>
                </div>
                <p className="text-xs mt-2 text-gray-500 dark:text-gray-400">
                  {t('airExchange.airPerPersonExamples')}
                </p>
              </FormGroup>
            </div>
          )}

          <Button onClick={handleCalculate} variant="primary" className="w-full mt-6">
            {t('common.calculate')}
          </Button>
        </Form>
      </div>

      {results && (
        <div
          className={`bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-6 ${showAnimation ? 'animate-fadeIn' : ''}`}
        >
          <div className="text-center mb-6">
            <h3 className="text-lg font-semibold mb-2 text-neutral dark:text-gray-200">
              {t('airExchange.recommendedExchange')}
            </h3>
            <div className="text-2xl font-bold text-success dark:text-accent inline-block min-w-[200px] py-3 px-4 bg-gray-200 dark:bg-gray-600 rounded-md">
              {results.final} {t('common.cubicMeterPerHour')}
            </div>
          </div>

          {results.volume && (
            <div className="text-center mb-4 text-lg text-gray-700 dark:text-gray-300">
              {t('airExchange.roomVolume')}: {results.volume} {t('common.cubicMeter')}
            </div>
          )}

          {(parseFloat(results.byRate) > 0 || parseFloat(results.byPeople) > 0) && (
            <div className="text-center mb-6 p-3 bg-gray-200 dark:bg-gray-600 rounded-md text-sm text-gray-700 dark:text-gray-300">
              {t('airExchange.calculationDetails', {
                byRate: results.byRate,
                byPeople: results.byPeople,
              })}
            </div>
          )}

          <div className="flex justify-center gap-3 flex-wrap mb-6">
            {results.dbnCompliance && (
              <div className="px-3 py-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded flex items-center gap-1 text-sm font-medium">
                <span className="text-lg">✓</span> ДБН В.2.2-15:2019
              </div>
            )}
            {results.dstuCompliance && (
              <div className="px-3 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded flex items-center gap-1 text-sm font-medium">
                <span className="text-lg">✓</span> ДСТУ Б EN 16798-1:2018
              </div>
            )}
          </div>

          <div className="text-center text-sm text-gray-500 dark:text-gray-400 italic">
            {t('airExchange.standardsNote')}
          </div>
        </div>
      )}

      {results && projects?.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 animate-fadeIn">
          <h4 className="text-center font-medium mb-4">{t('common.saveToProject')}</h4>

          <div className="mb-4">
            <select
              onChange={(e) => setSelectedProjectId(e.target.value)}
              value={selectedProjectId}
              className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary dark:focus:ring-accent focus:border-transparent"
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
  );
};

// Add this to your tailwind.css or create a new animation class
// @keyframes fadeIn {
//   from { opacity: 0; }
//   to { opacity: 1; }
// }
// .animate-fadeIn { animation: fadeIn 0.5s ease-in; }

export default AirExchangeCalculator;
