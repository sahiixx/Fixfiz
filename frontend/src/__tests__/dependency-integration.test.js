/**
 * Integration tests for updated dependencies (axios and postcss)
 */

describe('Dependency Integration Tests', () => {
  describe('Axios Integration', () => {
    it('should be able to import axios', () => {
      const axios = require('axios');
      expect(axios).toBeDefined();
      expect(typeof axios.create).toBe('function');
    });

    it('should support all HTTP methods', () => {
      const axios = require('axios');
      expect(typeof axios.get).toBe('function');
      expect(typeof axios.post).toBe('function');
      expect(typeof axios.put).toBe('function');
      expect(typeof axios.delete).toBe('function');
    });
  });

  describe('Version Validation', () => {
    it('should have exact versions we expect', () => {
      const packageJson = require('../../package.json');
      expect(packageJson.dependencies.axios).toBe('^1.12.0');
      expect(packageJson.devDependencies.postcss).toBe('^8.5.0');
    });
  });
});