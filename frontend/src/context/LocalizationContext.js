import React, { createContext, useContext, useState, useEffect } from 'react';
import uaTranslations from '../locales/ua.json';
import enTranslations from '../locales/en.json';

const LocalizationContext = createContext();

const translations = {
  ua: uaTranslations,
  en: enTranslations,
};

export const LocalizationProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    // Отримуємо збережену мову або встановлюємо українську за замовчуванням
    return localStorage.getItem('language') || 'ua';
  });

  useEffect(() => {
    localStorage.setItem('language', language);
    // Встановлюємо атрибут lang для HTML документа
    document.documentElement.lang = language;
  }, [language]);

  const t = (key, interpolations = {}) => {
    const keys = key.split('.');
    let value = translations[language];

    for (const k of keys) {
      value = value?.[k];
    }

    if (typeof value === 'string' && Object.keys(interpolations).length > 0) {
      return Object.keys(interpolations).reduce((str, param) => {
        return str.replace(new RegExp(`{{${param}}}`, 'g'), interpolations[param]);
      }, value);
    }

    return value || key;
  };

  const changeLanguage = (newLanguage) => {
    if (translations[newLanguage]) {
      setLanguage(newLanguage);
    }
  };

  const value = {
    language,
    setLanguage: changeLanguage,
    t,
    isUkrainian: language === 'ua',
    isEnglish: language === 'en',
  };

  return <LocalizationContext.Provider value={value}>{children}</LocalizationContext.Provider>;
};

export const useLocalization = () => {
  const context = useContext(LocalizationContext);
  if (!context) {
    throw new Error('useLocalization must be used within a LocalizationProvider');
  }
  return context;
};
