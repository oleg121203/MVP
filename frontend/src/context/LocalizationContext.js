import React, { createContext, useContext, useEffect, useState } from 'react';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Ukrainian translations
const uk = {
  nav: {
    dashboard: 'Панель управління',
    calculators: 'Калькулятори',
    projects: 'Проекти',
    login: 'Увійти',
    account: 'Обліковий запис',
    logout: 'Вийти',
    marketResearch: 'Дослідження ринку',
    admin: 'Адміністратор'
  },
  footer: {
    rights: 'Усі права захищені.'
  },
  calculators: {
    title: 'HVAC Калькулятори',
    airExchange: 'Розрахунок повітрообміну',
    ductSizing: 'Розмір повітроводів',
    smokeRemoval: 'Розрахунок димовидалення',
    ductArea: 'Площа повітроводів',
    waterHeater: 'Водонагрівач'
  },
  dashboard: {
    title: 'AI Панель управління',
    description: 'Автоматизований аналіз та оптимізація ваших проектів за допомогою AI.',
    loading: 'Завантаження...',
    insights: 'AI Інсайти',
    recentProjects: 'Останні проекти',
    projectName: 'Назва проекту',
    status: 'Статус',
    compliance: 'Відповідність нормам',
    costSavings: 'Економія витрат',
    automationPanel: 'Панель автоматизації',
    automationDescription: 'Увімкніть автоматичні процеси для оптимізації ваших робочих процесів.',
    projectAnalysis: 'Аналіз проектів',
    projectAnalysisDesc: 'Автоматичний аналіз проектів різних форматів для швидкого виявлення проблем.',
    complianceCheck: 'Перевірка відповідності',
    complianceCheckDesc: 'Автоматична перевірка відповідності українським нормам (ДБН).',
    costOptimization: 'Оптимізація витрат',
    costOptimizationDesc: 'AI пропонує рішення для зниження витрат на матеріали та роботи.',
    procurementAutomation: 'Автоматизація закупівель',
    procurementAutomationDesc: 'Оптимізація закупівель з урахуванням локації, часу доставки та вартості.',
    enabled: 'Увімкнено',
    disabled: 'Вимкнено'
  }
};

// English translations
const en = {
  nav: {
    dashboard: 'Dashboard',
    calculators: 'Calculators',
    projects: 'Projects',
    login: 'Login',
    account: 'Account',
    logout: 'Logout',
    marketResearch: 'Market Research',
    admin: 'Admin'
  },
  footer: {
    rights: 'All rights reserved.'
  },
  calculators: {
    title: 'HVAC Calculators',
    airExchange: 'Air Exchange Calculation',
    ductSizing: 'Duct Sizing',
    smokeRemoval: 'Smoke Removal Calculation',
    ductArea: 'Duct Area',
    waterHeater: 'Water Heater'
  },
  dashboard: {
    title: 'AI Dashboard',
    description: 'Automated analysis and optimization of your projects with AI.',
    loading: 'Loading...',
    insights: 'AI Insights',
    recentProjects: 'Recent Projects',
    projectName: 'Project Name',
    status: 'Status',
    compliance: 'Compliance',
    costSavings: 'Cost Savings',
    automationPanel: 'Automation Panel',
    automationDescription: 'Enable automated processes to streamline your workflows.',
    projectAnalysis: 'Project Analysis',
    projectAnalysisDesc: 'Automatic analysis of projects in various formats for quick issue detection.',
    complianceCheck: 'Compliance Check',
    complianceCheckDesc: 'Automated compliance verification with Ukrainian standards (ДБН).',
    costOptimization: 'Cost Optimization',
    costOptimizationDesc: 'AI suggests solutions to reduce costs on materials and labor.',
    procurementAutomation: 'Procurement Automation',
    procurementAutomationDesc: 'Optimized procurement considering location, delivery time, and cost.',
    enabled: 'Enabled',
    disabled: 'Disabled'
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      uk: { translation: uk }
    },
    lng: localStorage.getItem('language') || 'uk',
    fallbackLng: 'uk',
    interpolation: {
      escapeValue: false
    }
  });

const LocalizationContext = createContext();

export const useLocalization = () => useContext(LocalizationContext);

export const LocalizationProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);

  useEffect(() => {
    const handleLanguageChange = (lng) => {
      setCurrentLanguage(lng);
      localStorage.setItem('language', lng);
    };

    i18n.on('languageChanged', handleLanguageChange);

    return () => {
      i18n.off('languageChanged', handleLanguageChange);
    };
  }, []);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <LocalizationContext.Provider value={{ t: i18n.t, language: currentLanguage, changeLanguage }}>
      {children}
    </LocalizationContext.Provider>
  );
};
