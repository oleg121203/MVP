module.exports = {
  collectCoverage: true,
  coverageDirectory: '../../coverage/frontend',
  coverageReporters: ['text', 'lcov'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testEnvironment: 'jsdom',
  transformIgnorePatterns: [
    '/node_modules/(?!axios|other-es-module)/'
  ],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
    '/node_modules/(axios|other-es-module)/.*': 'babel-jest'
  }
};
