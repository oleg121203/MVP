import PropTypes from 'prop-types';
import { FaWind, FaThermometerHalf } from 'react-icons/fa';
import DarkModeToggle from './DarkModeToggle';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';

export default function MainLayout({ children }) {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header with thematic elements */}
      <header className="bg-vent-primary text-white p-4 shadow-md">
        <div className="container mx-auto flex items-center">
          <LanguageSwitcher className="mr-4" />
          <DarkModeToggle className="mr-4" />
          <FaWind className="text-3xl mr-3" />
          <h1 className="text-2xl font-bold">{t('appTitle')}</h1>
          <nav className="ml-auto flex space-x-6">
            <a href="/calculator" className="hover:underline flex items-center">
              <FaThermometerHalf className="mr-1" /> {t('calculator')}
            </a>
            <a href="/visualizer" className="hover:underline">
              {t('airflowVisualizer')}
            </a>
          </nav>
        </div>
      </header>

      {/* Main content area with modern design elements */}
      <main className="container mx-auto px-4 py-8 bg-gradient-to-br from-blue-50 to-white">
        <div className="backdrop-blur-sm bg-white/80 rounded-2xl shadow-lg p-8">{children}</div>
      </main>

      {/* Thematic footer */}
      <footer className="bg-gray-800 text-white p-6 mt-12">
        <div className="container mx-auto text-center">
          <p>
            {' '}
            {new Date().getFullYear()} VentAI - {t('precisionHVAC')}
          </p>
        </div>
      </footer>
    </div>
  );
}

MainLayout.propTypes = {
  children: PropTypes.node.isRequired,
};
