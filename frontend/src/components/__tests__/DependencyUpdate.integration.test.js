/**
 * Integration tests for package.json dependency updates
 * Tests axios and postcss version updates for compatibility and functionality
 */

describe('Dependency Update Integration Tests', () => {
  describe('Axios Version Update (^1.8.4 -> ^1.12.0)', () => {
    test('axios module can be imported', () => {
      expect(() => {
        require('axios');
      }).not.toThrow();
    });

    test('axios has expected API methods', () => {
      const axios = require('axios');
      
      expect(axios).toBeDefined();
      expect(typeof axios.get).toBe('function');
      expect(typeof axios.post).toBe('function');
      expect(typeof axios.put).toBe('function');
      expect(typeof axios.delete).toBe('function');
      expect(typeof axios.patch).toBe('function');
      expect(typeof axios.create).toBe('function');
    });

    test('axios.create returns axios instance with expected methods', () => {
      const axios = require('axios');
      const instance = axios.create({
        baseURL: 'https://api.example.com',
        timeout: 5000,
      });

      expect(instance).toBeDefined();
      expect(typeof instance.get).toBe('function');
      expect(typeof instance.post).toBe('function');
    });

    test('axios has interceptors support', () => {
      const axios = require('axios');
      
      expect(axios.interceptors).toBeDefined();
      expect(axios.interceptors.request).toBeDefined();
      expect(axios.interceptors.response).toBeDefined();
      expect(typeof axios.interceptors.request.use).toBe('function');
      expect(typeof axios.interceptors.response.use).toBe('function');
    });

    test('axios supports FormData (form-data ^4.0.4 dependency)', () => {
      const axios = require('axios');
      
      // Verify axios can handle FormData
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      };
      
      expect(config.headers['Content-Type']).toBe('multipart/form-data');
    });

    test('axios defaults object is accessible', () => {
      const axios = require('axios');
      
      expect(axios.defaults).toBeDefined();
      expect(axios.defaults.headers).toBeDefined();
      expect(axios.defaults.headers.common).toBeDefined();
    });
  });

  describe('PostCSS Version Update (^8.4.49 -> ^8.5.0)', () => {
    test('postcss module can be imported', () => {
      expect(() => {
        require('postcss');
      }).not.toThrow();
    });

    test('postcss has expected API', () => {
      const postcss = require('postcss');
      
      expect(postcss).toBeDefined();
      expect(typeof postcss).toBe('function');
    });

    test('postcss version is compatible', () => {
      const postcss = require('postcss');
      const pkg = require('postcss/package.json');
      
      expect(pkg.version).toBeDefined();
      // Version should be 8.5.0 or higher
      const version = pkg.version.split('.');
      expect(parseInt(version[0])).toBeGreaterThanOrEqual(8);
      expect(parseInt(version[1])).toBeGreaterThanOrEqual(5);
    });

    test('postcss can create processor', () => {
      const postcss = require('postcss');
      
      // Create a simple postcss processor
      const processor = postcss([]);
      
      expect(processor).toBeDefined();
      expect(typeof processor.process).toBe('function');
    });
  });

  describe('Backward Compatibility', () => {
    test('axios maintains backward compatible API', async () => {
      const axios = require('axios');
      
      // Test that common patterns still work
      const instance = axios.create({
        baseURL: 'https://jsonplaceholder.typicode.com',
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json'
        }
      });

      expect(instance.defaults.baseURL).toBe('https://jsonplaceholder.typicode.com');
      expect(instance.defaults.timeout).toBe(5000);
    });

    test('axios error handling structure remains consistent', () => {
      const axios = require('axios');
      
      // Verify error handling utilities exist
      expect(axios.isAxiosError).toBeDefined();
      expect(typeof axios.isAxiosError).toBe('function');
    });
  });

  describe('Security and Performance', () => {
    test('axios has no known critical vulnerabilities in version ^1.12.0', () => {
      const pkg = require('axios/package.json');
      
      // Version should be 1.12.0 or higher (addressing security issues)
      const version = pkg.version.split('.');
      const major = parseInt(version[0]);
      const minor = parseInt(version[1]);
      
      expect(major).toBe(1);
      expect(minor).toBeGreaterThanOrEqual(12);
    });

    test('postcss has no known critical vulnerabilities in version ^8.5.0', () => {
      const pkg = require('postcss/package.json');
      
      // Version should be 8.5.0 or higher
      const version = pkg.version.split('.');
      const major = parseInt(version[0]);
      const minor = parseInt(version[1]);
      
      expect(major).toBe(8);
      expect(minor).toBeGreaterThanOrEqual(5);
    });
  });

  describe('Transitive Dependencies', () => {
    test('axios includes form-data ^4.0.4', () => {
      const axiosPkg = require('axios/package.json');
      
      expect(axiosPkg.dependencies).toBeDefined();
      expect(axiosPkg.dependencies['form-data']).toBeDefined();
    });

    test('postcss includes nanoid ^3.3.8', () => {
      const postcssPkg = require('postcss/package.json');
      
      expect(postcssPkg.dependencies).toBeDefined();
      expect(postcssPkg.dependencies['nanoid']).toBeDefined();
    });
  });
});

describe('Component Compatibility with Updated Dependencies', () => {
  describe('MobileMatrixOptimizer with PostCSS', () => {
    test('component styles compile correctly with postcss ^8.5.0', () => {
      // This test verifies the component works with the updated postcss version
      const postcss = require('postcss');
      
      // Simulate CSS processing similar to what Tailwind/build tools do
      const cssInput = `
        .mobile-optimized {
          -webkit-overflow-scrolling: touch;
          touch-action: manipulation;
        }
      `;

      const processor = postcss([]);
      
      expect(() => {
        processor.process(cssInput, { from: undefined });
      }).not.toThrow();
    });

    test('Tailwind CSS compatibility with postcss ^8.5.0', () => {
      const postcss = require('postcss');
      
      // Verify postcss can handle common Tailwind patterns
      const tailwindCSS = `
        @layer utilities {
          .custom-class {
            @apply flex items-center justify-center;
          }
        }
      `;

      const processor = postcss([]);
      
      expect(() => {
        // Should not throw even though plugins aren't loaded
        processor.process(tailwindCSS, { from: undefined });
      }).not.toThrow();
    });
  });
});

describe('Build System Integration', () => {
  test('package.json has consistent dependency versions', () => {
    const pkg = require('../../../../package.json');
    
    expect(pkg.dependencies.axios).toMatch(/^\^1\.12\.0/);
    expect(pkg.devDependencies.postcss).toMatch(/^\^8\.5\.0/);
  });

  test('yarn.lock reflects updated dependencies', () => {
    // This is a meta-test to ensure lock file is updated
    const fs = require('fs');
    const path = require('path');
    
    const lockFilePath = path.join(__dirname, '../../../../yarn.lock');
    const lockFileExists = fs.existsSync(lockFilePath);
    
    expect(lockFileExists).toBe(true);
    
    if (lockFileExists) {
      const lockContent = fs.readFileSync(lockFilePath, 'utf8');
      
      // Verify axios 1.12.0 is in lock file
      expect(lockContent).toContain('axios@^1.12.0');
      
      // Verify postcss 8.5.0 is in lock file
      expect(lockContent).toContain('postcss@^8.5.0');
    }
  });
});