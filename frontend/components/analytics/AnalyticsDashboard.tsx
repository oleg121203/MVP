import React, { useState, useEffect } from 'react';
import { Card, Spin, Alert, Tabs } from 'antd';
import { 
  BarChartOutlined, 
  LineChartOutlined, 
  PieChartOutlined,
  TableOutlined 
} from '@ant-design/icons';

type DashboardData = {
  keyMetrics?: {
    totalLeads: number;
    conversionRate: number;
    avgDealSize: number;
  };
  leadSources?: Array<{ source: string; count: number }>;
  conversionTrends?: Array<{ date: string; rate: number }>;
};

const AnalyticsDashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<DashboardData>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // TODO: Replace with actual API calls
        const mockData: DashboardData = {
          keyMetrics: {
            totalLeads: 1245,
            conversionRate: 0.32,
            avgDealSize: 12500
          },
          leadSources: [
            { source: 'Website', count: 560 },
            { source: 'Referral', count: 320 },
            { source: 'Social', count: 220 },
            { source: 'Other', count: 145 }
          ],
          conversionTrends: Array(30).fill(0).map((_, i) => ({
            date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
            rate: 0.25 + Math.random() * 0.15
          }))
        };
        
        setData(mockData);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <Spin size="large" />;
  if (error) return <Alert message="Error loading dashboard" description={error} type="error" />;

  return (
    <div className="analytics-dashboard">
      <Tabs defaultActiveKey="1">
        <Tabs.TabPane 
          tab={
            <span>
              <BarChartOutlined />
              Key Metrics
            </span>
          } 
          key="1"
        >
          <div className="metrics-grid">
            <Card title="Total Leads" bordered={false}>
              {data.keyMetrics?.totalLeads.toLocaleString()}
            </Card>
            <Card title="Conversion Rate" bordered={false}>
              {(data.keyMetrics?.conversionRate * 100).toFixed(1)}%
            </Card>
            <Card title="Avg. Deal Size" bordered={false}>
              ${data.keyMetrics?.avgDealSize.toLocaleString()}
            </Card>
          </div>
        </Tabs.TabPane>
        
        <Tabs.TabPane 
          tab={
            <span>
              <PieChartOutlined />
              Lead Sources
            </span>
          } 
          key="2"
        >
          {/* TODO: Implement pie chart */}
          <pre>{JSON.stringify(data.leadSources, null, 2)}</pre>
        </Tabs.TabPane>
        
        <Tabs.TabPane 
          tab={
            <span>
              <LineChartOutlined />
              Conversion Trends
            </span>
          } 
          key="3"
        >
          {/* TODO: Implement line chart */}
          <pre>{JSON.stringify(data.conversionTrends, null, 2)}</pre>
        </Tabs.TabPane>
        
        <Tabs.TabPane 
          tab={
            <span>
              <TableOutlined />
              Raw Data
            </span>
          } 
          key="4"
        >
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </Tabs.TabPane>
      </Tabs>
    </div>
  );
};

export default AnalyticsDashboard;
