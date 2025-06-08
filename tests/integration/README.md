# VentAI Integration Tests

This directory contains integration tests for the VentAI application.

## Purpose

Integration tests verify that different components work correctly together:

- API endpoint testing
- Database integration
- Service communication
- Third-party integrations

## Running Tests

```bash
# Run all integration tests
npm run test:integration

# Run with specific environment
npm run test:integration:docker
```

## Test Categories

- **API Tests**: Test REST API endpoints
- **Database Tests**: Test database operations
- **Service Tests**: Test inter-service communication
- **Authentication Tests**: Test auth flows
