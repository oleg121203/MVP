// VentAI Frontend AI Integration - Комплексна AI система для HVAC
// filepath: /workspaces/MVP/frontend/src/services/aiService.js

class VentAIService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    this.cache = new Map(); // Кешування для покращення перформансу
    this.currentProvider = null;
  }

  /**
   * HVAC Системний Аналіз та Оптимізація
   */
  async analyzeHVAC(hvacData) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/hvac/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(hvacData)
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          analysis: result.analysis,
          recommendations: result.recommendations,
          efficiency_score: result.efficiency_score,
          cost_optimization: result.cost_optimization,
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'HVAC analysis failed');
      }
    } catch (error) {
      console.error('HVAC Analysis Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Оптимізація Цін та Матеріалів
   */
  async optimizePricesAndMaterials(calculationData, preferences = {}) {
    const cacheKey = `price_optimize_${JSON.stringify(calculationData)}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/price-optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculation_data: calculationData,
          preferences: {
            budget_range: preferences.budgetRange || [1000, 50000],
            quality_priority: preferences.qualityPriority || 'medium',
            delivery_time: preferences.deliveryTime || 'standard',
            brand_preferences: preferences.brandPreferences || [],
            sustainability: preferences.sustainability || false,
            ...preferences
          }
        })
      });

      const result = await response.json();
      
      if (result.success) {
        const optimization = {
          success: true,
          material_alternatives: result.alternatives || [],
          cost_breakdown: result.cost_breakdown || {},
          savings_potential: result.savings_potential || 0,
          quality_score: result.quality_score || 0,
          supplier_recommendations: result.suppliers || [],
          market_analysis: result.market_analysis || {},
          price_trends: result.price_trends || {},
          recommended_option: result.recommended_option || null,
          provider: result.provider_used
        };
        
        this.cache.set(cacheKey, optimization);
        return optimization;
      } else {
        throw new Error(result.error || 'Price optimization failed');
      }
    } catch (error) {
      console.error('Price Optimization Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Аналіз та Порівняння Проектів
   */
  async analyzeProject(projectData, comparisonProjects = []) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/project-analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project: projectData,
          comparisons: comparisonProjects
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          project_analysis: {
            complexity_score: result.complexity_score || 0,
            risk_assessment: result.risk_assessment || {},
            timeline_estimate: result.timeline_estimate || {},
            cost_estimate: result.cost_estimate || {},
            efficiency_rating: result.efficiency_rating || 0,
            compliance_check: result.compliance_check || {},
            optimization_suggestions: result.optimization_suggestions || []
          },
          comparisons: result.comparisons || [],
          recommendations: result.recommendations || [],
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Project analysis failed');
      }
    } catch (error) {
      console.error('Project Analysis Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * AI Асистент для Калькуляторів
   */
  async getCalculatorAssistance(calculatorType, inputData, question = null) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/calculator-assist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculator_type: calculatorType,
          input_data: inputData,
          question: question,
          context: {
            user_level: 'professional', // можна адаптувати
            calculation_purpose: 'design'
          }
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          suggestions: result.suggestions || [],
          warnings: result.warnings || [],
          optimizations: result.optimizations || [],
          explanations: result.explanations || {},
          alternative_approaches: result.alternatives || [],
          standards_compliance: result.standards || {},
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Calculator assistance failed');
      }
    } catch (error) {
      console.error('Calculator Assistance Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Розумна Валідація Вводу
   */
  async validateInputs(calculatorType, inputs) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/validate-inputs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculator_type: calculatorType,
          inputs: inputs
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          is_valid: result.is_valid || false,
          errors: result.errors || [],
          warnings: result.warnings || [],
          suggestions: result.suggestions || [],
          corrected_values: result.corrected_values || {},
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Input validation failed');
      }
    } catch (error) {
      console.error('Input Validation Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Аналіз Ринкових Цін
   */
  async getMarketPriceAnalysis(materialType, region = 'Ukraine', specifications = {}) {
    const cacheKey = `market_${materialType}_${region}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/market-prices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          material_type: materialType,
          region: region,
          specifications: specifications
        })
      });

      const result = await response.json();
      
      if (result.success) {
        const analysis = {
          success: true,
          current_prices: result.prices || {},
          price_trends: result.trends || {},
          suppliers: result.suppliers || [],
          market_conditions: result.market_conditions || {},
          forecast: result.forecast || {},
          recommended_timing: result.timing || {},
          provider: result.provider_used
        };
        
        // Кешуємо на 30 хвилин
        setTimeout(() => this.cache.delete(cacheKey), 30 * 60 * 1000);
        this.cache.set(cacheKey, analysis);
        return analysis;
      } else {
        throw new Error(result.error || 'Market analysis failed');
      }
    } catch (error) {
      console.error('Market Analysis Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Генерація Звітів та Документації
   */
  async generateReport(calculationResults, reportType = 'detailed') {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/generate-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculation_results: calculationResults,
          report_type: reportType,
          include_recommendations: true,
          include_alternatives: true,
          format: 'detailed_analysis'
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          report: {
            summary: result.summary || '',
            detailed_analysis: result.detailed_analysis || '',
            recommendations: result.recommendations || [],
            technical_notes: result.technical_notes || [],
            compliance_notes: result.compliance_notes || [],
            cost_breakdown: result.cost_breakdown || {},
            charts_data: result.charts_data || {}
          },
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Report generation failed');
      }
    } catch (error) {
      console.error('Report Generation Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Загальна AI генерація
   */
  async generateAIResponse(prompt, context = {}, preferredProvider = null) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          context,
          preferred_provider: preferredProvider
        })
      });

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('AI Generation Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Статус AI провайдерів
   */
  async getAIProvidersStatus() {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/providers/status`);
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('AI Providers Status Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Простий чат з AI - для зворотної сумісності
   */
  async chatWithAI(message) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: message })
      });

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Chat Error:', error);
      return {
        reply: 'Помилка з\'єднання з AI сервісом',
        suggestions: ['Спробуйте пізніше'],
        provider: 'none'
      };
    }
  }

  /**
   * Інтелектуальні Рекомендації для Калькуляторів
   */
  async getSmartRecommendations(calculatorType, results, userPreferences = {}) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/smart-recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculator_type: calculatorType,
          results: results,
          user_preferences: userPreferences,
          market_context: true
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          recommendations: {
            primary: result.primary_recommendations || [],
            alternative: result.alternative_recommendations || [],
            cost_saving: result.cost_saving_tips || [],
            efficiency: result.efficiency_tips || [],
            maintenance: result.maintenance_tips || [],
            upgrades: result.upgrade_suggestions || []
          },
          priority_scores: result.priority_scores || {},
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Smart recommendations failed');
      }
    } catch (error) {
      console.error('Smart Recommendations Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Автоматичне Виявлення Помилок та Оптимізація
   */
  async detectIssuesAndOptimize(calculatorType, inputData, currentResults) {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/ai/detect-optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          calculator_type: calculatorType,
          input_data: inputData,
          current_results: currentResults
        })
      });

      const result = await response.json();
      
      if (result.success) {
        return {
          success: true,
          issues: {
            critical: result.critical_issues || [],
            warnings: result.warnings || [],
            suggestions: result.suggestions || []
          },
          optimizations: {
            performance: result.performance_optimizations || [],
            cost: result.cost_optimizations || [],
            efficiency: result.efficiency_optimizations || []
          },
          corrected_inputs: result.corrected_inputs || {},
          improved_results: result.improved_results || {},
          provider: result.provider_used
        };
      } else {
        throw new Error(result.error || 'Issue detection failed');
      }
    } catch (error) {
      console.error('Issue Detection Error:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Утиліти для кешування та очищення
   */
  clearCache() {
    this.cache.clear();
  }

  getCacheSize() {
    return this.cache.size;
  }

  /**
   * Перевірка доступності AI сервісів
   */
  async checkHealth() {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/health`);
      const result = await response.json();
      return {
        available: result.status === 'healthy',
        providers: result.providers || [],
        version: result.version || 'unknown'
      };
    } catch (error) {
      return {
        available: false,
        error: error.message
      };
    }
  }
}

// Приклад React компонента, який використовує AI
export const HVACAnalyzer = () => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const aiService = new VentAIService();

  const analyzeSystem = async () => {
    setLoading(true);
    
    const hvacData = {
      area: 100,
      occupancy: 20,
      climate_zone: "temperate",
      building_type: "office"
    };

    const result = await aiService.analyzeHVAC(hvacData);
    
    if (result.success) {
      setAnalysis(result.analysis);
      // Показуємо результат користувачу
      console.log('Аналіз завершено:', result);
    } else {
      console.error('Помилка аналізу:', result.error);
    }
    
    setLoading(false);
  };

  return (
    <div>
      <h2>AI Аналіз HVAC</h2>
      <button onClick={analyzeSystem} disabled={loading}>
        {loading ? 'Аналізую...' : 'Проаналізувати систему'}
      </button>
      
      {analysis && (
        <div>
          <h3>Результати аналізу:</h3>
          <pre>{JSON.stringify(analysis, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default VentAIService;
