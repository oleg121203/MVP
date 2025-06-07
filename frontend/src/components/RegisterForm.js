import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function RegisterForm() {
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
      setError('Passwords do not match');
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
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={formData.username} onChange={(e) => setFormData({...formData, username: e.target.value})} />
      <input type="email" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
      <input type="password" value={formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} />
      <input type="password" value={formData.password2} onChange={(e) => setFormData({...formData, password2: e.target.value})} />
      {error && <div className="error">{error}</div>}
      <button type="submit">Register</button>
    </form>
  );
}
