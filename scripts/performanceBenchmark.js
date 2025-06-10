const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Configuration
const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3000/api/v1';
const ENDPOINTS = [
  { name: 'Get Leads', url: `${BASE_URL}/leads`, method: 'GET' },
  { name: 'Get Lead Sources', url: `${BASE_URL}/lead-sources`, method: 'GET' },
  { name: 'Get Lead Campaigns', url: `${BASE_URL}/lead-campaigns`, method: 'GET' },
  { name: 'Get CRM Contacts', url: `${BASE_URL}/crm/contacts`, method: 'GET' },
  { name: 'Get CRM Deals', url: `${BASE_URL}/crm/deals`, method: 'GET' },
];
const REQUESTS_PER_ENDPOINT = 100;
const CONCURRENT_REQUESTS = 10;

// Results storage
const results = [];

// Function to make a single request and measure time
async function makeRequest(endpoint) {
  const startTime = Date.now();
  try {
    if (endpoint.method === 'GET') {
      await axios.get(endpoint.url);
    } else if (endpoint.method === 'POST') {
      await axios.post(endpoint.url, {});
    }
    const endTime = Date.now();
    return { success: true, latency: endTime - startTime, error: null };
  } catch (error) {
    console.error(`Error for ${endpoint.name}:`, error.message);
    return { success: false, latency: null, error: error.message };
  }
}

// Function to run benchmark for a single endpoint
async function benchmarkEndpoint(endpoint) {
  console.log(`Benchmarking ${endpoint.name}...`);
  const requestResults = [];
  
  for (let i = 0; i < REQUESTS_PER_ENDPOINT; i += CONCURRENT_REQUESTS) {
    const batch = [];
    for (let j = 0; j < CONCURRENT_REQUESTS && i + j < REQUESTS_PER_ENDPOINT; j++) {
      batch.push(makeRequest(endpoint));
    }
    const batchResults = await Promise.all(batch);
    requestResults.push(...batchResults);
  }
  
  const successfulResults = requestResults.filter(result => result.success);
  const latencies = successfulResults.map(result => result.latency);
  const errors = requestResults.filter(result => !result.success).map(result => result.error);
  const uniqueErrors = [...new Set(errors)];
  
  const averageLatency = latencies.length > 0 ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 'N/A';
  const minLatency = latencies.length > 0 ? Math.min(...latencies) : 'N/A';
  const maxLatency = latencies.length > 0 ? Math.max(...latencies) : 'N/A';
  const successRate = (successfulResults.length / REQUESTS_PER_ENDPOINT) * 100;
  
  const result = {
    endpoint: endpoint.name,
    averageLatency,
    minLatency,
    maxLatency,
    successRate,
    totalRequests: REQUESTS_PER_ENDPOINT,
    successfulRequests: successfulResults.length,
    errors: uniqueErrors.length > 0 ? uniqueErrors : 'None'
  };
  
  console.log(`Completed ${endpoint.name}: Avg Latency = ${averageLatency}ms, Success Rate = ${successRate}%`);
  return result;
}

// Main function to run benchmarks for all endpoints
async function runBenchmarks() {
  console.log('Starting performance benchmarking...');
  const startTime = new Date().toISOString();
  
  for (const endpoint of ENDPOINTS) {
    const result = await benchmarkEndpoint(endpoint);
    results.push(result);
  }
  
  const endTime = new Date().toISOString();
  console.log('Benchmarking completed.');
  console.log('Results:', JSON.stringify(results, null, 2));
  
  // Save results to file
  const outputDir = path.join(__dirname, '../reports');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const outputFile = path.join(outputDir, `benchmark-${startTime.replace(/[:.]/g, '-')}.json`);
  fs.writeFileSync(outputFile, JSON.stringify({ startTime, endTime, results }, null, 2));
  console.log(`Results saved to ${outputFile}`);
}

// Run the benchmarks
runBenchmarks().catch(console.error);
