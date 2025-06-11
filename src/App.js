import React from 'react';
import { Provider } from 'react-redux';
import store from './redux/store';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProjectAnalyticsDashboard from './components/ProjectAnalyticsDashboard';
import PriceAnalytics from './components/dashboard/PriceAnalytics';
import PredictiveModeling from './components/predictive/PredictiveModeling';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route path="/dashboard" element={<PriceAnalytics />} />
          <Route path="/predictive" element={<PredictiveModeling />} />
          <Route path="/" element={
            <div className="app">
              <ProjectAnalyticsDashboard 
                projectId="PROJ-001" 
                onRefresh={() => window.location.reload()}
              />
            </div>
          } />
          {/* Other routes */}
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
