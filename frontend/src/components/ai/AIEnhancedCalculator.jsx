// AI компоненти для інтеграції в калькулятори
// filepath: /workspaces/MVP/frontend/src/components/ai/AIEnhancedCalculator.jsx

import React, { useState, useEffect } from 'react';
import VentAIService from '../../services/aiService';
import './AIComponents.css';

/**
 * AI-покращений калькулятор з інтелектуальними рекомендаціями
 */
export const AIEnhancedCalculator = ({ 
  calculatorType, 
  inputData, 
  results, 
  onSuggestionsUpdate,
  children 
}) => {
  const [aiSuggestions, setAiSuggestions] = useState(null);
  const [priceOptimization, setPriceOptimization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiService] = useState(() => new VentAIService());

  useEffect(() => {
    if (results && Object.keys(results).length > 0) {
      analyzeCalculation();
    }
  }, [results, inputData]);

  const analyzeCalculation = async () => {
    setLoading(true);
    
    try {
      // Отримуємо AI рекомендації
      const suggestions = await aiService.getCalculatorAssistance(
        calculatorType, 
        inputData
      );
      
      if (suggestions.success) {
        setAiSuggestions(suggestions);
        if (onSuggestionsUpdate) {
          onSuggestionsUpdate(suggestions);
        }
      }

      // Оптимізація цін та матеріалів
      if (results.cost || results.area) {
        const optimization = await aiService.optimizePricesAndMaterials(
          { calculatorType, inputData, results }
        );
        
        if (optimization.success) {
          setPriceOptimization(optimization);
        }
      }
    } catch (error) {
      console.error('AI Analysis Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimizePrice = async () => {
    setLoading(true);
    
    try {
      const marketAnalysis = await aiService.getMarketPriceAnalysis(
        'duct_materials',
        'Ukraine',
        { area: results.area, type: calculatorType }
      );
      
      if (marketAnalysis.success) {
        setPriceOptimization(prev => ({
          ...prev,
          market_analysis: marketAnalysis
        }));
      }
    } catch (error) {
      console.error('Price Optimization Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-enhanced-calculator">
      {children}
      
      {loading && (
        <div className="ai-loading">
          <div className="ai-spinner"></div>
          <span>AI аналізує ваші дані...</span>
        </div>
      )}
      
      {aiSuggestions && (
        <AIRecommendationsPanel 
          suggestions={aiSuggestions}
          onOptimizePrice={handleOptimizePrice}
        />
      )}
      
      {priceOptimization && (
        <PriceOptimizationPanel 
          optimization={priceOptimization}
          calculatorType={calculatorType}
        />
      )}
    </div>
  );
};

/**
 * Панель AI рекомендацій
 */
export const AIRecommendationsPanel = ({ suggestions, onOptimizePrice }) => {
  const [expandedSection, setExpandedSection] = useState(null);

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="ai-recommendations-panel">
      <h3 className="ai-panel-title">
        🤖 AI Рекомендації
        <span className="ai-provider">({suggestions.provider})</span>
      </h3>
      
      {suggestions.warnings && suggestions.warnings.length > 0 && (
        <div className="ai-warnings">
          <h4 onClick={() => toggleSection('warnings')} className="ai-section-header">
            ⚠️ Попередження {expandedSection === 'warnings' ? '▼' : '▶'}
          </h4>
          {expandedSection === 'warnings' && (
            <ul className="ai-list">
              {suggestions.warnings.map((warning, index) => (
                <li key={index} className="ai-warning-item">{warning}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      
      {suggestions.suggestions && suggestions.suggestions.length > 0 && (
        <div className="ai-suggestions">
          <h4 onClick={() => toggleSection('suggestions')} className="ai-section-header">
            💡 Пропозиції {expandedSection === 'suggestions' ? '▼' : '▶'}
          </h4>
          {expandedSection === 'suggestions' && (
            <ul className="ai-list">
              {suggestions.suggestions.map((suggestion, index) => (
                <li key={index} className="ai-suggestion-item">{suggestion}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      
      {suggestions.optimizations && suggestions.optimizations.length > 0 && (
        <div className="ai-optimizations">
          <h4 onClick={() => toggleSection('optimizations')} className="ai-section-header">
            🚀 Оптимізації {expandedSection === 'optimizations' ? '▼' : '▶'}
          </h4>
          {expandedSection === 'optimizations' && (
            <ul className="ai-list">
              {suggestions.optimizations.map((optimization, index) => (
                <li key={index} className="ai-optimization-item">{optimization}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      
      {suggestions.standards_compliance && Object.keys(suggestions.standards_compliance).length > 0 && (
        <div className="ai-compliance">
          <h4 onClick={() => toggleSection('compliance')} className="ai-section-header">
            📋 Відповідність стандартам {expandedSection === 'compliance' ? '▼' : '▶'}
          </h4>
          {expandedSection === 'compliance' && (
            <div className="ai-compliance-details">
              {Object.entries(suggestions.standards_compliance).map(([standard, status]) => (
                <div key={standard} className={`ai-compliance-item ${status ? 'compliant' : 'non-compliant'}`}>
                  <span className="ai-standard-name">{standard}</span>
                  <span className="ai-compliance-status">
                    {status ? '✅ Відповідає' : '❌ Не відповідає'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      <div className="ai-actions">
        <button 
          className="ai-button ai-optimize-button"
          onClick={onOptimizePrice}
        >
          💰 Оптимізувати ціни
        </button>
      </div>
    </div>
  );
};

/**
 * Панель оптимізації цін
 */
export const PriceOptimizationPanel = ({ optimization, calculatorType }) => {
  const [selectedAlternative, setSelectedAlternative] = useState(null);

  const handleSelectAlternative = (alternative) => {
    setSelectedAlternative(alternative);
  };

  return (
    <div className="price-optimization-panel">
      <h3 className="ai-panel-title">
        💰 Оптимізація цін та матеріалів
        <span className="ai-provider">({optimization.provider})</span>
      </h3>
      
      {optimization.savings_potential > 0 && (
        <div className="ai-savings-highlight">
          <h4>🎯 Потенційна економія: {optimization.savings_potential}%</h4>
        </div>
      )}
      
      {optimization.material_alternatives && optimization.material_alternatives.length > 0 && (
        <div className="ai-alternatives">
          <h4>🔄 Альтернативні матеріали</h4>
          <div className="ai-alternatives-grid">
            {optimization.material_alternatives.map((alternative, index) => (
              <div 
                key={index} 
                className={`ai-alternative-card ${selectedAlternative === index ? 'selected' : ''}`}
                onClick={() => handleSelectAlternative(index)}
              >
                <h5>{alternative.material_name}</h5>
                <div className="ai-alternative-details">
                  <div className="ai-price-comparison">
                    <span className="ai-original-price">Оригінал: {alternative.original_price} ₴</span>
                    <span className="ai-new-price">Нова ціна: {alternative.new_price} ₴</span>
                    <span className="ai-savings">
                      Економія: {alternative.savings_percentage}%
                    </span>
                  </div>
                  <div className="ai-quality-rating">
                    Якість: {alternative.quality_rating}/10
                  </div>
                  {alternative.advantages && (
                    <ul className="ai-advantages">
                      {alternative.advantages.map((advantage, advIndex) => (
                        <li key={advIndex}>{advantage}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {optimization.supplier_recommendations && optimization.supplier_recommendations.length > 0 && (
        <div className="ai-suppliers">
          <h4>🏪 Рекомендовані постачальники</h4>
          <div className="ai-suppliers-list">
            {optimization.supplier_recommendations.map((supplier, index) => (
              <div key={index} className="ai-supplier-card">
                <h5>{supplier.name}</h5>
                <div className="ai-supplier-details">
                  <span className="ai-supplier-rating">⭐ {supplier.rating}/5</span>
                  <span className="ai-supplier-delivery">🚚 {supplier.delivery_time}</span>
                  <span className="ai-supplier-price">💰 {supplier.price_range}</span>
                </div>
                {supplier.specialties && (
                  <div className="ai-supplier-specialties">
                    <strong>Спеціалізація:</strong> {supplier.specialties.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {optimization.market_analysis && (
        <div className="ai-market-analysis">
          <h4>📊 Аналіз ринку</h4>
          <div className="ai-market-details">
            {optimization.market_analysis.price_trends && (
              <div className="ai-price-trends">
                <h5>📈 Тенденції цін</h5>
                <ul>
                  {Object.entries(optimization.market_analysis.price_trends).map(([period, trend]) => (
                    <li key={period}>
                      {period}: {trend}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {optimization.market_analysis.recommended_timing && (
              <div className="ai-timing-recommendation">
                <h5>⏰ Рекомендований час покупки</h5>
                <p>{optimization.market_analysis.recommended_timing}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * AI чат асистент для калькуляторів
 */
export const AIChatAssistant = ({ calculatorType, context = {} }) => {
  const [messages, setMessages] = useState([
    {
      type: 'ai',
      content: `Привіт! Я AI асистент для ${calculatorType}. Чим можу допомогти?`,
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [aiService] = useState(() => new VentAIService());

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await aiService.generateAIResponse(
        inputValue,
        {
          calculator_type: calculatorType,
          conversation_context: messages.slice(-5), // Останні 5 повідомлень
          user_context: context
        }
      );

      if (response.success) {
        const aiMessage = {
          type: 'ai',
          content: response.response,
          timestamp: new Date(),
          provider: response.provider
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      const errorMessage = {
        type: 'ai',
        content: 'Вибачте, сталася помилка. Спробуйте ще раз.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`ai-chat-assistant ${isExpanded ? 'expanded' : 'minimized'}`}>
      <div className="ai-chat-header" onClick={() => setIsExpanded(!isExpanded)}>
        <span className="ai-chat-title">🤖 AI Асистент</span>
        <span className="ai-chat-toggle">{isExpanded ? '▼' : '▲'}</span>
      </div>
      
      {isExpanded && (
        <div className="ai-chat-content">
          <div className="ai-chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`ai-chat-message ${message.type}`}>
                <div className="ai-message-content">
                  {message.content}
                  {message.provider && (
                    <span className="ai-message-provider">({message.provider})</span>
                  )}
                </div>
                <div className="ai-message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
            {loading && (
              <div className="ai-chat-message ai-loading-message">
                <div className="ai-typing-indicator">
                  AI друкує...
                </div>
              </div>
            )}
          </div>
          
          <div className="ai-chat-input">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Задайте питання про розрахунки..."
              disabled={loading}
              rows={2}
            />
            <button 
              onClick={sendMessage}
              disabled={loading || !inputValue.trim()}
              className="ai-send-button"
            >
              📤
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIEnhancedCalculator;
