import React, { useState } from 'react';
import { useEnhancedWindsurfAI } from '../services/windsurfExactModels';

/**
 * 🌊 Windsurf Models Showcase Component
 * Interactive display of all available Windsurf AI models
 */
const WindsurfModelsShowcase = () => {
  const {
    providers,
    models,
    loading,
    error,
    refreshProviders,
    getFreeModels,
    getReasoningModels,
    getModelsByVendor,
  } = useEnhancedWindsurfAI();

  const [activeTab, setActiveTab] = useState('overview');
  const [selectedVendor, setSelectedVendor] = useState('all');

  // Stats calculations
  const stats = {
    totalProviders: providers?.length || 0,
    totalModels: models?.length || 0,
    freeModels: getFreeModels().length,
    reasoningModels: getReasoningModels().length,
    chatModels: models?.filter(m => m.type === 'chat').length || 0,
  };

  // Filter models by vendor
  const filteredModels = selectedVendor === 'all' 
    ? models 
    : getModelsByVendor(selectedVendor);

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-center mb-4">🌊 Windsurf AI Models Integration</h1>
        <p className="text-xl text-center text-gray-600 mb-6">
          Complete integration with all available Windsurf AI providers and models
        </p>
        
        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-100 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-blue-600">{stats.totalProviders}</div>
            <div className="text-sm text-blue-800">Providers</div>
          </div>
          <div className="bg-green-100 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-green-600">{stats.totalModels}</div>
            <div className="text-sm text-green-800">Total Models</div>
          </div>
          <div className="bg-purple-100 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-purple-600">{stats.freeModels}</div>
            <div className="text-sm text-purple-800">Free Models</div>
          </div>
          <div className="bg-orange-100 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-orange-600">{stats.reasoningModels}</div>
            <div className="text-sm text-orange-800">Reasoning Models</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-4 mb-8">
          <button 
            onClick={refreshProviders}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          ❌ Error: {error}
        </div>
      )}

      {/* Loading Display */}
      {loading && (
        <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-6">
          ⏳ Loading...
        </div>
      )}

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200 mb-6">
        <button 
          className={`px-4 py-2 font-medium ${activeTab === 'overview' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`px-4 py-2 font-medium ${activeTab === 'models' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('models')}
        >
          🤖 Models
        </button>
        <button 
          className={`px-4 py-2 font-medium ${activeTab === 'capabilities' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('capabilities')}
        >
          🎯 Capabilities
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Provider Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {providers?.map(provider => (
                <div key={provider.vendor} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-bold text-gray-800">{provider.name}</h3>
                    <span className={`inline-block w-3 h-3 rounded-full ${
                      provider.available ? 'bg-green-500' : 'bg-red-500'
                    }`}></span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    {provider.models?.length || 0} models available
                  </p>
                  <div className="space-y-2">
                    {provider.models?.slice(0, 3).map((model) => (
                      <div key={model.id} className="text-sm">
                        <span className="font-medium">{model.name}</span>
                        <span className="text-gray-500 ml-2">({model.credits})</span>
                      </div>
                    ))}
                    {provider.models?.length > 3 && (
                      <p className="text-xs text-gray-500">
                        +{provider.models.length - 3} more models...
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Models Tab */}
        {activeTab === 'models' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">All Models ({filteredModels?.length || 0})</h2>
              <select 
                value={selectedVendor} 
                onChange={(e) => setSelectedVendor(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="all">All Vendors</option>
                {providers?.map(p => (
                  <option key={p.vendor} value={p.vendor}>
                    {p.name} ({p.models.length})
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredModels?.map(model => (
                <div key={model.id} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                  <h4 className="font-semibold text-gray-800 mb-2">{model.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">ID: {model.id}</p>
                  
                  <div className="flex flex-wrap gap-2 mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      model.credits === 'free' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {model.credits}
                    </span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      model.type === 'reasoning' 
                        ? 'bg-purple-100 text-purple-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {model.type}
                    </span>
                    <span className="px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                      {model.vendor}
                    </span>
                  </div>

                  {model.family && (
                    <p className="text-xs text-gray-500">Family: {model.family}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Capabilities Tab */}
        {activeTab === 'capabilities' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Model Capabilities</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Free Models */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h3 className="text-xl font-bold text-green-800 mb-4 flex items-center">
                  <span className="text-green-600 mr-2">💚</span>
                  Free Models ({stats.freeModels})
                </h3>
                <div className="space-y-3">
                  {getFreeModels().map((model) => (
                    <div key={model.id} className="bg-white p-3 rounded border border-green-200">
                      <h4 className="font-semibold text-green-700">{model.name}</h4>
                      <p className="text-sm text-gray-600">Vendor: {model.vendor}</p>
                      <p className="text-sm text-gray-600">Type: {model.type}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Reasoning Models */}
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
                <h3 className="text-xl font-bold text-purple-800 mb-4 flex items-center">
                  <span className="text-purple-600 mr-2">🧠</span>
                  Reasoning Models ({stats.reasoningModels})
                </h3>
                <div className="space-y-3">
                  {getReasoningModels().map((model) => (
                    <div key={model.id} className="bg-white p-3 rounded border border-purple-200">
                      <h4 className="font-semibold text-purple-700">{model.name}</h4>
                      <p className="text-sm text-gray-600">Vendor: {model.vendor}</p>
                      <p className="text-sm text-gray-600">Credits: {model.credits}</p>
                      <div className="mt-2">
                        <span className="inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                          Advanced Reasoning
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WindsurfModelsShowcase;
