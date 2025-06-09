import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AnalyticsPage from './pages/AnalyticsPage';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/analytics/:projectId" element={<AnalyticsPage />} />
        {/* Add other routes here as needed */}
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
