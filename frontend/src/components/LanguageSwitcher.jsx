import { useTranslation } from 'react-i18next';

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();

  return (
    <select
      value={i18n.language}
      onChange={(e) => i18n.changeLanguage(e.target.value)}
      className="bg-white dark:bg-dark-card p-1 rounded border border-gray-300"
    >
      <option value="en">English</option>
      <option value="uk">Українська</option>
    </select>
  );
}
