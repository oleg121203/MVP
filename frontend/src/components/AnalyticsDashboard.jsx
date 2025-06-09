import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import AIChatInterface from './AIChatInterface';
import AlertPanel from './AlertPanel';
import { connectToProjectRoom, disconnectFromServer } from '../utils/socket';

const AnalyticsDashboard = () => {
  const { projectId } = useParams();
  const [metrics, setMetrics] = useState({
    costAnalysis: {},
    timelineMetrics: {},
    qualityMetrics: {},
    sustainabilityMetrics: {}
  });
  const [trends, setTrends] = useState([]);
  const [optimizationOpportunities, setOptimizationOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = "http://localhost:8000/api/analytics";

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const metricsRes = await axios.get(`${API_BASE_URL}/project/${projectId}/metrics`);
        setMetrics(metricsRes.data);
        setOptimizationOpportunities(metricsRes.data.costAnalysis?.optimizationOpportunities || []);

        const trendsRes = await axios.get(`${API_BASE_URL}/project/${projectId}/trends?days=30`);
        const trendData = trendsRes.data.dates.map((date, index) => ({
          date,
          energyEfficiency: trendsRes.data.energy_efficiency[index],
          timeToCompletion: trendsRes.data.time_to_completion[index],
          complianceScore: trendsRes.data.compliance_score[index]
        }));
        setTrends(trendData);

        setLoading(false);
      } catch (error) {
        console.error("Error fetching analytics data:", error);
        setLoading(false);
      }
    };

    fetchAnalytics();

    connectToProjectRoom(projectId, (data) => {
      if (data.type === 'metrics') {
        setMetrics(data.data);
        setOptimizationOpportunities(data.data.costAnalysis?.optimizationOpportunities || []);
      } else if (data.type === 'trends') {
        setTrends(data.data);
      }
    });

    return () => {
      disconnectFromServer();
    };
  }, [projectId]);

  if (loading) {
    return <div className="flex justify-center p-6"><div className="text-xl">Loading...</div></div>;
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Project Analytics Dashboard</h1>

      {/* Alert Panel */}
      <div className="dashboard">
        <div className="alerts-section">
          <h2>Real-time Alerts</h2>
          <AlertPanel projectId={projectId} />
        </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <Card>
          <CardHeader><CardTitle>Project Progress</CardTitle></CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.timelineMetrics?.currentProgress || 'N/A'}%</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Compliance Score</CardTitle></CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.qualityMetrics?.complianceScore || 'N/A'}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Carbon Footprint</CardTitle></CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.sustainabilityMetrics?.carbonFootprint || 'N/A'} kgCO2</div>
          </CardContent>
        </Card>
        <div className="md:col-span-2 lg:col-span-1 h-96 md:h-auto">
          <AIChatInterface />
        </div>
      </div>

      {/* Optimization Opportunities */}
      {optimizationOpportunities.length > 0 && (
        <Card className="mb-6">
          <CardHeader><CardTitle>Optimization Opportunities</CardTitle></CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={optimizationOpportunities}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`$${value}`, 'Potential Savings']} />
                  <Legend />
                  <Bar dataKey="potentialSavings" fill="#8884d8" name="Potential Savings" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Risk Assessment */}
      {metrics.timelineMetrics?.riskAssessment && (
        <Card className="mb-6">
          <CardHeader><CardTitle>Risk Assessment</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-red-100 p-4 rounded-lg">
                <h3 className="font-bold">High Risk</h3>
                <p className="text-2xl">{metrics.timelineMetrics.riskAssessment.highRiskItems}</p>
              </div>
              <div className="bg-yellow-100 p-4 rounded-lg">
                <h3 className="font-bold">Medium Risk</h3>
                <p className="text-2xl">{metrics.timelineMetrics.riskAssessment.mediumRiskItems}</p>
              </div>
              <div className="bg-green-100 p-4 rounded-lg">
                <h3 className="font-bold">Low Risk</h3>
                <p className="text-2xl">{metrics.timelineMetrics.riskAssessment.lowRiskItems}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Performance Trends */}
      <Card className="mb-6">
        <CardHeader><CardTitle>Performance Trends (Last 30 Days)</CardTitle></CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="energyEfficiency" stroke="#8884d8" name="Energy Efficiency" />
                <Line yAxisId="right" type="monotone" dataKey="complianceScore" stroke="#ffc658" name="Compliance Score" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AnalyticsDashboard;
