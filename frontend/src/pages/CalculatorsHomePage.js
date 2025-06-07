import React, { useState, useEffect } from 'react';
import { useLocalization } from './context/LocalizationContext';
import { useTheme } from './context/ThemeContext';
import AirExchangeCalculator from './AirExchangeCalculator';
import DuctSizingCalculator from './DuctSizingCalculator';
import DuctAreaCalculator from './DuctAreaCalculator';
import SmokeRemovalCalculator from './SmokeRemovalCalculator';
import PressureDropCalculator from './PressureDropCalculator';
import AcousticCalculator from './AcousticCalculator';
import WaterHeaterCalculator from './WaterHeaterCalculator';
import { Button } from './components/ui';
import './calculators.animations.css';

const CalculatorsHomePage = ({ projects, addSpecToProject }) => {
  const { t } = useLocalization();
  const { theme } = useTheme();
  const [activeCalculator, setActiveCalculator] = useState(null);
  const [showAnimation, setShowAnimation] = useState(true);

  const calculators = [
    {
      id: 'waterHeater',
      name: t('calculators.waterHeater', 'Water Heater Calculator'),
      component: WaterHeaterCalculator,
      icon: '🔥',
      color: theme === 'dark' ? '#dc2626' : '#b91c1c',
      description: t(
        'calculators.waterHeaterDescription',
        'Select a water heater based on power or temperature requirements.'
      ),
    },
    {
      id: 'airExchange',
      name: t('calculators.airExchange'),
      component: AirExchangeCalculator,
      icon: '🔄',
      color: theme === 'dark' ? '#4f46e5' : '#4338ca',
      description: t(
        'calculators.airExchangeDescription',
        'Calculate required air exchange rates for different room types.'
      ),
    },
    {
      id: 'ductSizing',
      name: t('calculators.ductSizing'),
      component: DuctSizingCalculator,
      icon: '📏',
      color: theme === 'dark' ? '#0891b2' : '#0e7490',
      description: t(
        'calculators.ductSizingDescription',
        'Size ventilation ducts based on airflow requirements.'
      ),
    },
    {
      id: 'ductArea',
      name: t('calculators.ductArea', 'Duct Area Calculator'),
      component: DuctAreaCalculator,
      icon: '📐',
      color: theme === 'dark' ? '#059669' : '#047857',
      description: t(
        'calculators.ductAreaDescription',
        'Calculate surface area of ducts and fittings for material estimation.'
      ),
    },
    {
      id: 'smokeRemoval',
      name: t('calculators.smokeRemoval'),
      component: SmokeRemovalCalculator,
      icon: '💨',
      color: theme === 'dark' ? '#7c3aed' : '#6d28d9',
      description: t(
        'calculators.smokeRemovalDescription',
        'Calculate smoke removal requirements for fire safety systems.'
      ),
    },
    {
      id: 'pressureDrop',
      name: t('calculators.pressureDrop'),
      component: PressureDropCalculator,
      icon: '📉',
      color: theme === 'dark' ? '#ea580c' : '#c2410c',
      description: t(
        'calculators.pressureDropDescription',
        'Calculate pressure drop in ventilation systems.'
      ),
    },
    {
      id: 'acoustic',
      name: t('calculators.acoustic'),
      component: AcousticCalculator,
      icon: '🔊',
      color: theme === 'dark' ? '#16a34a' : '#15803d',
      description: t(
        'calculators.acousticDescription',
        'Calculate sound levels and acoustic requirements.'
      ),
    },
  ];

  const handleCalculatorSelect = (calculatorId) => {
    setShowAnimation(false);
    // Small delay for exit animation
    setTimeout(() => {
      setActiveCalculator(calculatorId);
      setShowAnimation(true);
    }, 300);
  };

  const renderActiveCalculator = () => {
    if (!activeCalculator) return null;

    const calculator = calculators.find((calc) => calc.id === activeCalculator);
    if (!calculator) return null;

    const CalculatorComponent = calculator.component;
    return (
      <div
        className={
          showAnimation ? 'section-enter section-enter-active' : 'section-exit section-exit-active'
        }
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1.5rem',
            gap: '0.5rem',
          }}
        >
          <span
            style={{
              fontSize: '1.5rem',
              marginRight: '0.5rem',
            }}
          >
            {calculator.icon}
          </span>
          <h1
            style={{
              margin: 0,
              color: theme === 'dark' ? '#f9fafb' : '#111827',
              fontSize: '1.75rem',
            }}
          >
            {calculator.name}
          </h1>
        </div>
        <CalculatorComponent projects={projects} addSpecToProject={addSpecToProject} />
        <div style={{ textAlign: 'center', margin: '2rem 0' }}>
          <Button
            onClick={() => handleCalculatorSelect(null)}
            variant="secondary"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              margin: '0 auto',
              padding: '0.75rem 1.5rem',
            }}
          >
            <span style={{ fontSize: '1.25rem' }}>←</span>
            {t('common.backToCalculators')}
          </Button>
        </div>
      </div>
    );
  };

  // Effect to handle page title update
  useEffect(() => {
    if (activeCalculator) {
      const calculator = calculators.find((calc) => calc.id === activeCalculator);
      if (calculator) {
        document.title = `Vent.AI - ${calculator.name}`;
      }
    } else {
      document.title = 'Vent.AI - Calculators';
    }

    return () => {
      document.title = 'Vent.AI';
    };
  }, [activeCalculator, calculators]);

  return (
    <div
      className="calculators-home-container"
      style={{
        padding: '2rem 1rem',
        maxWidth: '1400px',
        margin: '0 auto',
      }}
    >
      {!activeCalculator ? (
        <div
          className={
            showAnimation
              ? 'section-enter section-enter-active'
              : 'section-exit section-exit-active'
          }
        >
          <div
            style={{
              textAlign: 'center',
              marginBottom: '3rem',
              animation: 'fadeIn 0.8s ease-out',
            }}
          >
            <h1
              style={{
                margin: '0 0 1rem 0',
                color: theme === 'dark' ? '#f9fafb' : '#111827',
                fontSize: '2.5rem',
              }}
            >
              {t('calculators.title')}
            </h1>
            <p
              style={{
                color: theme === 'dark' ? '#d1d5db' : '#4b5563',
                maxWidth: '800px',
                margin: '0 auto',
                fontSize: '1.1rem',
              }}
            >
              {t('calculators.description')}
            </p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
              gap: '1.5rem',
              maxWidth: '1200px',
              margin: '0 auto',
            }}
          >
            {calculators.map((calculator, index) => (
              <div
                key={calculator.id}
                onClick={() => handleCalculatorSelect(calculator.id)}
                style={{
                  backgroundColor: theme === 'dark' ? '#1f2937' : '#ffffff',
                  color: theme === 'dark' ? '#f9fafb' : '#212529',
                  boxShadow:
                    theme === 'dark'
                      ? '0 8px 30px rgba(0, 0, 0, 0.3)'
                      : '0 8px 30px rgba(0, 0, 0, 0.12)',
                  border: `1px solid ${theme === 'dark' ? '#374151' : '#e9ecef'}`,
                  borderRadius: '12px',
                  padding: '2rem',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  position: 'relative',
                  overflow: 'hidden',
                  animation: `fadeIn ${0.3 + index * 0.1}s ease-out`,
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px)';
                  e.currentTarget.style.boxShadow =
                    theme === 'dark'
                      ? '0 12px 40px rgba(0, 0, 0, 0.4)'
                      : '0 12px 40px rgba(0, 0, 0, 0.15)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow =
                    theme === 'dark'
                      ? '0 8px 30px rgba(0, 0, 0, 0.3)'
                      : '0 8px 30px rgba(0, 0, 0, 0.12)';
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    top: '0',
                    left: '0',
                    width: '8px',
                    height: '100%',
                    backgroundColor: calculator.color,
                    borderTopLeftRadius: '12px',
                    borderBottomLeftRadius: '12px',
                  }}
                ></div>

                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '60px',
                    height: '60px',
                    borderRadius: '50%',
                    backgroundColor: calculator.color + '20', // Adding transparency
                    margin: '0 auto 1.25rem',
                    fontSize: '2rem',
                  }}
                >
                  {calculator.icon}
                </div>

                <h3
                  style={{
                    margin: '0 0 1rem 0',
                    fontSize: '1.25rem',
                    fontWeight: '600',
                  }}
                >
                  {calculator.name}
                </h3>

                <p
                  style={{
                    color: theme === 'dark' ? '#d1d5db' : '#4b5563',
                    margin: '0 0 1.5rem 0',
                    fontSize: '0.95rem',
                    lineHeight: '1.5',
                  }}
                >
                  {t(`calculators.${calculator.id}Description`)}
                </p>

                <div
                  style={{
                    display: 'inline-block',
                    padding: '0.5rem 1rem',
                    borderRadius: '4px',
                    backgroundColor: theme === 'dark' ? '#374151' : '#f3f4f6',
                    color: calculator.color,
                    fontWeight: '500',
                    fontSize: '0.875rem',
                    transition: 'all 0.2s ease',
                  }}
                >
                  {t('common.openCalculator')} →
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        renderActiveCalculator()
      )}
    </div>
  );
};

export default CalculatorsHomePage;
