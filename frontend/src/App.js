import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import CalculatorsPage from './pages/CalculatorsPage';
import DashboardPage from './pages/DashboardPage';
import AIDashboard from './pages/AIDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<HomePage />} />
          <Route path="calculators" element={<CalculatorsPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="ai-dashboard" element={<AIDashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
