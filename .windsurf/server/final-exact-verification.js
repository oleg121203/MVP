#!/usr/bin/env node

/**
 * 🎯 ФІНАЛЬНА ВЕРИФІКАЦІЯ WINDSURF ІНТЕГРАЦІЇ
 * Точна відповідність всіх моделей Windsurf (11 червня 2025)
 */

import fetch from 'node-fetch';

const colors = {
  green: '\x1b[32m',
  blue: '\x1b[34m', 
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

class WindsurfExactVerification {
  constructor() {
    this.endpoint = 'http://localhost:8001';
    this.results = [];
  }

  async runCompleteVerification() {
    console.log(`${colors.bold}🎯 === ФІНАЛЬНА ВЕРИФІКАЦІЯ WINDSURF ІНТЕГРАЦІЇ ===${colors.reset}\n`);

    try {
      // Test 1: Перевірка точності даних провайдерів
      await this.verifyExactProviderData();
      
      // Test 2: Перевірка всіх 11 моделей 
      await this.verifyExactModelCount();
      
      // Test 3: Перевірка безкоштовних моделей
      await this.verifyFreeModels();
      
      // Test 4: Перевірка reasoning моделей
      await this.verifyReasoningModels();
      
      // Test 5: Перевірка chat моделей
      await this.verifyChatModels();
      
      // Test 6: Перевірка capabilities
      await this.verifyCapabilities();
      
      // Test 7: Тестування AI чату
      await this.verifyAIChat();
      
      this.showFinalResults();
      
    } catch (error) {
      console.error(`${colors.red}❌ Verification failed: ${error.message}${colors.reset}`);
    }
  }

  async callAPI(endpoint, data = null) {
    const options = {
      method: data ? 'POST' : 'GET',
      headers: { 'Content-Type': 'application/json' }
    };
    
    if (data) options.body = JSON.stringify(data);
    
    const response = await fetch(`${this.endpoint}${endpoint}`, options);
    return await response.json();
  }

  async verifyExactProviderData() {
    console.log(`${colors.blue}🔍 Test 1: Перевірка точності даних провайдерів...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers',
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    
    // Очікувані провайдери
    const expectedVendors = ['windsurf', 'openai', 'anthropic', 'google', 'xai', 'deepseek'];
    const actualVendors = data.providers.map(p => p.vendor);
    
    const vendorsMatch = expectedVendors.every(v => actualVendors.includes(v));
    const totalProvidersMatch = data.total === 6;
    
    this.results.push({
      test: 'Provider Data Accuracy',
      success: vendorsMatch && totalProvidersMatch,
      details: `Providers: ${actualVendors.join(', ')} (Expected: 6, Got: ${data.total})`
    });
    
    console.log(`   ${vendorsMatch && totalProvidersMatch ? '✅' : '❌'} Providers: ${data.total}/6 expected`);
  }

  async verifyExactModelCount() {
    console.log(`${colors.blue}🔍 Test 2: Перевірка всіх 11 моделей...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers',
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    const totalModels = data.total_models;
    const expectedModels = 11;
    
    // Перевіряємо кількість моделей по провайдерах
    const modelsByProvider = {
      windsurf: 2,
      openai: 3,
      anthropic: 2,
      google: 2,
      xai: 1,
      deepseek: 1
    };
    
    let allCountsCorrect = true;
    data.providers.forEach(provider => {
      const expected = modelsByProvider[provider.vendor];
      if (provider.models.length !== expected) {
        allCountsCorrect = false;
      }
    });
    
    this.results.push({
      test: 'Exact Model Count',
      success: totalModels === expectedModels && allCountsCorrect,
      details: `Total: ${totalModels}/${expectedModels}, Per-provider counts: ${allCountsCorrect ? 'Correct' : 'Incorrect'}`
    });
    
    console.log(`   ${totalModels === expectedModels && allCountsCorrect ? '✅' : '❌'} Models: ${totalModels}/${expectedModels} expected`);
  }

  async verifyFreeModels() {
    console.log(`${colors.blue}🔍 Test 3: Перевірка безкоштовних моделей...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers', 
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    const freeModelsCount = data.free_models_count;
    const expectedFreeModels = 3; // windsurf-swe-1, windsurf-swe-1-lite, deepseek-v3
    
    // Перевіряємо конкретні безкоштовні моделі
    const allModels = data.providers.flatMap(p => p.models);
    const freeModels = allModels.filter(m => m.credits === 'free');
    const expectedFreeIds = ['windsurf-swe-1', 'windsurf-swe-1-lite', 'deepseek-v3'];
    const actualFreeIds = freeModels.map(m => m.id);
    
    const allFreeModelsPresent = expectedFreeIds.every(id => actualFreeIds.includes(id));
    
    this.results.push({
      test: 'Free Models Verification',
      success: freeModelsCount === expectedFreeModels && allFreeModelsPresent,
      details: `Free models: ${actualFreeIds.join(', ')}`
    });
    
    console.log(`   ${freeModelsCount === expectedFreeModels && allFreeModelsPresent ? '✅' : '❌'} Free models: ${freeModelsCount}/${expectedFreeModels} expected`);
  }

  async verifyReasoningModels() {
    console.log(`${colors.blue}🔍 Test 4: Перевірка reasoning моделей...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers',
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    const reasoningCapabilities = data.capabilities.reasoning;
    
    const expectedReasoning = [
      "openai:o3-mini (medium reasoning)",
      "anthropic:Claude 3.7 Sonnet (Thinking)"
    ];
    
    const reasoningMatch = expectedReasoning.every(r => reasoningCapabilities.includes(r));
    
    this.results.push({
      test: 'Reasoning Models',
      success: reasoningMatch && reasoningCapabilities.length === 2,
      details: `Reasoning: ${reasoningCapabilities.join(', ')}`
    });
    
    console.log(`   ${reasoningMatch ? '✅' : '❌'} Reasoning models: ${reasoningCapabilities.length}/2 expected`);
  }

  async verifyChatModels() {
    console.log(`${colors.blue}🔍 Test 5: Перевірка chat моделей...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers',
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    const chatCapabilities = data.capabilities.chat;
    
    const expectedChatCount = 9;
    const actualChatCount = chatCapabilities.length;
    
    this.results.push({
      test: 'Chat Models Count',
      success: actualChatCount === expectedChatCount,
      details: `Chat models: ${actualChatCount}/${expectedChatCount}`
    });
    
    console.log(`   ${actualChatCount === expectedChatCount ? '✅' : '❌'} Chat models: ${actualChatCount}/${expectedChatCount} expected`);
  }

  async verifyCapabilities() {
    console.log(`${colors.blue}🔍 Test 6: Перевірка capabilities структури...${colors.reset}`);
    
    const result = await this.callAPI('/mcp/call-tool', {
      tool: 'list_ai_providers',
      params: {}
    });
    
    const data = JSON.parse(result.content[0].text);
    const capabilities = data.capabilities;
    
    const hasChat = capabilities.chat && Array.isArray(capabilities.chat);
    const hasReasoning = capabilities.reasoning && Array.isArray(capabilities.reasoning);
    const totalCapabilities = capabilities.chat.length + capabilities.reasoning.length;
    
    this.results.push({
      test: 'Capabilities Structure',
      success: hasChat && hasReasoning && totalCapabilities === 11,
      details: `Chat: ${capabilities.chat.length}, Reasoning: ${capabilities.reasoning.length}, Total: ${totalCapabilities}`
    });
    
    console.log(`   ${hasChat && hasReasoning ? '✅' : '❌'} Capabilities structure: Complete`);
  }

  async verifyAIChat() {
    console.log(`${colors.blue}🔍 Test 7: Тестування AI чату...${colors.reset}`);
    
    try {
      const result = await this.callAPI('/mcp/call-tool', {
        tool: 'ai_chat_completion',
        params: {
          messages: [{ role: 'user', content: 'Hello! Test message.' }],
          provider: 'windsurf',
          model: 'windsurf-swe-1'
        }
      });
      
      const response = JSON.parse(result.content[0].text);
      const hasResponse = response.response && response.response.length > 0;
      
      this.results.push({
        test: 'AI Chat Functionality',
        success: hasResponse,
        details: `Response length: ${response.response?.length || 0} characters`
      });
      
      console.log(`   ${hasResponse ? '✅' : '❌'} AI Chat: ${hasResponse ? 'Working' : 'Failed'}`);
      
    } catch (error) {
      this.results.push({
        test: 'AI Chat Functionality',
        success: false,
        details: `Error: ${error.message}`
      });
      
      console.log(`   ❌ AI Chat: Failed - ${error.message}`);
    }
  }

  showFinalResults() {
    console.log(`\n${colors.bold}🏆 === ФІНАЛЬНІ РЕЗУЛЬТАТИ ВЕРИФІКАЦІЇ ===${colors.reset}\n`);
    
    const successful = this.results.filter(r => r.success);
    const failed = this.results.filter(r => !r.success);
    
    console.log(`${colors.green}✅ Успішні тести: ${successful.length}/${this.results.length}${colors.reset}`);
    console.log(`${colors.red}❌ Невдалі тести: ${failed.length}/${this.results.length}${colors.reset}`);
    
    if (this.results.length > 0) {
      const successRate = ((successful.length / this.results.length) * 100).toFixed(1);
      console.log(`${colors.cyan}📈 Рівень успіху: ${successRate}%${colors.reset}`);
    }
    
    console.log(`\n${colors.bold}📋 Деталі тестів:${colors.reset}`);
    this.results.forEach(result => {
      const icon = result.success ? '✅' : '❌';
      console.log(`${icon} ${result.test}: ${result.details}`);
    });
    
    console.log(`\n${colors.bold}🎯 === СТАТУС ІНТЕГРАЦІЇ ===${colors.reset}`);
    if (successful.length === this.results.length) {
      console.log(`${colors.green}🎉 WINDSURF ІНТЕГРАЦІЯ: ПОВНІСТЮ УСПІШНА!${colors.reset}`);
      console.log(`${colors.green}✅ Всі 6 провайдерів доступні${colors.reset}`);
      console.log(`${colors.green}✅ Всі 11 моделей інтегровано${colors.reset}`);
      console.log(`${colors.green}✅ 3 безкоштовні моделі доступні${colors.reset}`);
      console.log(`${colors.green}✅ 2 reasoning моделі функціонують${colors.reset}`);
      console.log(`${colors.green}✅ 9 chat моделей готові${colors.reset}`);
      console.log(`${colors.bold}🚀 ГОТОВО ДО ПРОДАКШНУ!${colors.reset}`);
    } else {
      console.log(`${colors.yellow}⚠️ WINDSURF ІНТЕГРАЦІЯ: ПОТРЕБУЄ ДООПРАЦЮВАННЯ${colors.reset}`);
      console.log(`${colors.yellow}📝 Див. деталі тестів вище${colors.reset}`);
    }
  }
}

// Запуск верифікації
async function main() {
  const verification = new WindsurfExactVerification();
  await verification.runCompleteVerification();
}

main().catch(console.error);
