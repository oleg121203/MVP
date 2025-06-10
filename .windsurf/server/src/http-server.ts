#!/usr/bin/env node

/**
 * 🌐 HTTP Wrapper for Windsurf Enterprise MCP Server
 * Enables HTTP access to MCP tools for testing and integration
 */

import express from 'express';
import cors from 'cors';
import { spawn } from 'child_process';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const app = express();
const PORT = 8001;

// Middleware
app.use(cors());
app.use(express.json());

// Global MCP client
let mcpClient: Client | null = null;

/**
 * Initialize MCP client connection
 */
async function initializeMCPClient() {
  try {
    console.log('🚀 Starting MCP client...');
    
    // Create client transport with correct command parameters
    const transport = new StdioClientTransport({
      command: 'node',
      args: ['dist/enterprise-index.js']
    });

    // Initialize client
    mcpClient = new Client({
      name: 'windsurf-http-wrapper',
      version: '1.0.0',
    }, {
      capabilities: {}
    });

    await mcpClient.connect(transport);
    console.log('✅ MCP client connected successfully');

  } catch (error) {
    console.error('❌ Failed to initialize MCP client:', error);
    throw error;
  }
}

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    mcpConnected: mcpClient !== null,
    timestamp: new Date().toISOString()
  });
});

/**
 * List available tools
 */
app.get('/mcp/tools', async (req, res) => {
  try {
    if (!mcpClient) {
      return res.status(503).json({ error: 'MCP client not connected' });
    }

    const tools = await mcpClient.listTools();
    res.json(tools);
  } catch (error) {
    console.error('Error listing tools:', error);
    res.status(500).json({ error: 'Failed to list tools' });
  }
});

/**
 * Call MCP tool
 */
app.post('/mcp/call-tool', async (req, res) => {
  try {
    if (!mcpClient) {
      return res.status(503).json({ error: 'MCP client not connected' });
    }

    const { tool, params } = req.body;
    
    if (!tool) {
      return res.status(400).json({ error: 'Tool name is required' });
    }

    console.log(`🔧 Calling tool: ${tool} with params:`, params);
    
    const result = await mcpClient.callTool({
      name: tool,
      arguments: params || {}
    });

    res.json(result);
  } catch (error) {
    console.error('Error calling tool:', error);
    res.status(500).json({ 
      error: 'Failed to call tool', 
      details: error instanceof Error ? error.message : String(error)
    });
  }
});

/**
 * List available resources
 */
app.get('/mcp/resources', async (req, res) => {
  try {
    if (!mcpClient) {
      return res.status(503).json({ error: 'MCP client not connected' });
    }

    const resources = await mcpClient.listResources();
    res.json(resources);
  } catch (error) {
    console.error('Error listing resources:', error);
    res.status(500).json({ error: 'Failed to list resources' });
  }
});

/**
 * Start the HTTP server
 */
async function startServer() {
  try {
    // Initialize MCP client first
    await initializeMCPClient();

    // Start HTTP server
    app.listen(PORT, () => {
      console.log(`🌐 HTTP MCP Wrapper running on http://localhost:${PORT}`);
      console.log(`📋 Available endpoints:`);
      console.log(`   GET  /health - Health check`);
      console.log(`   GET  /mcp/tools - List available tools`);
      console.log(`   POST /mcp/call-tool - Call MCP tool`);
      console.log(`   GET  /mcp/resources - List available resources`);
    });

  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down HTTP MCP Wrapper...');
  
  if (mcpClient) {
    mcpClient.close();
  }
  
  process.exit(0);
});

// Start the server
startServer().catch(console.error);
