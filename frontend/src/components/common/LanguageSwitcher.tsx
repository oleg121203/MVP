import React from 'react';
import { Select } from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '../../hooks/useLanguage';

const LanguageSwitcher: React.FC = () => {
  const { t } = useTranslation();
  const { currentLanguage, changeLanguage } = useLanguage();

  const handleLanguageChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    changeLanguage(event.target.value);
  };

  return (
    <Select 
      value={currentLanguage} 
      onChange={handleLanguageChange} 
      size="sm" 
      width="auto"
      aria-label={t('language')}
    >
      <option value="en">English</option>
      <option value="uk">Українська</option>
    </Select>
  );
};

export default LanguageSwitcher;
