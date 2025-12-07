/**
 * Comprehensive tests for package.json dependency updates
 * Tests validate axios and postcss version updates and their compatibility
 */

describe('Package Dependencies', () => {
  let packageJson;

  beforeAll(() => {
    packageJson = require('../../package.json');
  });

  describe('Axios Dependency', () => {
    it('should have axios dependency defined', () => {
      expect(packageJson.dependencies).toHaveProperty('axios');
    });

    it('should have axios version 1.12.0 or higher', () => {
      const axiosVersion = packageJson.dependencies.axios;
      expect(axiosVersion).toBeTruthy();
      const versionNumber = axiosVersion.replace(/[\^~]/, '');
      const [major, minor] = versionNumber.split('.').map(Number);
      expect(major).toBeGreaterThanOrEqual(1);
      if (major === 1) {
        expect(minor).toBeGreaterThanOrEqual(12);
      }
    });

    it('should have axios at version ^1.12.0', () => {
      expect(packageJson.dependencies.axios).toBe('^1.12.0');
    });
  });

  describe('PostCSS Dependency', () => {
    it('should have postcss in devDependencies', () => {
      expect(packageJson.devDependencies).toHaveProperty('postcss');
    });

    it('should have postcss at version ^8.5.0', () => {
      expect(packageJson.devDependencies.postcss).toBe('^8.5.0');
    });
  });

  describe('Security Considerations', () => {
    it('should not use wildcard version for axios', () => {
      const axiosVersion = packageJson.dependencies.axios;
      expect(axiosVersion).not.toBe('*');
      expect(axiosVersion).not.toBe('latest');
    });

    it('should not use wildcard version for postcss', () => {
      const postcssVersion = packageJson.devDependencies.postcss;
      expect(postcssVersion).not.toBe('*');
      expect(postcssVersion).not.toBe('latest');
    });
  });
});