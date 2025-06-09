import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';
import { jest } from '@jest/globals';

// Configure test timeout
configure({ asyncUtilTimeout: 5000 });

// Mock Redis client
jest.mock('redis', () => ({
  createClient: jest.fn().mockImplementation(() => ({
    connect: jest.fn(),
    get: jest.fn(),
    setEx: jest.fn(),
    quit: jest.fn(),
    on: jest.fn()
  }))
}));
