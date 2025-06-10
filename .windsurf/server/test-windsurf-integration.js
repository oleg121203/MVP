#!/usr/bin/env node

/**
 * 🌊 Test Windsurf Native AI Integration
 * Перевірка роботи нових Windsurf моделей
 */

import { WindsurfAIProvider } from './dist/windsurf-ai-provider.js';

async function testWindsurfIntegration() {
  console.log('🌊 Testing Windsurf Native AI Integration...\n');

  const provider = new WindsurfAIProvider();
  
  // Дочекаємося ініціалізації
  await new Promise(resolve => setTimeout(resolve, 2000));

  try {
    // 1. Перевірка статусу провайдера
    console.log('📊 Provider Status:');
    const status = provider.getProviderStatus();
    console.log(JSON.stringify(status, null, 2));
    console.log('');

    // 2. Список доступних провайдерів
    console.log('📋 Available Providers:');
    const providers = provider.getAvailableProviders();
    providers.forEach(p => {
      console.log(`  ✅ ${p.name} (${p.vendor}): ${p.models.length} models`);
    });
    console.log('');

    // 3. Тест простого чату
    console.log('💬 Testing Chat Completion...');
    try {
      const chatResponse = await provider.generateChatResponse([
        { role: 'user', content: 'Hello! Can you help me with HVAC calculations?' }
      ]);
      
      console.log(`Response from ${chatResponse.provider}:`);
      console.log(chatResponse.content.substring(0, 200) + '...');
      console.log(`Tokens: ${JSON.stringify(chatResponse.tokens)}\n`);
    } catch (error) {
      console.error('❌ Chat test failed:', error.message, '\n');
    }

    // 4. Тест аналізу коду
    console.log('🔍 Testing Code Analysis...');
    try {
      const codeAnalysis = await provider.analyzeCode(
        `function calculateAirflow(area, height) {
  return area * height * 6; // ACH of 6
}`,
        'test.js',
        'review'
      );
      
      console.log(`Code analysis from ${codeAnalysis.provider}:`);
      console.log(codeAnalysis.content.substring(0, 200) + '...\n');
    } catch (error) {
      console.error('❌ Code analysis test failed:', error.message, '\n');
    }

    // 5. Тест HVAC розрахунків
    console.log('🧮 Testing HVAC Calculations...');
    try {
      const hvacHelp = await provider.hvacCalculationAssistance(
        'Air Flow Calculator',
        { area: 20, height: 3, people: 4 },
        'How much ventilation do I need for this room?'
      );
      
      console.log(`HVAC assistance from ${hvacHelp.provider}:`);
      console.log(hvacHelp.content.substring(0, 200) + '...\n');
    } catch (error) {
      console.error('❌ HVAC calculation test failed:', error.message, '\n');
    }

    // 6. Тест всіх моделей
    console.log('🧪 Testing All Models...');
    try {
      const testResults = await provider.testAllModels();
      
      console.log(`Model Test Results:`);
      console.log(`Total: ${testResults.summary.total}, Working: ${testResults.summary.working}, Failed: ${testResults.summary.failed}`);
      
      testResults.available.forEach(result => {
        const status = result.success ? '✅' : '❌';
        console.log(`  ${status} ${result.vendor}:${result.model}`);
      });
      console.log('');
    } catch (error) {
      console.error('❌ Model testing failed:', error.message, '\n');
    }

    // 7. Демонстрація вибору оптимальної моделі
    console.log('🎯 Optimal Model Selection:');
    const taskTypes = ['code', 'creative', 'technical', 'reasoning', 'general'];
    
    for (const taskType of taskTypes) {
      try {
        const bestModel = await provider.selectBestModel(taskType);
        console.log(`  ${taskType}: ${bestModel}`);
      } catch (error) {
        console.log(`  ${taskType}: Error - ${error.message}`);
      }
    }
    console.log('');

    console.log('🎉 Windsurf Native AI Integration Test Completed!\n');
    
    // Рекомендації
    console.log('💡 Recommendations:');
    if (providers.length === 0) {
      console.log('  ⚠️  No Windsurf providers available. Check your Windsurf installation.');
    } else {
      console.log(`  ✅ ${providers.length} providers available`);
      console.log('  ✅ Native integration provides better security and performance');
      console.log('  ✅ No external API keys required');
      console.log('  ✅ Uses your existing Windsurf subscription');
    }

  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Запуск тестів
testWindsurfIntegration().catch(console.error);
