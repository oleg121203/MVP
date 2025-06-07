import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Temporarily commented out to resolve module not found errors
// import en from './locales/en.json';
// import uk from './locales/uk.json';

// Removed unnecessary type declarations since using direct objects
// declare module "./locales/en.json" {
//   const value: { [key: string]: string };
//   export default value;
// }
// declare module "./locales/uk.json" {
//   const value: { [key: string]: string };
//   export default value;
// }

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          welcome: "Welcome to VentAI",
          home: "Home",
          calculators: "Calculators",
          dashboard: "Dashboard",
          automation: "Automation",
          language: "Language"
        }
      },
      uk: {
        translation: {
          welcome: "Ласкаво просимо до VentAI",
          home: "Головна",
          calculators: "Калькулятори",
          dashboard: "Панель управління",
          automation: "Автоматизація",
          language: "Мова"
        }
      }
    },
    lng: 'en', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
