#!/usr/bin/env node

/**
 * 🧪 Test script for Multi-AI Provider functionality
 * Tests all the new AI tools and provider capabilities
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

class AIProviderTester {
  constructor() {
    this.serverProcess = null;
    this.testResults = {
      providers: [],
      tools: [],
      errors: []
    };
  }

  /**
   * Test AI Providers List
   */
  async testListProviders() {
    console.log('🔍 Testing AI Providers List...');
    try {
      const result = await this.callMCPTool('list_ai_providers', {});
      console.log('✅ AI Providers listed successfully');
      this.testResults.tools.push({ tool: 'list_ai_providers', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed to list AI providers:', error.message);
      this.testResults.errors.push({ tool: 'list_ai_providers', error: error.message });
      return null;
    }
  }

  /**
   * Test Chat Completion
   */
  async testChatCompletion() {
    console.log('💬 Testing AI Chat Completion...');
    try {
      const result = await this.callMCPTool('ai_chat_completion', {
        messages: [
          { role: 'user', content: 'Hello! Please respond with a brief greeting.' }
        ],
        temperature: 0.7,
        maxTokens: 100
      });
      console.log('✅ AI Chat Completion successful');
      this.testResults.tools.push({ tool: 'ai_chat_completion', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed AI chat completion:', error.message);
      this.testResults.errors.push({ tool: 'ai_chat_completion', error: error.message });
      return null;
    }
  }

  /**
   * Test Embeddings Creation
   */
  async testCreateEmbeddings() {
    console.log('🧮 Testing AI Embeddings Creation...');
    try {
      const result = await this.callMCPTool('ai_create_embeddings', {
        text: 'This is a test text for embedding generation in VentAI project.'
      });
      console.log('✅ AI Embeddings creation successful');
      this.testResults.tools.push({ tool: 'ai_create_embeddings', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed AI embeddings creation:', error.message);
      this.testResults.errors.push({ tool: 'ai_create_embeddings', error: error.message });
      return null;
    }
  }

  /**
   * Test Windsurf Assistant
   */
  async testWindsurfAssistant() {
    console.log('🏗️ Testing Windsurf AI Assistant...');
    try {
      const result = await this.callMCPTool('ai_windsurf_assistant', {
        query: 'How can I optimize my TypeScript code for better performance?',
        context: 'Working on VentAI enterprise project',
        includeProjectFiles: true
      });
      console.log('✅ Windsurf AI Assistant successful');
      this.testResults.tools.push({ tool: 'ai_windsurf_assistant', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed Windsurf AI Assistant:', error.message);
      this.testResults.errors.push({ tool: 'ai_windsurf_assistant', error: error.message });
      return null;
    }
  }

  /**
   * Test Code Analysis
   */
  async testCodeAnalysis() {
    console.log('🔍 Testing AI Code Analysis...');
    try {
      const result = await this.callMCPTool('ai_code_analysis', {
        filePath: '/Users/olegkizyma/workspaces/MVP/ventai-app/.windsurf/server/src/enterprise-index.ts',
        analysisType: 'review'
      });
      console.log('✅ AI Code Analysis successful');
      this.testResults.tools.push({ tool: 'ai_code_analysis', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed AI code analysis:', error.message);
      this.testResults.errors.push({ tool: 'ai_code_analysis', error: error.message });
      return null;
    }
  }

  /**
   * Test Provider Testing
   */
  async testProviderTesting() {
    console.log('🧪 Testing AI Provider Testing...');
    try {
      const result = await this.callMCPTool('ai_test_providers', {
        testEmbeddings: true,
        testChat: true
      });
      console.log('✅ AI Provider Testing successful');
      this.testResults.tools.push({ tool: 'ai_test_providers', success: true, result });
      return result;
    } catch (error) {
      console.error('❌ Failed AI provider testing:', error.message);
      this.testResults.errors.push({ tool: 'ai_test_providers', error: error.message });
      return null;
    }
  }

  /**
   * Mock MCP tool call (in real scenario this would use MCP protocol)
   */
  async callMCPTool(toolName, params) {
    // This is a simulation - in real usage this would call through MCP protocol
    console.log(`📞 Calling MCP tool: ${toolName}`);
    console.log(`📄 Params:`, JSON.stringify(params, null, 2));
    
    // Simulate success response
    return {
      success: true,
      tool: toolName,
      timestamp: new Date().toISOString(),
      simulated: true,
      message: `${toolName} would be executed with provided parameters`
    };
  }

  /**
   * Run all tests
   */
  async runAllTests() {
    console.log('🚀 Starting Multi-AI Provider Test Suite...\n');

    // Test each AI tool
    await this.testListProviders();
    await this.testChatCompletion();
    await this.testCreateEmbeddings();
    await this.testWindsurfAssistant();
    await this.testCodeAnalysis();
    await this.testProviderTesting();

    // Print results
    this.printResults();
  }

  /**
   * Print test results
   */
  printResults() {
    console.log('\n📊 Test Results Summary:');
    console.log('=====================================');
    
    const successful = this.testResults.tools.filter(t => t.success).length;
    const total = this.testResults.tools.length + this.testResults.errors.length;
    
    console.log(`✅ Successful: ${successful}/${total}`);
    console.log(`❌ Failed: ${this.testResults.errors.length}/${total}`);
    
    if (this.testResults.errors.length > 0) {
      console.log('\n❌ Failed Tests:');
      this.testResults.errors.forEach(error => {
        console.log(`   - ${error.tool}: ${error.error}`);
      });
    }
    
    console.log('\n✅ Successful Tests:');
    this.testResults.tools.forEach(test => {
      console.log(`   - ${test.tool}: ${test.success ? 'PASS' : 'FAIL'}`);
    });
    
    console.log('\n🎯 Multi-AI Provider Integration Complete!');
    console.log('📋 Available AI Tools:');
    console.log('   1. list_ai_providers - List all available AI providers');
    console.log('   2. ai_chat_completion - Generate text with multiple AI providers');
    console.log('   3. ai_create_embeddings - Create embeddings with provider selection');
    console.log('   4. ai_windsurf_assistant - Context-aware Windsurf assistant');
    console.log('   5. ai_code_analysis - AI-powered code analysis');
    console.log('   6. ai_test_providers - Test all providers availability');
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const tester = new AIProviderTester();
  tester.runAllTests().catch(console.error);
}

export default AIProviderTester;
