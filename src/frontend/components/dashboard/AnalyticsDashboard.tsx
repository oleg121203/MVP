import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setAnalyticsData, setLoading } from '../../store/analyticsSlice';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import type { ProjectAnalytics } from '../../interfaces/analytics';

Chart.register(...registerables);

const AnalyticsDashboard = ({ projectId }: { projectId: string }) => {
  const dispatch = useDispatch();
  const { data, loading } = useSelector((state: any) => state.analytics);

  useEffect(() => {
    const loadData = async () => {
      dispatch(setLoading(true));
      try {
        // WebSocket connection would be established here
        const mockData: ProjectAnalytics = {
          completionRate: { value: 0.75, trend: 'up', lastUpdated: new Date().toISOString() },
          budgetUtilization: { value: 0.65, trend: 'stable', lastUpdated: new Date().toISOString() },
          timeEfficiency: { value: 1.2, trend: 'down', lastUpdated: new Date().toISOString() },
          insights: ['Project is on track', 'Consider optimizing task allocation']
        };
        dispatch(setAnalyticsData(mockData));
      } catch (err) {
        dispatch(setError(err.message));
      } finally {
        dispatch(setLoading(false));
      }
    };

    loadData();
  }, [projectId, dispatch]);

  if (loading) return <div>Loading analytics...</div>;
  if (!data) return <div>No analytics data available</div>;

  return (
    <div className="dashboard-container">
      {/* Dashboard implementation would go here */}
    </div>
  );
};

export default AnalyticsDashboard;