import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProjectAnalyticsPage from './pages/ProjectAnalyticsPage';

// Other imports as needed for other pages

function App() {
  return (
    <Router>
      <Routes>
        {/* Add route for project analytics page */}
        <Route path="/project/:projectId/analytics" element={<ProjectAnalyticsPage />} />
        {/* Other routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
