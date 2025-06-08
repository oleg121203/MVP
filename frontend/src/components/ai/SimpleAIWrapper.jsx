// Спрощений AI Wrapper для калькуляторів
// filepath: /workspaces/MVP/frontend/src/components/ai/SimpleAIWrapper.jsx

import React from 'react';
import { useAICalculator } from '../../hooks/useAICalculator';
import { AIRecommendationsPanel, PriceOptimizationPanel, AIChatAssistant } from './AIEnhancedCalculator';
import './AIComponents.css';

/**
 * Простий AI wrapper для калькуляторів
 */
export const SimpleAIWrapper = ({ 
  calculatorType, 
  inputData, 
  results, 
  children,
  showChat = true,
  showPriceOptimization = true,
  showRecommendations = true 
}) => {
  const {
    aiSuggestions,
    priceOptimization,
    loading,
    error,
    optimizePrice,
    askAI,
    hasAISuggestions,
    hasPriceOptimization
  } = useAICalculator(calculatorType, inputData, results);

  return (
    <div className="ai-calculator-wrapper">
      {/* Основний калькулятор */}
      {children}

      {/* AI Loading Indicator */}
      {loading && (
        <div className="ai-loading">
          <div className="ai-spinner"></div>
          <span>AI аналізує ваші дані...</span>
        </div>
      )}

      {/* AI Error */}
      {error && (
        <div className="ai-error">
          <span>❌ Помилка AI: {error}</span>
        </div>
      )}

      {/* AI Рекомендації */}
      {showRecommendations && hasAISuggestions && (
        <AIRecommendationsPanel 
          suggestions={aiSuggestions}
          onOptimizePrice={optimizePrice}
        />
      )}

      {/* Оптимізація Цін */}
      {showPriceOptimization && hasPriceOptimization && (
        <PriceOptimizationPanel 
          optimization={priceOptimization}
          calculatorType={calculatorType}
        />
      )}

      {/* AI Chat Assistant */}
      {showChat && (
        <AIChatAssistant 
          calculatorType={calculatorType}
          context={{
            inputData,
            results,
            suggestions: aiSuggestions,
            optimization: priceOptimization
          }}
          onAskAI={askAI}
        />
      )}
    </div>
  );
};

export default SimpleAIWrapper;
