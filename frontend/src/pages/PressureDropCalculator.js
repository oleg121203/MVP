import React, { useState, useMemo, useEffect } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { Button, Input, Form, FormGroup } from './components/ui';
import { useTheme } from './context/ThemeContext';

// Довідник коефіцієнтів місцевих опорів (ζ, дзета) згідно з поширеними практиками та нормами
const LOCAL_RESISTANCE_COEFFICIENTS = {
  elbow90: { name: 'Відвід 90°', zeta: 1.1 },
  tee_pass: { name: 'Трійник (на прохід)', zeta: 0.4 },
  tee_branch: { name: 'Трійник (на відгалуження)', zeta: 1.5 },
  grille: { name: 'Вентиляційна решітка', zeta: 2.0 },
  filter_clean: { name: 'Фільтр (чистий)', zeta: 100 },
};

const PressureDropCalculator = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [sections, setSections] = useState([]);
  const [elementType, setElementType] = useState('straight');

  const [airflow, setAirflow] = useState('');
  const [diameter, setDiameter] = useState('');
  const [length, setLength] = useState('');
  const [errors, setErrors] = useState({});
  const [animatingSection, setAnimatingSection] = useState(null);
  const [showAnimation, setShowAnimation] = useState(false);

  const [selectedProjectId, setSelectedProjectId] = useState(
    projects?.length > 0 ? projects[0].id : ''
  );

  const handleAddSection = () => {
    // Reset errors
    setErrors({});

    const L = parseFloat(airflow);
    const D_mm = parseFloat(diameter);

    // Validate inputs
    const newErrors = {};
    if (isNaN(L) || L <= 0) newErrors.airflow = t('pressureDrop.invalidAirflow');
    if (isNaN(D_mm) || D_mm <= 0) newErrors.diameter = t('pressureDrop.invalidDiameter');

    if (elementType === 'straight') {
      const l_m = parseFloat(length);
      if (isNaN(l_m) || l_m <= 0) newErrors.length = t('pressureDrop.invalidLength');
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const D_m = D_mm / 1000;
    const RHO = 1.2; // Густина повітря, кг/м³
    const LAMBDA = 0.025; // Коефіцієнт тертя для сталі

    const area = Math.PI * Math.pow(D_m / 2, 2);
    const velocity = L / (3600 * area);
    const dynamicPressure = (RHO * Math.pow(velocity, 2)) / 2;

    let pressureDrop = 0;
    let sectionName = '';
    let details = `L=${L} м³/год, D=${D_mm} мм`;

    if (elementType === 'straight') {
      const l_m = parseFloat(length);
      const R = (LAMBDA / D_m) * dynamicPressure;
      pressureDrop = R * l_m;
      sectionName = t('pressureDrop.straightSection');
      details += `, ${t('pressureDrop.length')}=${l_m} ${t('common.meter')}`;
    } else {
      const fitting = LOCAL_RESISTANCE_COEFFICIENTS[elementType];
      pressureDrop = fitting.zeta * dynamicPressure;
      sectionName = fitting.name;
    }

    const newSection = {
      id: Date.now(),
      name: sectionName,
      details,
      pressureDrop: pressureDrop.toFixed(2),
    };

    setSections((prevSections) => [...prevSections, newSection]);
    setShowAnimation(true);

    // Clear inputs for straight section after adding
    if (elementType === 'straight') {
      setLength('');
    }
  };

  const handleRemoveSection = (sectionId) => {
    // Mark section for animation
    setAnimatingSection(sectionId);

    // Remove after animation completes
    setTimeout(() => {
      setSections((prevSections) => prevSections.filter((section) => section.id !== sectionId));
      setAnimatingSection(null);
    }, 500); // Match the animation duration in CSS
  };

  // Reset animation flag when sections change
  useEffect(() => {
    if (sections.length > 0) {
      setShowAnimation(true);
    }
  }, [sections.length]);

  const totalPressureDrop = useMemo(() => {
    return sections
      .reduce((total, section) => total + parseFloat(section.pressureDrop), 0)
      .toFixed(2);
  }, [sections]);

  const handleSaveToProject = () => {
    if (totalPressureDrop <= 0 || !selectedProjectId) return;

    const sectionsDescription = sections
      .map((section) => `${section.name}: ${section.details} - ${section.pressureDrop} Па`)
      .join('\n');

    const specString = `Аеродинамічний розрахунок:\n${sectionsDescription}\nЗагальні втрати тиску: ${totalPressureDrop} Па`;
    addSpecToProject(parseInt(selectedProjectId), specString);
  };

  return (
    <div className="max-w-3xl mx-auto my-8 p-8 bg-base-100 dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-semibold text-center text-gray-800 dark:text-gray-100 mb-6">
        {t('pressureDrop.title')}
      </h2>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
        <h3 className="mt-0 text-center text-lg font-medium mb-4">Додати елемент до мережі</h3>

        <Form>
          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label="Витрата повітря (L):"
                value={airflow}
                onChange={(e) => setAirflow(e.target.value)}
                min="0"
                step="10"
                error={errors.airflow}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                м³/год
              </span>
            </div>
          </FormGroup>

          <FormGroup>
            <div className="relative">
              <Input
                type="number"
                label="Діаметр повітроводу (D):"
                value={diameter}
                onChange={(e) => setDiameter(e.target.value)}
                min="0"
                step="10"
                error={errors.diameter}
              />
              <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                мм
              </span>
            </div>
          </FormGroup>

          <FormGroup>
            <label className="block mb-2 text-gray-700 dark:text-gray-300">Тип елемента:</label>
            <select
              value={elementType}
              onChange={(e) => setElementType(e.target.value)}
              className="w-full p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="straight">Пряма ділянка</option>
              {Object.entries(LOCAL_RESISTANCE_COEFFICIENTS).map(([key, { name }]) => (
                <option key={key} value={key}>
                  {name}
                </option>
              ))}
            </select>
          </FormGroup>

          {elementType === 'straight' && (
            <FormGroup>
              <div className="relative animate-fadeIn">
                <Input
                  type="number"
                  label="Довжина ділянки (l):"
                  value={length}
                  onChange={(e) => setLength(e.target.value)}
                  min="0"
                  step="0.1"
                  error={errors.length}
                />
                <span className="absolute right-3 top-9 text-gray-500 dark:text-gray-400 pointer-events-none">
                  м
                </span>
              </div>
            </FormGroup>
          )}

          <Button onClick={handleAddSection} variant="primary" className="w-full mt-4">
            Додати ділянку
          </Button>
        </Form>
      </div>

      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
        <h3 className="mt-0 text-center text-lg font-medium mb-4">
          {t('pressureDrop.networkCalculation')}
        </h3>
        {sections.length > 0 ? (
          <>
            <ul className="list-none p-0 my-6 flex flex-col gap-3">
              {sections.map((section) => (
                <li
                  key={section.id}
                  className={`flex justify-between items-center p-3 bg-white dark:bg-gray-600 rounded-md shadow-sm border border-gray-200 dark:border-gray-500 transition-all duration-500 overflow-hidden ${animatingSection === section.id ? 'opacity-0 max-h-0 mb-0' : 'opacity-100 max-h-24 mb-3'}`}
                >
                  <div className="flex-1">
                    <div className="font-medium mb-1 text-gray-900 dark:text-gray-100">
                      {section.name}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">
                      {section.details}
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="font-bold text-green-600 dark:text-green-400">
                      {section.pressureDrop} Па
                    </span>
                    <Button
                      onClick={() => handleRemoveSection(section.id)}
                      variant="danger"
                      className="p-1 min-w-0"
                      title="Видалити ділянку"
                    >
                      ✕
                    </Button>
                  </div>
                </li>
              ))}
            </ul>
            <div className="mt-6 p-4 bg-gray-200 dark:bg-gray-600 rounded-md text-center font-bold text-lg">
              Загальні втрати тиску:{' '}
              <span className="text-green-700 dark:text-green-400">{totalPressureDrop} Па</span>
            </div>
          </>
        ) : (
          <p className="text-center text-gray-500 dark:text-gray-400 py-8">
            Додайте ділянки для розрахунку
          </p>
        )}
      </div>

      {sections.length > 0 && projects?.length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 animate-fadeIn">
          <h4 className="text-center text-lg font-medium mb-4">Зберегти результат в проекті</h4>

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
            Зберегти
          </Button>
        </div>
      )}
    </div>
  );
};

export default PressureDropCalculator;
