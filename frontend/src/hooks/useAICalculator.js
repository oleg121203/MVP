// Hook для AI інтеграції в калькулятори
// filepath: /workspaces/MVP/frontend/src/hooks/useAICalculator.js

import { useState, useEffect, useCallback } from 'react';
import VentAIService from '../services/aiService';

/**
 * Custom hook для AI покращення калькуляторів
 * @param {string} calculatorType - Тип калькулятора
 * @param {Object} inputData - Вхідні дані калькулятора
 * @param {Object} results - Результати обчислень
 * @returns {Object} AI функціональність та стан
 */
export const useAICalculator = (calculatorType, inputData, results) => {
  const [aiService] = useState(() => new VentAIService());
  const [aiSuggestions, setAiSuggestions] = useState(null);
  const [priceOptimization, setPriceOptimization] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Аналіз калькулятора
  const analyzeCalculation = useCallback(async () => {
    if (!results || Object.keys(results).length === 0) return;

    setLoading(true);
    setError(null);

    try {
      // Отримуємо AI рекомендації
      const suggestions = await aiService.getCalculatorAssistance(
        calculatorType,
        inputData
      );

      if (suggestions.success) {
        setAiSuggestions(suggestions);
      }

      // Оптимізація цін (якщо є вартість)
      if (results.cost || results.totalCost || results.area) {
        const optimization = await aiService.optimizePricesAndMaterials({
          calculatorType,
          inputData,
          results
        });

        if (optimization.success) {
          setPriceOptimization(optimization);
        }
      }
    } catch (err) {
      console.error('AI Analysis Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [calculatorType, inputData, results, aiService]);

  // Автоматичний аналіз при зміні результатів
  useEffect(() => {
    if (results && Object.keys(results).length > 0) {
      analyzeCalculation();
    }
  }, [results, analyzeCalculation]);

  // Оптимізація цін вручну
  const optimizePrice = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const marketAnalysis = await aiService.getMarketPriceAnalysis(
        'hvac_materials',
        'Ukraine',
        { area: results?.area, type: calculatorType }
      );

      if (marketAnalysis.success) {
        setPriceOptimization(prev => ({
          ...prev,
          market_analysis: marketAnalysis
        }));
      }
    } catch (err) {
      console.error('Price Optimization Error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [aiService, calculatorType, results]);

  // Отримання AI відповіді на питання
  const askAI = useCallback(async (question) => {
    setLoading(true);
    setError(null);

    try {
      const response = await aiService.generateAIResponse(question, {
        calculator_type: calculatorType,
        input_data: inputData,
        results: results,
        context: 'calculator_assistance'
      });

      setLoading(false);
      return response;
    } catch (err) {
      console.error('AI Question Error:', err);
      setError(err.message);
      setLoading(false);
      return { success: false, error: err.message };
    }
  }, [aiService, calculatorType, inputData, results]);

  // Валідація вхідних даних
  const validateInputs = useCallback(async (inputs) => {
    try {
      const validation = await aiService.validateInputData(calculatorType, inputs);
      return validation;
    } catch (err) {
      console.error('Input Validation Error:', err);
      return { success: false, error: err.message };
    }
  }, [aiService, calculatorType]);

  // Отримання рекомендацій по стандартам
  const getComplianceCheck = useCallback(async () => {
    try {
      const compliance = await aiService.checkCompliance(calculatorType, {
        inputData,
        results
      });
      return compliance;
    } catch (err) {
      console.error('Compliance Check Error:', err);
      return { success: false, error: err.message };
    }
  }, [aiService, calculatorType, inputData, results]);

  // Оновлення стану AI рекомендацій
  const updateAISuggestions = useCallback((suggestions) => {
    setAiSuggestions(suggestions);
  }, []);

  return {
    // Стан
    aiSuggestions,
    priceOptimization,
    loading,
    error,

    // Функції
    analyzeCalculation,
    optimizePrice,
    askAI,
    validateInputs,
    getComplianceCheck,
    updateAISuggestions,

    // Утиліти
    hasAISuggestions: Boolean(aiSuggestions),
    hasPriceOptimization: Boolean(priceOptimization),
    isReady: !loading && !error
  };
};

export default useAICalculator;
