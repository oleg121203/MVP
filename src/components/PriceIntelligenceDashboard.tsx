import React from 'react';
import { useAppSelector } from '../store/hooks';

interface Product {
  id: number;
  name: string;
  price: number;
}

const PriceIntelligenceDashboard = () => {
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [data, setData] = React.useState<Product[]>([]);

  React.useEffect(() => {
    // TODO: Replace with actual API call
    setTimeout(() => {
      setLoading(false);
      setData([{ id: 1, name: 'Product 1', price: 100 }, { id: 2, name: 'Product 2', price: 200 }]);
    }, 1000);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Price Intelligence Dashboard</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceIntelligenceDashboard;
