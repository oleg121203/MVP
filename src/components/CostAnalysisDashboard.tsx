import React from 'react';
import { useAppSelector } from '../store/hooks';
import { LineChart, BarChart } from './charts';

type Props = {
  supplierId?: string;
  competitorId?: string;
};

export const CostAnalysisDashboard: React.FC<Props> = ({ supplierId, competitorId }) => {
  const { priceData, loading, error } = useAppSelector(state => state.priceAnalysis);

  if (loading) return <div>Loading cost analysis...</div>;
  if (error) return <div>Error loading data: {error}</div>;

  return (
    <div className="cost-analysis-container">
      <div className="price-trend-section">
        <h3>Price Trends</h3>
        <LineChart 
          data={priceData.trends} 
          xField="date" 
          yField="price"
        />
      </div>
      
      <div className="comparison-section">
        <h3>Cost Comparison</h3>
        <BarChart 
          data={priceData.comparisons} 
          xField="name" 
          yField="value"
        />
      </div>
    </div>
  );
};
