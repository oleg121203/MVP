#!/usr/bin/env node

/**
 * VentAI Environment Setup Script
 * Automatically configures environment variables and validates setup
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
};

function log(message, color = colors.blue) {
    const timestamp = new Date().toISOString().substring(0, 19).replace('T', ' ');
    console.log(`${color}[${timestamp}]${colors.reset} ${message}`);
}

function success(message) {
    console.log(`${colors.green}✓${colors.reset} ${message}`);
}

function warning(message) {
    console.log(`${colors.yellow}⚠${colors.reset} ${message}`);
}

function error(message) {
    console.log(`${colors.red}✗${colors.reset} ${message}`);
}

class EnvironmentSetup {
    constructor() {
        this.projectRoot = process.cwd();
        this.envPath = path.join(this.projectRoot, '.env');
        this.envDevPath = path.join(this.projectRoot, 'environments', '.env.development');
    }

    checkNodeVersion() {
        log('Checking Node.js version...');
        const nodeVersion = process.version;
        const majorVersion = parseInt(nodeVersion.substring(1).split('.')[0]);
        
        if (majorVersion < 18) {
            error(`Node.js version ${nodeVersion} is not supported. Please use Node.js 18 or higher.`);
            process.exit(1);
        }
        
        success(`Node.js version ${nodeVersion} is supported`);
    }

    checkRequiredDirectories() {
        log('Checking required directories...');
        
        const requiredDirs = [
            'backend',
            'frontend', 
            'services/mcp',
            'infra/docker',
            'scripts',
            'environments',
            'tests'
        ];

        const missingDirs = requiredDirs.filter(dir => {
            const dirPath = path.join(this.projectRoot, dir);
            return !fs.existsSync(dirPath);
        });

        if (missingDirs.length > 0) {
            error(`Missing required directories: ${missingDirs.join(', ')}`);
            process.exit(1);
        }

        success('All required directories exist');
    }

    setupEnvironmentFile() {
        log('Setting up environment file...');
        
        if (fs.existsSync(this.envPath)) {
            warning('.env file already exists, skipping creation');
            return;
        }

        if (!fs.existsSync(this.envDevPath)) {
            error('Development environment template not found');
            process.exit(1);
        }

        // Copy development environment as base
        fs.copyFileSync(this.envDevPath, this.envPath);
        success('Created .env file from development template');
    }

    generateSecretKeys() {
        log('Generating secure secret keys...');
        
        const crypto = require('crypto');
        
        // Generate secure keys
        const secretKey = crypto.randomBytes(64).toString('hex');
        const encryptionKey = crypto.randomBytes(32).toString('base64');
        const jwtSecret = crypto.randomBytes(64).toString('hex');

        // Read current .env file
        let envContent = fs.readFileSync(this.envPath, 'utf8');

        // Replace placeholder keys if they exist
        envContent = envContent.replace(
            /SECRET_KEY=dev-secret-key-change-in-production.*/,
            `SECRET_KEY=${secretKey}`
        );
        
        envContent = envContent.replace(
            /ENCRYPTION_KEY=P-K5ljoDHJvr7AU-P-gsY3wtTuXAP-3PyuR7nfQsPE8=/,
            `ENCRYPTION_KEY=${encryptionKey}`
        );
        
        envContent = envContent.replace(
            /JWT_SECRET_KEY=jwt-secret-key-for-development.*/,
            `JWT_SECRET_KEY=${jwtSecret}`
        );

        // Write updated content
        fs.writeFileSync(this.envPath, envContent);
        success('Generated and updated secure secret keys');
    }

    validatePackageFiles() {
        log('Validating package files...');
        
        const packageFiles = [
            'package.json',
            'frontend/package.json',
            'backend/requirements.txt'
        ];

        for (const file of packageFiles) {
            const filePath = path.join(this.projectRoot, file);
            if (!fs.existsSync(filePath)) {
                error(`Missing required file: ${file}`);
                process.exit(1);
            }
        }

        success('All package files exist');
    }

    checkDockerSetup() {
        log('Checking Docker setup...');
        
        try {
            execSync('docker --version', { stdio: 'pipe' });
            execSync('docker-compose --version', { stdio: 'pipe' });
            success('Docker and Docker Compose are available');
        } catch (err) {
            warning('Docker or Docker Compose not found - Docker development will not be available');
        }
    }

    createLogDirectories() {
        log('Creating log directories...');
        
        const logDirs = [
            'backend/logs',
            'services/mcp/logs',
            'tests/logs'
        ];

        logDirs.forEach(dir => {
            const dirPath = path.join(this.projectRoot, dir);
            if (!fs.existsSync(dirPath)) {
                fs.mkdirSync(dirPath, { recursive: true });
            }
        });

        success('Created log directories');
    }

    displaySetupSummary() {
        console.log('\n' + '='.repeat(50));
        console.log(`${colors.bright}VentAI Environment Setup Complete!${colors.reset}`);
        console.log('='.repeat(50));
        
        console.log('\nNext steps:');
        console.log('1. Configure API keys in .env file (optional for development)');
        console.log('2. Run: npm run install:all');
        console.log('3. Run: npm run dev (Docker) or npm run dev:local (Local)');
        
        console.log('\nAccess points:');
        console.log('• Frontend: http://localhost:3000');
        console.log('• Backend API: http://localhost:8000/docs');
        console.log('• MCP Server: http://localhost:8001');
        
        console.log('\nUseful commands:');
        console.log('• npm run validate - Validate workflow');
        console.log('• npm run docker:down - Stop Docker services');
        console.log('• npm run test - Run all tests');
        console.log('• npm run lint - Run code linting');
    }

    async run() {
        try {
            log('Starting VentAI environment setup...');
            
            this.checkNodeVersion();
            this.checkRequiredDirectories();
            this.validatePackageFiles();
            this.setupEnvironmentFile();
            this.generateSecretKeys();
            this.createLogDirectories();
            this.checkDockerSetup();
            
            this.displaySetupSummary();
            
        } catch (err) {
            error(`Setup failed: ${err.message}`);
            process.exit(1);
        }
    }
}

// Run setup if this script is executed directly
if (require.main === module) {
    const setup = new EnvironmentSetup();
    setup.run();
}

module.exports = EnvironmentSetup;
