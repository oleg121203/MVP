import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { io } from 'socket.io-client';

type AlertSeverity = 'low' | 'medium' | 'high';

interface AlertItem {
  timestamp: string;
  message: string;
  severity: AlertSeverity;
}

interface Alert {
  timestamp: Date;
  message: string;
  severity: 'low' | 'medium' | 'high';
}

const getAlertStyle = (severity: AlertSeverity) => {
  switch (severity) {
    case 'high':
      return 'bg-red-100 border-red-500 text-red-800';
    case 'medium':
      return 'bg-yellow-100 border-yellow-500 text-yellow-800';
    default:
      return 'bg-blue-100 border-blue-500 text-blue-800';
  }
};

const AlertPanel = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const socket = io(process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000');
    
    socket.on('connect', () => {
      socket.emit('join-project-room', projectId);
    });

    socket.on('alert', (data: { alerts: Alert[] }) => {
      setAlerts(prev => [...data.alerts, ...prev].slice(0, 50));
      setLoading(false);
    });

    return () => {
      socket.disconnect();
    };
  }, [projectId]);

  if (loading) {
    return (
      <div className="p-4 bg-gray-100 rounded-lg mb-6">
        <h2 className="text-xl font-bold mb-2">Performance Alerts</h2>
        <p>Loading alerts...</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gray-100 rounded-lg mb-6">
      <h2 className="text-xl font-bold mb-4">Performance Alerts</h2>
      
      {alerts.length > 0 ? (
        <div className="space-y-3">
          {alerts.map((alert, index) => (
            <div 
              key={index} 
              className={`p-3 rounded border-l-4 ${getAlertStyle(alert.severity as AlertSeverity)}`}
            >
              <div className="font-semibold">
                {alert.timestamp.toLocaleString()}
              </div>
              <div>{alert.message}</div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-600">No active alerts</p>
      )}
    </div>
  );
};

export default AlertPanel;
