import React from 'react';
import { SupplyChainDashboard } from './components/SupplyChainDashboard';
import { SupplyChainItem } from './types/supplyChain';

function App() {
  const supplyChainItems: SupplyChainItem[] = [
    {
      id: '1',
      name: 'HVAC Unit',
      supplierId: 'supplier-123',
      origin: 'Germany',
      leadTime: 30,
      cost: 2500,
      sustainabilityScore: 85,
      criticality: 'high'
    },
    {
      id: '2',
      name: 'Thermostat',
      supplierId: 'supplier-456',
      origin: 'China',
      leadTime: 45,
      cost: 120,
      sustainabilityScore: 70,
      criticality: 'medium'
    }
  ];

  return (
    <div className="App">
      <SupplyChainDashboard items={supplyChainItems} />
    </div>
  );
}

export default App;
