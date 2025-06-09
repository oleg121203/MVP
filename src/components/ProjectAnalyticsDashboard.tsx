import React from 'react';
import { Line } from 'react-chartjs-2';
import { ThemeToggle } from './ThemeToggle';
import { AIChatPanel } from './AIChatPanel';
import styles from './ProjectAnalyticsDashboard.module.css';
import { ProjectMetrics } from '../../interfaces/analytics';

type DashboardProps = {
  projectId: string;
  onRefresh: () => void;
};

// Custom chart components
const LineChart = ({ data, title }: { data: any, title: string }) => (
  <div className={styles.chartContainer}>
    <Line data={data} />
    <h4>{title}</h4>
  </div>
);

const ProgressBar = ({ value }: { value: number }) => (
  <div className={styles.progressBar}>
    <div 
      className={styles.progressFill} 
      style={{ width: `${value}%` }}
    />
  </div>
);

const MemoizedLineChart = React.memo(LineChart);
const MemoizedProgressBar = React.memo(ProgressBar);

export const ProjectAnalyticsDashboard: React.FC<DashboardProps> = ({
  projectId,
  onRefresh
}) => {
  const [metrics, setMetrics] = React.useState<ProjectMetrics>();
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string>();
  const [fetchCache, setFetchCache] = React.useState<Record<string, ProjectMetrics>>({});

  const fetchMetrics = async () => {
    setLoading(true);
    setError(undefined);
    
    try {
      if (fetchCache[projectId]) {
        setMetrics(fetchCache[projectId]);
        return;
      }
      
      const response = await fetch(`/api/analytics/${projectId}`);
      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      setFetchCache(prev => ({...prev, [projectId]: data}));
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    fetchMetrics();
  }, [projectId]);

  if (error) return (
    <div className={styles.errorState}>
      <p>Error loading dashboard: {error}</p>
      <button onClick={fetchMetrics}>Retry</button>
    </div>
  );

  if (loading) return <div className={styles.loadingState}>Loading dashboard...</div>;

  const handleAIQuery = async (query: string) => {
    try {
      const response = await fetch(`/api/analytics/${projectId}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      return await response.json();
    } catch (error) {
      return 'Error connecting to analytics service';
    }
  };

  return (
    <div className={styles.dashboardContainer}>
      <div className={styles.header}>
        <h2 className={styles.title}>Project Analytics: {projectId}</h2>
        <ThemeToggle />
      </div>
      
      {/* Metrics Overview */}
      <div className={styles.metricsOverview}>
        <div className={styles.metricCard}>
          <h3>Cost Analysis</h3>
          <p>${metrics?.costAnalysis?.totalCost?.toFixed(2) || 'Loading...'}</p>
          {metrics?.costAnalysis && (
            <MemoizedLineChart 
              data={metrics.costAnalysis.weeklyTrend}
              title="Weekly Cost Trend"
            />
          )}
        </div>
        
        <div className={styles.metricCard}>
          <h3>Timeline</h3>
          <p>{metrics?.timelineMetrics?.completionPercentage}% Complete</p>
          <MemoizedProgressBar 
            value={metrics?.timelineMetrics?.completionPercentage || 0}
          />
        </div>
        
        {/* Additional metrics will be added here */}
      </div>
      
      <button onClick={onRefresh}>Refresh Data</button>
      <AIChatPanel 
        projectId={projectId}
        onSendQuery={handleAIQuery}
      />
    </div>
  );
};

export default ProjectAnalyticsDashboard;
