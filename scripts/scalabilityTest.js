const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3000/api/v1';
const CONCURRENT_USERS = [10, 50, 100];
const REQUESTS_PER_USER = 100;
const OUTPUT_DIR = path.join(__dirname, 'test_results');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'scalability_results.json');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// API Endpoints to test
const ENDPOINTS = [
  { method: 'GET', path: '/lead-generation/leads' },
  { method: 'GET', path: '/crm/contacts' },
  { method: 'GET', path: '/price-data/current' },
];

// Function to simulate a single user's requests
async function simulateUser(endpoint) {
  const startTime = Date.now();
  let successfulRequests = 0;
  let totalLatency = 0;
  let errors = [];

  for (let i = 0; i < REQUESTS_PER_USER; i++) {
    try {
      const response = await axios({
        method: endpoint.method,
        url: `${API_BASE_URL}${endpoint.path}`,
        headers: { 'Authorization': 'Bearer test-token' }
      });
      successfulRequests++;
      totalLatency += Date.now() - startTime;
    } catch (error) {
      errors.push({ request: i + 1, error: error.message });
    }
  }

  return {
    successfulRequests,
    successRate: successfulRequests / REQUESTS_PER_USER,
    averageLatency: successfulRequests > 0 ? totalLatency / successfulRequests : 0,
    errors
  };
}

// Function to run test for a specific number of concurrent users
async function runTestForConcurrentUsers(usersCount, endpoint) {
  console.log(`Running scalability test for ${usersCount} concurrent users on ${endpoint.path}`);
  const startTime = Date.now();
  const userPromises = [];

  for (let i = 0; i < usersCount; i++) {
    userPromises.push(simulateUser(endpoint));
  }

  const results = await Promise.all(userPromises);
  const totalRequests = results.reduce((sum, r) => sum + r.successfulRequests, 0);
  const totalLatency = results.reduce((sum, r) => sum + r.averageLatency * r.successfulRequests, 0);
  const totalErrors = results.reduce((sum, r) => sum + r.errors.length, 0);

  return {
    users: usersCount,
    endpoint: endpoint.path,
    totalRequests,
    successRate: totalRequests / (usersCount * REQUESTS_PER_USER),
    averageLatency: totalRequests > 0 ? totalLatency / totalRequests : 0,
    totalErrors,
    duration: (Date.now() - startTime) / 1000, // in seconds
    detailedResults: results
  };
}

// Main function to run scalability tests
async function runScalabilityTests() {
  console.log('Starting scalability tests...');
  const allResults = [];

  for (const endpoint of ENDPOINTS) {
    for (const usersCount of CONCURRENT_USERS) {
      const result = await runTestForConcurrentUsers(usersCount, endpoint);
      allResults.push(result);
      console.log(`Completed test for ${usersCount} users on ${endpoint.path}: ${result.successRate.toFixed(2)} success rate, ${result.averageLatency.toFixed(2)}ms avg latency`);
    }
  }

  // Save results to file
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allResults, null, 2));
  console.log(`Scalability test results saved to ${OUTPUT_FILE}`);

  // Summarize results
  console.log('\nScalability Test Summary:');
  for (const result of allResults) {
    console.log(`- ${result.users} users on ${result.endpoint}: ${result.successRate.toFixed(2)} success rate, ${result.averageLatency.toFixed(2)}ms avg latency, ${result.totalErrors} errors`);
  }
}

// Run the tests
runScalabilityTests().catch(console.error);
