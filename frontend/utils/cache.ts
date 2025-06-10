import { useState, useEffect } from 'react';

export const useCachedData = (key: string, fetchFunction: () => Promise<any>, ttl: number = 60000) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cachedData = localStorage.getItem(key);
    if (cachedData) {
      const { data: cached, timestamp } = JSON.parse(cachedData);
      if (Date.now() - timestamp < ttl) {
        setData(cached);
        setLoading(false);
        return;
      }
    }
    fetchFunction().then(result => {
      setData(result);
      localStorage.setItem(key, JSON.stringify({ data: result, timestamp: Date.now() }));
    }).catch(err => setError(err)).finally(() => setLoading(false));
  }, [key, fetchFunction, ttl]);

  return { data, loading, error };
};