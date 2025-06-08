// Розширений AI Dashboard для проектного аналізу
// filepath: /workspaces/MVP/frontend/src/pages/AIProjectDashboard.jsx

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import VentAIService from '../services/aiService';

// UI Components
import { Card, Button, Input, Select, Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/react';

const AIProjectDashboard = ({ projects = [] }) => {
  const { t } = useTranslation();
  const [aiService] = useState(() => new VentAIService());
  
  // State Management
  const [selectedProject, setSelectedProject] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [comparisonResults, setComparisonResults] = useState(null);
  const [optimizationResults, setOptimizationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  // Analysis Options
  const [analysisOptions, setAnalysisOptions] = useState({
    includeCompliance: true,
    includeCostOptimization: true,
    includeEfficiencyAnalysis: true,
    includeRiskAssessment: true,
    comparisonProjects: []
  });

  useEffect(() => {
    if (projects.length > 0 && !selectedProject) {
      setSelectedProject(projects[0]);
    }
  }, [projects, selectedProject]);

  // Comprehensive Project Analysis
  const runProjectAnalysis = async () => {
    if (!selectedProject) return;

    setLoading(true);
    try {
      const projectData = {
        id: selectedProject.id,
        name: selectedProject.name,
        specifications: selectedProject.specifications || [],
        calculationResults: selectedProject.calculationResults || {},
        materials: selectedProject.materials || [],
        timeline: selectedProject.timeline || {},
        budget: selectedProject.budget || {}
      };

      const comparisonData = analysisOptions.comparisonProjects
        .map(pid => projects.find(p => p.id === pid))
        .filter(Boolean);

      const analysis = await aiService.analyzeProject(projectData, comparisonData);

      if (analysis.success) {
        setAnalysisResults(analysis.project_analysis);
        setComparisonResults(analysis.comparisons);
      }
    } catch (error) {
      console.error('Project Analysis Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Cost and Material Optimization
  const runCostOptimization = async () => {
    if (!selectedProject) return;

    setLoading(true);
    try {
      const optimization = await aiService.optimizePricesAndMaterials({
        project: selectedProject,
        preferences: {
          budgetRange: [selectedProject.budget?.min || 10000, selectedProject.budget?.max || 100000],
          qualityPriority: 'high',
          deliveryTime: 'standard',
          sustainability: true
        }
      });

      if (optimization.success) {
        setOptimizationResults(optimization);
      }
    } catch (error) {
      console.error('Cost Optimization Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // HVAC System Analysis
  const runHVACAnalysis = async () => {
    if (!selectedProject) return;

    setLoading(true);
    try {
      const hvacData = {
        project_id: selectedProject.id,
        area: selectedProject.area || 1000,
        occupancy: selectedProject.occupancy || 50,
        climate_zone: 'Ukraine',
        current_systems: selectedProject.hvacSystems || [],
        requirements: selectedProject.requirements || {}
      };

      const hvacAnalysis = await aiService.analyzeHVAC(hvacData);

      if (hvacAnalysis.success) {
        setAnalysisResults(prev => ({
          ...prev,
          hvac_analysis: hvacAnalysis.analysis,
          hvac_recommendations: hvacAnalysis.recommendations,
          efficiency_score: hvacAnalysis.efficiency_score
        }));
      }
    } catch (error) {
      console.error('HVAC Analysis Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-project-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          🤖 AI Аналіз Проектів
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          Комплексний аналіз та оптимізація HVAC проектів з використанням штучного інтелекту
        </p>
      </div>

      {/* Project Selection */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold mb-4">Вибір проекту</h2>
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium mb-2">Проект для аналізу:</label>
            <Select
              value={selectedProject?.id || ''}
              onChange={(e) => {
                const project = projects.find(p => p.id === e.target.value);
                setSelectedProject(project);
              }}
            >
              {projects.map(project => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </Select>
          </div>
          
          <div className="flex gap-2">
            <Button 
              colorScheme="blue" 
              onClick={runProjectAnalysis}
              isLoading={loading}
              loadingText="Аналізуємо..."
            >
              📊 Аналізувати
            </Button>
            <Button 
              colorScheme="green" 
              onClick={runCostOptimization}
              isLoading={loading}
              loadingText="Оптимізуємо..."
            >
              💰 Оптимізувати
            </Button>
            <Button 
              colorScheme="purple" 
              onClick={runHVACAnalysis}
              isLoading={loading}
              loadingText="Аналізуємо HVAC..."
            >
              🔥 HVAC Аналіз
            </Button>
          </div>
        </div>
      </Card>

      {/* Analysis Options */}
      <Card className="mb-6 p-6">
        <h2 className="text-xl font-semibold mb-4">Налаштування аналізу</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={analysisOptions.includeCompliance}
              onChange={(e) => setAnalysisOptions(prev => ({
                ...prev,
                includeCompliance: e.target.checked
              }))}
              className="mr-2"
            />
            Перевірка відповідності
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={analysisOptions.includeCostOptimization}
              onChange={(e) => setAnalysisOptions(prev => ({
                ...prev,
                includeCostOptimization: e.target.checked
              }))}
              className="mr-2"
            />
            Оптимізація вартості
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={analysisOptions.includeEfficiencyAnalysis}
              onChange={(e) => setAnalysisOptions(prev => ({
                ...prev,
                includeEfficiencyAnalysis: e.target.checked
              }))}
              className="mr-2"
            />
            Аналіз ефективності
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={analysisOptions.includeRiskAssessment}
              onChange={(e) => setAnalysisOptions(prev => ({
                ...prev,
                includeRiskAssessment: e.target.checked
              }))}
              className="mr-2"
            />
            Оцінка ризиків
          </label>
        </div>
      </Card>

      {/* Results Tabs */}
      {(analysisResults || comparisonResults || optimizationResults) && (
        <Tabs index={activeTab} onChange={setActiveTab}>
          <TabList>
            <Tab>📊 Аналіз проекту</Tab>
            <Tab>💰 Оптимізація</Tab>
            <Tab>📈 Порівняння</Tab>
            <Tab>🔥 HVAC Система</Tab>
          </TabList>

          <TabPanels>
            {/* Project Analysis Results */}
            <TabPanel>
              {analysisResults && (
                <div className="space-y-6">
                  {/* Complexity Score */}
                  <Card className="p-6">
                    <h3 className="text-lg font-semibold mb-4">Оцінка складності проекту</h3>
                    <div className="flex items-center mb-4">
                      <div className="w-full bg-gray-200 rounded-full h-4 mr-4">
                        <div 
                          className="bg-blue-600 h-4 rounded-full transition-all duration-300"
                          style={{ width: `${analysisResults.complexity_score * 10}%` }}
                        ></div>
                      </div>
                      <span className="text-lg font-bold">
                        {analysisResults.complexity_score}/10
                      </span>
                    </div>
                  </Card>

                  {/* Risk Assessment */}
                  {analysisResults.risk_assessment && (
                    <Card className="p-6">
                      <h3 className="text-lg font-semibold mb-4">⚠️ Оцінка ризиків</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {Object.entries(analysisResults.risk_assessment).map(([risk, level]) => (
                          <div key={risk} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                            <span className="capitalize">{risk.replace('_', ' ')}</span>
                            <span className={`px-2 py-1 rounded text-sm font-medium ${
                              level === 'high' ? 'bg-red-100 text-red-800' :
                              level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {level}
                            </span>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}

                  {/* Compliance Check */}
                  {analysisResults.compliance_check && (
                    <Card className="p-6">
                      <h3 className="text-lg font-semibold mb-4">📋 Відповідність стандартам</h3>
                      <div className="space-y-2">
                        {Object.entries(analysisResults.compliance_check).map(([standard, compliant]) => (
                          <div key={standard} className="flex justify-between items-center p-2 border rounded">
                            <span>{standard}</span>
                            <span className={`px-2 py-1 rounded text-sm ${
                              compliant ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {compliant ? '✅ Відповідає' : '❌ Не відповідає'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}
                </div>
              )}
            </TabPanel>

            {/* Optimization Results */}
            <TabPanel>
              {optimizationResults && (
                <div className="space-y-6">
                  <Card className="p-6">
                    <h3 className="text-lg font-semibold mb-4">💰 Потенціал економії</h3>
                    <div className="text-3xl font-bold text-green-600 mb-2">
                      {optimizationResults.savings_potential}%
                    </div>
                    <p className="text-gray-600">
                      Можлива економія від оптимізації матеріалів та постачальників
                    </p>
                  </Card>

                  {/* Material Alternatives */}
                  {optimizationResults.material_alternatives && (
                    <Card className="p-6">
                      <h3 className="text-lg font-semibold mb-4">🔄 Альтернативні матеріали</h3>
                      <div className="space-y-4">
                        {optimizationResults.material_alternatives.map((alt, index) => (
                          <div key={index} className="border rounded p-4">
                            <div className="flex justify-between items-start mb-2">
                              <h4 className="font-medium">{alt.material_name}</h4>
                              <span className="text-green-600 font-bold">
                                -{alt.savings_percentage}%
                              </span>
                            </div>
                            <div className="text-sm text-gray-600 space-y-1">
                              <p>Якість: {alt.quality_rating}/10</p>
                              <p>Економія: {alt.savings_amount} ₴</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}
                </div>
              )}
            </TabPanel>

            {/* Comparison Results */}
            <TabPanel>
              {comparisonResults && (
                <div className="space-y-6">
                  <Card className="p-6">
                    <h3 className="text-lg font-semibold mb-4">📈 Порівняння з іншими проектами</h3>
                    <div className="space-y-4">
                      {comparisonResults.map((comparison, index) => (
                        <div key={index} className="border rounded p-4">
                          <h4 className="font-medium mb-2">{comparison.project_name}</h4>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <span className="text-gray-500">Вартість:</span>
                              <div className="font-medium">{comparison.cost_difference}</div>
                            </div>
                            <div>
                              <span className="text-gray-500">Ефективність:</span>
                              <div className="font-medium">{comparison.efficiency_difference}</div>
                            </div>
                            <div>
                              <span className="text-gray-500">Терміни:</span>
                              <div className="font-medium">{comparison.timeline_difference}</div>
                            </div>
                            <div>
                              <span className="text-gray-500">Складність:</span>
                              <div className="font-medium">{comparison.complexity_difference}</div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
                </div>
              )}
            </TabPanel>

            {/* HVAC Analysis */}
            <TabPanel>
              {analysisResults?.hvac_analysis && (
                <div className="space-y-6">
                  <Card className="p-6">
                    <h3 className="text-lg font-semibold mb-4">🔥 Аналіз HVAC системи</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-medium mb-2">Ефективність системи</h4>
                        <div className="text-2xl font-bold text-blue-600">
                          {analysisResults.efficiency_score}/100
                        </div>
                      </div>
                      <div>
                        <h4 className="font-medium mb-2">Рекомендації</h4>
                        <ul className="space-y-1 text-sm">
                          {analysisResults.hvac_recommendations?.map((rec, index) => (
                            <li key={index} className="flex items-start">
                              <span className="text-blue-500 mr-2">•</span>
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </Card>
                </div>
              )}
            </TabPanel>
          </TabPanels>
        </Tabs>
      )}
    </div>
  );
};

export default AIProjectDashboard;
