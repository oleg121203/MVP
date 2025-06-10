import React, { useState, useEffect } from 'react';
import { useEnhancedWindsurfAI } from '../services/windsurfExactModels';
import './WindsurfModelsShowcase.css';

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
    chatWithAI,
    selectBestModel,
    getFreeModels,
    getReasoningModels,
    getModelsByVendor,
    getModelRecommendations,
    demoAllModels,
    service
  } = useEnhancedWindsurfAI();

  const [activeTab, setActiveTab] = useState('overview');
  const [testMessage, setTestMessage] = useState('Hello! Can you briefly introduce yourself?');
  const [testResults, setTestResults] = useState([]);
  const [selectedVendor, setSelectedVendor] = useState('all');
  const [chatHistory, setChatHistory] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');

  // Stats calculations
  const stats = {
    totalProviders: providers?.length || 0,
    totalModels: models?.length || 0,
    freeModels: getFreeModels().length,
    reasoningModels: getReasoningModels().length,
    chatModels: models?.filter(m => m.type === 'chat').length || 0,
    vendorStats: service?.getProviderStats() || []
  };

  // Handle model testing
  const handleTestAllModels = async () => {
    try {
      const results = await demoAllModels(testMessage);
      setTestResults(results);
      setActiveTab('testing');
    } catch (err) {
      console.error('Testing failed:', err);
    }
  };

  // Handle single model chat
  const handleSingleChat = async (modelId, message) => {
    try {
      const result = await chatWithAI(message, { modelId });
      const newEntry = {
        id: Date.now(),
        modelId,
        modelName: models.find(m => m.id === modelId)?.name || 'Unknown',
        vendor: models.find(m => m.id === modelId)?.vendor || 'Unknown',
        message,
        response: result.content?.[0]?.text || 'No response',
        timestamp: new Date().toLocaleTimeString()
      };
      setChatHistory(prev => [newEntry, ...prev]);
    } catch (err) {
      console.error('Chat failed:', err);
    }
  };

  // Filter models by vendor
  const filteredModels = selectedVendor === 'all' 
    ? models 
    : getModelsByVendor(selectedVendor);

  // Render model card
  const ModelCard = ({ model }) => (
    <div className="model-card" key={model.id}>
      <div className="model-header">
        <h4>{model.name}</h4>
        <div className="model-badges">
          <span className={`badge badge-${model.type}`}>{model.type}</span>
          <span className={`badge badge-${model.credits === 'free' ? 'free' : 'premium'}`}>
            {model.credits === 'free' ? 'FREE' : model.credits}
          </span>
          <span className="badge badge-vendor">{model.vendor}</span>
        </div>
      </div>
      
      <div className="model-details">
        <p>{model.description}</p>
        <div className="model-specs">
          <div>🧠 Context: {model.context_window?.toLocaleString() || 'N/A'}</div>
          <div>💰 Credits: {model.credits}</div>
          <div>🏢 Provider: {model.providerName}</div>
        </div>
      </div>

      <div className="model-actions">
        <button 
          onClick={() => handleSingleChat(model.id, currentMessage || 'Hello!')}
          disabled={loading}
          className="btn btn-primary"
        >
          Test Chat
        </button>
        <button 
          onClick={() => {
            const best = selectBestModel('coding');
            if (best.id === model.id) {
              alert('This is already the best model for coding!');
            } else {
              alert(`Best for coding: ${best.name}`);
            }
          }}
          className="btn btn-secondary"
        >
          Compare
        </button>
      </div>
    </div>
  );

  // Render provider overview
  const ProviderOverview = ({ provider }) => (
    <div className="provider-card" key={provider.vendor}>
      <div className="provider-header">
        <h3>{provider.name}</h3>
        <span className={`status ${provider.available ? 'available' : 'unavailable'}`}>
          {provider.available ? '✅ Available' : '❌ Unavailable'}
        </span>
      </div>
      
      <div className="provider-stats">
        <div>📊 Models: {provider.models.length}</div>
        <div>💎 Free: {provider.models.filter(m => m.credits === 'free').length}</div>
        <div>🧠 Reasoning: {provider.models.filter(m => m.type === 'reasoning').length}</div>
        <div>💬 Chat: {provider.models.filter(m => m.type === 'chat').length}</div>
      </div>

      <div className="provider-models">
        {provider.models.map(model => (
          <div key={model.id} className="mini-model">
            <span className="model-name">{model.name}</span>
            <span className={`model-credit ${model.credits === 'free' ? 'free' : 'premium'}`}>
              {model.credits}
            </span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="windsurf-showcase">
      <div className="showcase-header">
        <h1>🌊 Windsurf AI Models Integration</h1>
        <p>Complete integration with all available Windsurf AI providers and models</p>
        
        <div className="header-stats">
          <div className="stat-card">
            <div className="stat-number">{stats.totalProviders}</div>
            <div className="stat-label">Providers</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.totalModels}</div>
            <div className="stat-label">Models</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.freeModels}</div>
            <div className="stat-label">Free</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{stats.reasoningModels}</div>
            <div className="stat-label">Reasoning</div>
          </div>
        </div>

        <div className="header-actions">
          <button 
            onClick={refreshProviders}
            disabled={loading}
            className="btn btn-refresh"
          >
            🔄 Refresh
          </button>
          <button 
            onClick={handleTestAllModels}
            disabled={loading}
            className="btn btn-test"
          >
            🧪 Test All
          </button>
        </div>
      </div>

      <div className="showcase-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`tab ${activeTab === 'models' ? 'active' : ''}`}
          onClick={() => setActiveTab('models')}
        >
          🤖 Models
        </button>
        <button 
          className={`tab ${activeTab === 'testing' ? 'active' : ''}`}
          onClick={() => setActiveTab('testing')}
        >
          🧪 Testing
        </button>
        <button 
          className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button 
          className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          🎯 Smart Select
        </button>
      </div>

      <div className="showcase-content">
        {error && (
          <div className="error-message">
            ❌ Error: {error}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            ⏳ Loading...
          </div>
        )}

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <h2>Provider Overview</h2>
            <div className="providers-grid">
              {providers?.map(provider => (
                <ProviderOverview key={provider.vendor} provider={provider} />
              ))}
            </div>

            <div className="capabilities-section">
              <h3>Model Capabilities</h3>
              <div className="capabilities-grid">
                <div className="capability-card">
                  <h4>💬 Chat Models ({stats.chatModels})</h4>
                  <p>General conversation and assistance</p>
                  <div className="model-list">
                    {models?.filter(m => m.type === 'chat').map(m => (
                      <span key={m.id} className="model-tag">{m.name}</span>
                    ))}
                  </div>
                </div>
                
                <div className="capability-card">
                  <h4>🧠 Reasoning Models ({stats.reasoningModels})</h4>
                  <p>Advanced problem solving and analysis</p>
                  <div className="model-list">
                    {getReasoningModels().map(m => (
                      <span key={m.id} className="model-tag">{m.name}</span>
                    ))}
                  </div>
                </div>
                
                <div className="capability-card">
                  <h4>💎 Free Models ({stats.freeModels})</h4>
                  <p>No credits required</p>
                  <div className="model-list">
                    {getFreeModels().map(m => (
                      <span key={m.id} className="model-tag">{m.name}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Models Tab */}
        {activeTab === 'models' && (
          <div className="models-tab">
            <div className="models-controls">
              <h2>All Models ({filteredModels?.length || 0})</h2>
              <select 
                value={selectedVendor} 
                onChange={(e) => setSelectedVendor(e.target.value)}
                className="vendor-filter"
              >
                <option value="all">All Vendors</option>
                {providers?.map(p => (
                  <option key={p.vendor} value={p.vendor}>
                    {p.name} ({p.models.length})
                  </option>
                ))}
              </select>
            </div>

            <div className="global-message-input">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                placeholder="Enter message to test with models..."
                className="message-input"
              />
            </div>

            <div className="models-grid">
              {filteredModels?.map(model => (
                <ModelCard key={model.id} model={model} />
              ))}
            </div>
          </div>
        )}

        {/* Testing Tab */}
        {activeTab === 'testing' && (
          <div className="testing-tab">
            <h2>Model Testing</h2>
            
            <div className="test-controls">
              <input
                type="text"
                value={testMessage}
                onChange={(e) => setTestMessage(e.target.value)}
                placeholder="Test message for all models..."
                className="test-input"
              />
              <button 
                onClick={handleTestAllModels}
                disabled={loading}
                className="btn btn-test"
              >
                🧪 Test All Models
              </button>
            </div>

            {testResults.length > 0 && (
              <div className="test-results">
                <h3>Test Results ({testResults.length} models)</h3>
                <div className="results-grid">
                  {testResults.map((result, index) => (
                    <div key={index} className={`result-card ${result.success ? 'success' : 'error'}`}>
                      <div className="result-header">
                        <h4>{result.model}</h4>
                        <span className="result-vendor">{result.vendor}</span>
                        <span className={`result-status ${result.success ? 'success' : 'error'}`}>
                          {result.success ? '✅' : '❌'}
                        </span>
                      </div>
                      
                      <div className="result-content">
                        {result.success ? (
                          <p>{result.response}</p>
                        ) : (
                          <p className="error">Error: {result.error}</p>
                        )}
                      </div>
                      
                      <div className="result-meta">
                        <span>Credits: {result.credits}</span>
                        <span>Type: {result.type}</span>
                        <span>Context: {result.contextWindow?.toLocaleString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="chat-tab">
            <h2>Interactive Chat</h2>
            
            <div className="chat-history">
              {chatHistory.length === 0 ? (
                <div className="empty-chat">
                  <p>No chat history yet. Select a model and send a message!</p>
                </div>
              ) : (
                chatHistory.map(entry => (
                  <div key={entry.id} className="chat-entry">
                    <div className="chat-header">
                      <span className="chat-model">{entry.modelName}</span>
                      <span className="chat-vendor">({entry.vendor})</span>
                      <span className="chat-time">{entry.timestamp}</span>
                    </div>
                    <div className="chat-message">
                      <strong>You:</strong> {entry.message}
                    </div>
                    <div className="chat-response">
                      <strong>AI:</strong> {entry.response}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* Recommendations Tab */}
        {activeTab === 'recommendations' && (
          <div className="recommendations-tab">
            <h2>Smart Model Selection</h2>
            
            <div className="recommendation-categories">
              {[
                'hvac_calculations',
                'customer_support', 
                'code_review',
                'complex_reasoning',
                'budget_friendly'
              ].map(taskType => {
                const rec = getModelRecommendations(taskType);
                return (
                  <div key={taskType} className="recommendation-card">
                    <h3>{taskType.replace('_', ' ').toUpperCase()}</h3>
                    <p>{rec.reason}</p>
                    
                    <div className="primary-recommendation">
                      <h4>🥇 Primary Choice</h4>
                      {rec.primary && (
                        <div className="recommended-model">
                          <span className="model-name">{rec.primary.name}</span>
                          <span className="model-vendor">({rec.primary.vendor})</span>
                          <span className="model-credits">{rec.primary.credits}</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="alternative-recommendations">
                      <h4>🥈 Alternatives</h4>
                      <div className="alternatives-list">
                        {rec.alternatives?.slice(0, 3).map(alt => (
                          <div key={alt.id} className="alternative-model">
                            <span>{alt.name}</span>
                            <span>({alt.vendor})</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
          <h3 className="font-semibold text-orange-800">Reasoning Models</h3>
          <p className="text-2xl font-bold text-orange-600">{reasoningModels.length}</p>
        </div>
      </div>

      {/* Current Provider */}
      {currentProvider && (
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-lg mb-8">
          <h2 className="text-xl font-bold mb-2">🎯 Current Default Provider</h2>
          <p className="text-lg">{currentProvider.name}</p>
          <p className="text-sm opacity-90">
            {currentProvider.models.length} models available
          </p>
        </div>
      )}

      {/* Free Models Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4 text-green-700">🆓 Free Models</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {freeModels.map((model, index) => (
            <div key={index} className="border-2 border-green-200 bg-green-50 p-4 rounded-lg">
              <h3 className="font-bold text-green-800">{model.name}</h3>
              <p className="text-sm text-green-600">{model.providerName}</p>
              <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                FREE
              </span>
              {model.features && (
                <div className="mt-2">
                  {model.features.map((feature, idx) => (
                    <span key={idx} className="inline-block mr-1 mb-1 px-2 py-1 bg-green-200 text-green-700 text-xs rounded">
                      {feature}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* All Providers */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">🤖 All AI Providers</h2>
        <div className="space-y-6">
          {providers.map((provider, providerIndex) => (
            <div key={providerIndex} className="border rounded-lg p-6 bg-white shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-800">{provider.name}</h3>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  provider.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {provider.available ? 'Available' : 'Unavailable'}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {provider.models.map((model, modelIndex) => (
                  <div 
                    key={modelIndex} 
                    className={`border p-4 rounded-lg cursor-pointer transition-all ${
                      selectedModel?.id === model.id 
                        ? 'border-blue-500 bg-blue-50' 
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedModel(model)}
                  >
                    <h4 className="font-semibold text-gray-800">{model.name}</h4>
                    <p className="text-sm text-gray-600 mb-2">ID: {model.id}</p>
                    
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getModelCreditsColor(model.credits)}`}>
                        {model.credits}
                      </span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        model.type === 'reasoning' 
                          ? 'bg-purple-100 text-purple-800' 
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {model.type}
                      </span>
                    </div>

                    {model.family && (
                      <p className="text-xs text-gray-500">Family: {model.family}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Test Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">💬 Test Chat with Models</h2>
        <div className="bg-gray-50 p-6 rounded-lg">
          {selectedModel ? (
            <div className="mb-4 p-3 bg-blue-100 rounded-lg">
              <p className="text-blue-800">
                <strong>Selected:</strong> {selectedModel.name} ({selectedModel.vendor})
              </p>
            </div>
          ) : (
            <div className="mb-4 p-3 bg-yellow-100 rounded-lg">
              <p className="text-yellow-800">Select a model above to test chat functionality</p>
            </div>
          )}
          
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Enter your message..."
              className="flex-1 p-3 border rounded-lg"
              onKeyPress={(e) => e.key === 'Enter' && handleChatTest()}
            />
            <button
              onClick={handleChatTest}
              disabled={!selectedModel || !chatInput.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              Send
            </button>
          </div>
          
          {chatResponse && (
            <div className="p-4 bg-white border rounded-lg">
              <h4 className="font-semibold mb-2">Response:</h4>
              <pre className="whitespace-pre-wrap text-gray-700">{chatResponse}</pre>
            </div>
          )}
        </div>
      </div>

      {/* Provider Testing */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">🧪 Provider Health Check</h2>
        <button
          onClick={handleTestProviders}
          disabled={testingInProgress}
          className="mb-4 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
        >
          {testingInProgress ? 'Testing...' : 'Test All Providers'}
        </button>
        
        {testResults && (
          <div className="bg-white border rounded-lg p-6">
            <h3 className="font-bold mb-4">Test Results</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">{testResults.summary?.total || 0}</p>
                <p className="text-sm text-gray-600">Total Tested</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">{testResults.summary?.available || 0}</p>
                <p className="text-sm text-gray-600">Available</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-600">{testResults.summary?.chatCapable || 0}</p>
                <p className="text-sm text-gray-600">Chat Capable</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-orange-600">{testResults.summary?.embeddingCapable || 0}</p>
                <p className="text-sm text-gray-600">Embedding Capable</p>
              </div>
            </div>
            
            {testResults.recommendations && testResults.recommendations.length > 0 && (
              <div>
                <h4 className="font-semibold mb-2">Recommendations:</h4>
                {testResults.recommendations.map((rec, index) => (
                  <div key={index} className={`p-3 rounded mb-2 ${
                    rec.type === 'critical' ? 'bg-red-100 text-red-800' :
                    rec.type === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {rec.message}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Capabilities */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">🎯 Model Capabilities</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white border rounded-lg p-6">
            <h3 className="font-bold mb-3 text-blue-700">💬 Chat Models</h3>
            <div className="space-y-2">
              {capabilities.chat?.map((model, index) => (
                <div key={index} className="flex items-center justify-between p-2 bg-blue-50 rounded">
                  <span className="text-sm">{model}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white border rounded-lg p-6">
            <h3 className="font-bold mb-3 text-purple-700">🧠 Reasoning Models</h3>
            <div className="space-y-2">
              {capabilities.reasoning?.map((model, index) => (
                <div key={index} className="flex items-center justify-between p-2 bg-purple-50 rounded">
                  <span className="text-sm">{model}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg">
            <p className="text-lg">Loading Windsurf models...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WindsurfModelsShowcase;
