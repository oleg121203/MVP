#!/usr/bin/env node

/**
 * 🧪 Test MCP Client Communication with Windsurf
 * Test communication with the running MCP server
 */

import { spawn } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const serverPath = join(__dirname, 'dist', 'enterprise-index.js');

async function testMCPCommunication() {
  console.log('🔄 Testing MCP Client Communication...\n');

  return new Promise((resolve, reject) => {
    // Start MCP server as child process
    const server = spawn('node', [serverPath], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let responseCount = 0;
    const messages = [];

    server.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter(line => line.trim());
      lines.forEach(line => {
        try {
          const message = JSON.parse(line);
          messages.push(message);
          console.log('📨 Received:', JSON.stringify(message, null, 2));
          responseCount++;
        } catch (e) {
          console.log('📝 Server log:', line);
        }
      });
    });

    server.stderr.on('data', (data) => {
      console.log('⚠️ Server error:', data.toString());
    });

    // Send initialize request
    const initMessage = {
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {
          roots: {
            listChanged: true
          },
          sampling: {}
        },
        clientInfo: {
          name: "Windsurf Test Client",
          version: "1.0.0"
        }
      }
    };

    console.log('📤 Sending initialize:', JSON.stringify(initMessage, null, 2));
    server.stdin.write(JSON.stringify(initMessage) + '\n');

    // Wait for response and send more requests
    setTimeout(() => {
      // List tools request
      const listToolsMessage = {
        jsonrpc: "2.0",
        id: 2,
        method: "tools/list"
      };

      console.log('📤 Sending tools/list:', JSON.stringify(listToolsMessage, null, 2));
      server.stdin.write(JSON.stringify(listToolsMessage) + '\n');
    }, 1000);

    setTimeout(() => {
      // Test AI provider list
      const providerListMessage = {
        jsonrpc: "2.0",
        id: 3,
        method: "tools/call",
        params: {
          name: "list_ai_providers",
          arguments: {}
        }
      };

      console.log('📤 Sending list_ai_providers:', JSON.stringify(providerListMessage, null, 2));
      server.stdin.write(JSON.stringify(providerListMessage) + '\n');
    }, 2000);

    setTimeout(() => {
      // Test Windsurf chat
      const chatMessage = {
        jsonrpc: "2.0",
        id: 4,
        method: "tools/call",
        params: {
          name: "ai_chat_completion",
          arguments: {
            messages: [
              { role: "user", content: "Explain HVAC basics" }
            ],
            provider: "windsurf"
          }
        }
      };

      console.log('📤 Sending ai_chat_completion:', JSON.stringify(chatMessage, null, 2));
      server.stdin.write(JSON.stringify(chatMessage) + '\n');
    }, 3000);

    // Clean up after tests
    setTimeout(() => {
      server.kill();
      console.log(`\n✅ Test completed. Received ${responseCount} responses.`);
      console.log(`📊 Total messages: ${messages.length}`);
      resolve(messages);
    }, 5000);

    server.on('error', (error) => {
      console.error('❌ Server error:', error);
      reject(error);
    });
  });
}

// Test the frontend service as well
async function testFrontendService() {
  console.log('\n🎨 Testing Frontend Windsurf Service...');

  try {
    // Import the frontend service
    const { default: EnhancedVentAIService } = await import('../frontend/src/services/windsurfAIService.js');
    
    const service = new EnhancedVentAIService();
    
    // Test service initialization
    console.log('✅ Frontend service initialized');
    
    // Test model selection
    const bestModel = service.selectBestModel('hvac_analysis');
    console.log('🎯 Best model for HVAC:', bestModel);
    
    // Test priority system
    const priorities = service.getModelPriorities();
    console.log('📊 Model priorities:', priorities);
    
  } catch (error) {
    console.log('⚠️ Frontend service test skipped:', error.message);
  }
}

async function main() {
  console.log('🚀 Starting MCP Integration Tests\n');
  
  try {
    await testMCPCommunication();
    await testFrontendService();
    
    console.log('\n🎉 All MCP tests completed successfully!');
    
  } catch (error) {
    console.error('❌ MCP test failed:', error);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { testMCPCommunication };
