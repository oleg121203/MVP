import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';

export default function RegisterForm() {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password2) {
      setError(t('auth.register.passwordMismatch'));
      return;
    }
    try {
      await api.post('/auth/register/', {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || t('auth.register.registrationFailed'));
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">{t('auth.register.title')}</h2>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="username">
            {t('auth.register.username')}
          </label>
          <input 
            id="username"
            type="text" 
            className="w-full px-3 py-2 border rounded-md"
            value={formData.username} 
            onChange={(e) => setFormData({...formData, username: e.target.value})} 
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="email">
            {t('auth.register.email')}
          </label>
          <input 
            id="email"
            type="email" 
            className="w-full px-3 py-2 border rounded-md"
            value={formData.email} 
            onChange={(e) => setFormData({...formData, email: e.target.value})} 
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="password">
            {t('auth.register.password')}
          </label>
          <input 
            id="password"
            type="password" 
            className="w-full px-3 py-2 border rounded-md"
            value={formData.password} 
            onChange={(e) => setFormData({...formData, password: e.target.value})} 
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 mb-2" htmlFor="password2">
            {t('auth.register.passwordConfirm')}
          </label>
          <input 
            id="password2"
            type="password" 
            className="w-full px-3 py-2 border rounded-md"
            value={formData.password2} 
            onChange={(e) => setFormData({...formData, password2: e.target.value})} 
            required
          />
        </div>
        <button 
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600"
        >
          {t('auth.register.submit')}
        </button>
      </form>
    </div>
  );
}
