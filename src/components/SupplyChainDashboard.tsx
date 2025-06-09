import React from 'react';
import { SupplyChainItem } from '../types/supplyChain';
import { calculateRisk } from '../services/riskAssessment';
import { SupplyChainVisualization } from './SupplyChainVisualization';

interface SupplyChainDashboardProps {
  items: SupplyChainItem[];
}

export const SupplyChainDashboard: React.FC<SupplyChainDashboardProps> = ({ items }) => {
  return (
    <div className="supply-chain-dashboard">
      <h2>Supply Chain Dashboard</h2>
      
      <SupplyChainVisualization items={items} />
      
      <div className="supply-chain-items">
        {items.map(item => (
          <div key={item.id} className="supply-chain-item">
            <h3>{item.name}</h3>
            <p>Supplier: {item.supplierId}</p>
            <p>Origin: {item.origin}</p>
            <p>Risk Score: {calculateRisk(item).overall.toFixed(1)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
