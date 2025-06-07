import { useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import logo from '../assets/logo.svg';

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

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Тут буде логіка відправки запиту на скидання пароля
    setMessage('Інструкції зі скидання пароля відправлено на вашу електронну пошту');
  };

  return (
    <FormContainer>
      <Logo src={logo} alt="Логотип" />
      <h2>Відновлення пароля</h2>

      {message && <div style={{ color: 'green' }}>{message}</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Ваш email"
          required
          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '1rem',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '16px'
          }}
        />

        <button
          type="submit"
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#4a76a8',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            cursor: 'pointer'
          }}
        >
          Надіслати інструкції
        </button>
      </form>

      <div style={{ marginTop: '1rem' }}>
        <Link to="/login">Повернутися до входу</Link>
      </div>
    </FormContainer>
  );
}
