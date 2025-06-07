import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../services/auth';
import styled from 'styled-components';
import logo from '../assets/logo.svg'; // Додайте логотип у цю папку

const FormContainer = styled.div`
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
`;

const Logo = styled.img`
  width: 120px;
  margin-bottom: 1.5rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  margin: 1rem 0;
  label {
    margin-left: 8px;
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 12px;
  background-color: #4a76a8;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  &:hover {
    background-color: #3a5f8a;
  }
`;

const LinksContainer = styled.div`
  margin-top: 1rem;
  a {
    color: #4a76a8;
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
`;

const Error = styled.div`
  color: #ff3333;
  margin-bottom: 1rem;
  padding: 8px;
  background-color: #ffeeee;
  border-radius: 4px;
`;

export default function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    rememberMe: false
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(formData.username, formData.password);
      if (formData.rememberMe) {
        localStorage.setItem('rememberMe', 'true');
      } else {
        localStorage.removeItem('rememberMe');
      }
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Невірний логін або пароль');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormContainer>
      <Logo src={logo} alt="Логотип" />
      <h2>Вхід в систему</h2>
      {error && <Error>{error}</Error>}

      <form onSubmit={handleSubmit}>
        <Input
          type="text"
          value={formData.username}
          onChange={(e) => setFormData({...formData, username: e.target.value})}
          placeholder="Логін"
          required
        />

        <Input
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          placeholder="Пароль"
          required
        />

        <CheckboxContainer>
          <input
            type="checkbox"
            id="rememberMe"
            checked={formData.rememberMe}
            onChange={(e) => setFormData({...formData, rememberMe: e.target.checked})}
          />
          <label htmlFor="rememberMe">Запам'ятати мене</label>
        </CheckboxContainer>

        <Button type="submit" disabled={loading}>
          {loading ? 'Завантаження...' : 'Увійти'}
        </Button>
      </form>

      <LinksContainer>
        <Link to="/forgot-password">Забули пароль?</Link>
      </LinksContainer>
    </FormContainer>
  );
}
