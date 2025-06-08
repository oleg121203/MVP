import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useLoading } from '../context/LoadingContext';
import { useTranslation } from 'react-i18next';

interface LoginFormProps {}

export const LoginForm: React.FC<LoginFormProps> = () => {
  const { t } = useTranslation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const { withLoading } = useLoading();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setError(t('auth.login.requiredError'));
      return;
    }

    try {
      await withLoading(() => login(username, password));
    } catch (err) {
      setError(err instanceof Error ? err.message : t('auth.login.loginFailed'));
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">{t('auth.login.title')}</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="username">
            {t('auth.login.username')}
          </label>
          <input
            id="username"
            type="text"
            className="w-full px-3 py-2 border rounded-md"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 mb-2" htmlFor="password">
            {t('auth.login.password')}
          </label>
          <input
            id="password"
            type="password"
            className="w-full px-3 py-2 border rounded-md"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors"
        >
          {t('auth.login.submit')}
        </button>
      </form>
    </div>
  );
};
