#!/usr/bin/env node

/**
 * Node.js Version Checker for VentAI
 * Ensures the project runs on supported Node.js versions
 */

const semver = require('semver');
const pkg = require('../package.json');

const currentVersion = process.version;
const requiredVersion = pkg.engines?.node || '>=18.0.0';

console.log(`Current Node.js version: ${currentVersion}`);
console.log(`Required Node.js version: ${requiredVersion}`);

if (!semver.satisfies(currentVersion, requiredVersion)) {
    console.error(`\n❌ Node.js version ${currentVersion} is not supported.`);
    console.error(`Please upgrade to Node.js ${requiredVersion}\n`);
    
    console.log('To upgrade Node.js:');
    console.log('1. Using nvm: nvm install 18 && nvm use 18');
    console.log('2. Download from: https://nodejs.org/');
    console.log('3. Using package manager: brew install node (macOS)\n');
    
    process.exit(1);
}

console.log('✅ Node.js version is compatible\n');
