import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import ThemeToggle from '../components/ThemeToggle';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import { useToast } from '../context/ToastContext';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const { register, loading, error } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const validatePassword = () => {
    if (password !== confirmPassword) {
      setPasswordError("Passwords don't match");
      toast.error("Passwords don't match");
      return false;
    }
    setPasswordError('');
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validatePassword()) return;

    // Додаткова валідація
    if (!username || username.trim() === '') {
      toast.error('Username is required');
      return;
    }

    if (!email || email.trim() === '') {
      toast.error('Email is required');
      return;
    }

    if (!email.includes('@') || !email.includes('.')) {
      toast.error('Please enter a valid email');
      return;
    }

    console.log('Registration data:', { username, email, password });

    try {
      const success = await register(username, email, password);
      if (success) {
        toast.success('Registration successful!');
        navigate('/projects'); // Redirect to projects after successful registration
      }
    } catch (err) {
      toast.error(error || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-neutral p-4">
      <div className="p-8 max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-neutral dark:text-white">Register</h2>
          <ThemeToggle />
        </div>

        {passwordError && (
          <div className="p-3 mb-4 text-sm rounded-md bg-error/10 border border-error text-error">
            {passwordError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            type="text"
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            required
          />

          <Input
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />

          <Input
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />

          <div className="mb-0">
            <Input
              type="password"
              label="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              error={passwordError}
            />
          </div>

          <Button type="submit" variant="primary" disabled={loading} isLoading={loading}>
            Register
          </Button>

          <p className="mt-4 text-center text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <Link to="/login" className="text-primary dark:text-accent hover:underline">
              Login
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
