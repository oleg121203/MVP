module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  testMatch: ['**/tests/**/*.test.ts', '**/tests/**/*.test.tsx'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setupTests.ts'],
  transformIgnorePatterns: ['/node_modules/(?!cheerio|axios|socket.io)/'],
  transform: {
    '^.+\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
