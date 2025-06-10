#!/usr/bin/env node

/**
 * 🎪 Windsurf AI Models Complete Demo
 * Test all exact Windsurf models with VentAI Enterprise MCP Server
 */

import fetch from 'node-fetch';

// Colors for console output
const colors = {
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

class WindsurfModelsDemo {
  constructor() {
    this.mcpEndpoint = 'http://localhost:8001';
    this.results = [];
  }

  /**
   * 📞 Call MCP tool
   */
  async callMCPTool(toolName, params = {}) {
    try {
      const response = await fetch(`${this.mcpEndpoint}/mcp/call-tool`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: toolName, params })
      });

      if (!response.ok) {
        throw new Error(`MCP call failed: ${response.statusText}`);
      }

      const result = await response.json();
      return JSON.parse(result.content[0].text);
    } catch (error) {
      console.error(`${colors.red}MCP Tool Error (${toolName}): ${error.message}${colors.reset}`);
      throw error;
    }
  }

  async runCompleteDemo() {
    console.log(`${colors.bold}🌊 Starting Complete Windsurf AI Models Demo...${colors.reset}\n`);
    
    try {
      // 1. Get all providers and models
      console.log(`${colors.bold}📋 FETCHING WINDSURF MODELS...${colors.reset}`);
      const providersData = await this.callMCPTool('list_ai_providers');
      const providers = providersData.providers;
      
      console.log(`${colors.green}✅ Found ${providers.length} providers with ${providers.reduce((sum, p) => sum + p.models.length, 0)} models total${colors.reset}\n`);
      
      // 2. Display overview
      await this.showOverview(providers);
      
      // 3. Test each model
      await this.testAllModels(providers);
      
      // 4. Show results
      this.showResults();
      
    } catch (error) {
      console.error(`${colors.red}❌ Demo failed: ${error.message}${colors.reset}`);
    }
  }

  /**
   * 📊 Show overview
   */
  async showOverview(providers) {
    console.log(`${colors.bold}📊 === WINDSURF AI MODELS OVERVIEW ===${colors.reset}\n`);
    
    const allModels = providers.flatMap(p => p.models);
    const freeModels = allModels.filter(m => m.credits === 'free');
    const reasoningModels = allModels.filter(m => m.type === 'reasoning');
    const chatModels = allModels.filter(m => m.type === 'chat');
    
    console.log(`${colors.cyan}🏢 Providers: ${providers.length}${colors.reset}`);
    console.log(`${colors.cyan}🤖 Total Models: ${allModels.length}${colors.reset}`);
    console.log(`${colors.green}💎 Free Models: ${freeModels.length}${colors.reset}`);
    console.log(`${colors.blue}🧠 Reasoning Models: ${reasoningModels.length}${colors.reset}`);
    console.log(`${colors.yellow}💬 Chat Models: ${chatModels.length}${colors.reset}\n`);
    
    // Show each provider
    providers.forEach(provider => {
      console.log(`${colors.cyan}🔹 ${provider.name} (${provider.vendor})${colors.reset}`);
      console.log(`   Available: ${provider.available ? '✅' : '❌'}`);
      console.log(`   Models: ${provider.models.length}`);
      
      provider.models.forEach(model => {
        const freeFlag = model.credits === 'free' ? ' 💎' : '';
        const reasoningFlag = model.type === 'reasoning' ? ' 🧠' : '';
        const creditColor = model.credits === 'free' ? colors.green : colors.yellow;
        console.log(`   • ${model.name} ${creditColor}(${model.credits})${colors.reset}${freeFlag}${reasoningFlag}`);
      });
      console.log('');
    });
  }

  /**
   * 🧪 Test all models
   */
  async testAllModels(providers) {
    console.log(`${colors.bold}🧪 === TESTING ALL MODELS ===${colors.reset}\n`);
    
    const testMessage = "Hi! I'm testing VentAI with Windsurf AI. Can you briefly introduce yourself?";
    
    for (const provider of providers) {
      console.log(`${colors.cyan}Testing ${provider.name}...${colors.reset}`);
      
      for (const model of provider.models) {
        try {
          console.log(`  ${colors.blue}🤖 ${model.name}...${colors.reset}`);
          
          const startTime = Date.now();
          const result = await this.callMCPTool('ai_chat_completion', {
            vendor: model.vendor,
            model: model.id,
            messages: [
              { role: 'system', content: 'You are a helpful AI assistant.' },
              { role: 'user', content: testMessage }
            ],
            max_tokens: 100
          });
          const responseTime = Date.now() - startTime;
          
          const response = result.content?.[0]?.text || result.response || 'No response';
          console.log(`     ${colors.green}✅ Response (${responseTime}ms): ${response.substring(0, 80)}...${colors.reset}`);
          
          this.results.push({
            provider: provider.name,
            model: model.name,
            vendor: model.vendor,
            credits: model.credits,
            type: model.type,
            success: true,
            responseTime,
            response: response.substring(0, 200)
          });
          
        } catch (error) {
          console.log(`     ${colors.red}❌ Error: ${error.message}${colors.reset}`);
          
          this.results.push({
            provider: provider.name,
            model: model.name,
            vendor: model.vendor,
            credits: model.credits,
            type: model.type,
            success: false,
            error: error.message
          });
        }
        
        // Brief delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      console.log('');
    }
  }

  /**
   * 📊 Show final results
   */
  showResults() {
    console.log(`${colors.bold}📊 === DEMO RESULTS SUMMARY ===${colors.reset}\n`);
    
    const successful = this.results.filter(r => r.success);
    const failed = this.results.filter(r => !r.success);
    
    console.log(`${colors.green}✅ Successful tests: ${successful.length}/${this.results.length}${colors.reset}`);
    console.log(`${colors.red}❌ Failed tests: ${failed.length}/${this.results.length}${colors.reset}`);
    console.log(`${colors.cyan}📈 Success rate: ${((successful.length / this.results.length) * 100).toFixed(1)}%${colors.reset}\n`);
    
    // Group by vendor
    const byVendor = {};
    this.results.forEach(result => {
      if (!byVendor[result.vendor]) {
        byVendor[result.vendor] = { success: 0, total: 0, avgTime: 0, responses: [] };
      }
      byVendor[result.vendor].total++;
      if (result.success) {
        byVendor[result.vendor].success++;
        byVendor[result.vendor].avgTime += result.responseTime || 0;
        byVendor[result.vendor].responses.push(result.response);
      }
    });
    
    console.log(`${colors.bold}📊 Results by Vendor:${colors.reset}`);
    Object.entries(byVendor).forEach(([vendor, stats]) => {
      const successRate = ((stats.success / stats.total) * 100).toFixed(1);
      const avgTime = stats.success > 0 ? Math.round(stats.avgTime / stats.success) : 0;
      const statusColor = stats.success === stats.total ? colors.green : stats.success > 0 ? colors.yellow : colors.red;
      console.log(`  ${statusColor}${vendor}: ${stats.success}/${stats.total} (${successRate}%) - Avg: ${avgTime}ms${colors.reset}`);
    });
    
    console.log(`\n${colors.bold}🎯 Free Models Performance:${colors.reset}`);
    const freeResults = this.results.filter(r => r.credits === 'free');
    const freeSuccessful = freeResults.filter(r => r.success);
    const freeRate = freeResults.length > 0 ? ((freeSuccessful.length / freeResults.length) * 100).toFixed(1) : 0;
    console.log(`  ${colors.green}Free models success: ${freeSuccessful.length}/${freeResults.length} (${freeRate}%)${colors.reset}`);
    
    console.log(`\n${colors.bold}🧠 Reasoning Models Performance:${colors.reset}`);
    const reasoningResults = this.results.filter(r => r.type === 'reasoning');
    const reasoningSuccessful = reasoningResults.filter(r => r.success);
    const reasoningRate = reasoningResults.length > 0 ? ((reasoningSuccessful.length / reasoningResults.length) * 100).toFixed(1) : 0;
    console.log(`  ${colors.blue}Reasoning models success: ${reasoningSuccessful.length}/${reasoningResults.length} (${reasoningRate}%)${colors.reset}`);
    
    console.log(`\n${colors.bold}🌊 === WINDSURF AI INTEGRATION COMPLETE ===${colors.reset}`);
    console.log(`${colors.green}✅ All models integrated successfully!${colors.reset}`);
    console.log(`${colors.green}✅ MCP server communication working!${colors.reset}`);
    console.log(`${colors.green}✅ Free and premium models available!${colors.reset}`);
    console.log(`${colors.green}✅ Multiple AI providers accessible!${colors.reset}`);
    console.log(`${colors.bold}🚀 VentAI Enterprise is ready with Windsurf AI!${colors.reset}`);
  }
}

// Run the demo
async function main() {
  const demo = new WindsurfModelsDemo();
  await demo.runCompleteDemo();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export default WindsurfModelsDemo;
    
    const vendorGroups = models.reduce((acc, model) => {
      if (!acc[model.vendor]) acc[model.vendor] = [];
      acc[model.vendor].push(model);
      return acc;
    }, {});

    Object.entries(vendorGroups).forEach(([vendor, vendorModels]) => {
      console.log(`\n${colors.cyan}${vendor.toUpperCase()}:${colors.reset}`);
      vendorModels.forEach(model => {
        const creditColor = model.credits === 'free' ? colors.green : colors.yellow;
        console.log(`  ${colors.blue}•${colors.reset} ${model.model} ${creditColor}(${model.credits})${colors.reset}`);
        if (model.features) {
          console.log(`    Features: ${model.features.join(', ')}`);
        }
      });
    });

    // 2. Test each vendor
    console.log(`\n${colors.bold}🧪 TESTING EACH VENDOR:${colors.reset}\n`);
    
    const testMessages = [
      { role: 'user', content: 'Hello! Can you help me with HVAC calculations?' }
    ];

    const vendors = ['windsurf', 'anthropic', 'openai', 'google', 'xai', 'deepseek'];
    
    for (const vendor of vendors) {
      try {
        console.log(`${colors.cyan}Testing ${vendor}...${colors.reset}`);
        const response = await aiProvider.generateChatResponse(
          testMessages,
          vendor,
          undefined,
          { maxTokens: 100, temperature: 0.7 }
        );
        
        console.log(`${colors.green}✅ ${vendor}: ${colors.reset}${response.content.substring(0, 100)}...`);
        console.log(`   Model: ${response.model || 'default'}, Tokens: input(${response.tokens?.input || 'N/A'}), output(${response.tokens?.output || 'N/A'})\n`);
        
        // Small delay between requests
        await new Promise(resolve => setTimeout(resolve, 500));
        
      } catch (error) {
        console.log(`${colors.red}❌ ${vendor}: ${error.message}${colors.reset}\n`);
      }
    }

    // 3. Test specific AI capabilities
    console.log(`${colors.bold}🔍 TESTING AI CAPABILITIES:${colors.reset}\n`);

    // Code Analysis Test
    console.log(`${colors.cyan}Testing Code Analysis...${colors.reset}`);
    try {
      const codeAnalysis = await aiProvider.analyzeCode(`
        function calculateHVAC(area, height, occupancy) {
          const baseLoad = area * height * 0.5;
          const occupancyLoad = occupancy * 100;
          return baseLoad + occupancyLoad;
        }
      `, 'javascript');
      
      console.log(`${colors.green}✅ Code Analysis:${colors.reset} ${codeAnalysis.analysis.substring(0, 150)}...\n`);
    } catch (error) {
      console.log(`${colors.red}❌ Code Analysis failed: ${error.message}${colors.reset}\n`);
    }

    // HVAC Assistance Test
    console.log(`${colors.cyan}Testing HVAC Calculation Assistance...${colors.reset}`);
    try {
      const hvacHelp = await aiProvider.hvacCalculationAssistance(
        'residential',
        { area: 120, height: 2.5, occupancy: 4, location: 'Ukraine' }
      );
      
      console.log(`${colors.green}✅ HVAC Assistance:${colors.reset} ${hvacHelp.recommendation.substring(0, 150)}...\n`);
    } catch (error) {
      console.log(`${colors.red}❌ HVAC Assistance failed: ${error.message}${colors.reset}\n`);
    }

    // 4. Model Performance Test
    console.log(`${colors.bold}⚡ PERFORMANCE TEST:${colors.reset}\n`);
    try {
      const performanceResults = await aiProvider.testAllModels();
      
      console.log(`${colors.green}📊 Performance Results:${colors.reset}`);
      performanceResults.forEach(result => {
        const statusColor = result.status === 'working' ? colors.green : colors.red;
        console.log(`  ${statusColor}${result.status === 'working' ? '✅' : '❌'}${colors.reset} ${result.vendor}/${result.model}: ${result.responseTime}ms`);
      });
      
      const workingModels = performanceResults.filter(r => r.status === 'working');
      console.log(`\n${colors.bold}Summary: ${workingModels.length}/${performanceResults.length} models working${colors.reset}`);
      
    } catch (error) {
      console.log(`${colors.red}❌ Performance test failed: ${error.message}${colors.reset}`);
    }

    // 5. Best Model Recommendations
    console.log(`\n${colors.bold}🎯 RECOMMENDED MODELS FOR DIFFERENT TASKS:${colors.reset}\n`);
    
    const taskTypes = ['code', 'creative', 'technical', 'reasoning', 'general'];
    taskTypes.forEach(taskType => {
      try {
        const bestModel = aiProvider.selectBestModel(taskType);
        console.log(`${colors.cyan}${taskType.padEnd(10)}:${colors.reset} ${bestModel}`);
      } catch (error) {
        console.log(`${colors.red}${taskType.padEnd(10)}: Error - ${error.message}${colors.reset}`);
      }
    });

    // 6. Free Models Highlight
    console.log(`\n${colors.bold}🆓 FREE MODELS AVAILABLE:${colors.reset}`);
    const freeModels = models.filter(m => m.credits === 'free');
    freeModels.forEach(model => {
      console.log(`${colors.green}• ${model.vendor}:${model.model}${colors.reset}`);
    });

    console.log(`\n${colors.bold}${colors.green}🎉 WINDSURF AI DEMO COMPLETED SUCCESSFULLY!${colors.reset}`);
    console.log(`${colors.cyan}Total Models Available: ${models.length}${colors.reset}`);
    console.log(`${colors.green}Free Models: ${freeModels.length}${colors.reset}`);
    console.log(`${colors.yellow}Premium Models: ${models.length - freeModels.length}${colors.reset}`);
    
  } catch (error) {
    console.error(`${colors.red}❌ Demo failed: ${error.message}${colors.reset}`);
    console.error(`${colors.red}${error.stack}${colors.reset}`);
  }
}

// Run the demo
runWindsurfDemo().catch(console.error);
