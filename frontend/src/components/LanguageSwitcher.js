import React from 'react';
import { useLocalization } from '../context/LocalizationContext';
import './LanguageSwitcher.css';

const LanguageSwitcher = () => {
  const { language, setLanguage } = useLocalization();

  return (
    <div className="language-switcher">
      <button
        className={`lang-btn ${language === 'ua' ? 'active' : ''}`}
        onClick={() => setLanguage('ua')}
        title="Українська"
      >
        🇺🇦 УКР
      </button>
      <button
        className={`lang-btn ${language === 'en' ? 'active' : ''}`}
        onClick={() => setLanguage('en')}
        title="English"
      >
        🇬🇧 ENG
      </button>
    </div>
  );
};

export default LanguageSwitcher;
