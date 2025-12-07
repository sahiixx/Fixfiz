/**
 * Setup file for Jest tests
 * Configures testing environment and global test utilities
 */

// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
import '@testing-library/jest-dom';

// Mock window.matchMedia if not available
if (!window.matchMedia) {
  window.matchMedia = (query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  });
}

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock screen.orientation
if (!window.screen.orientation) {
  Object.defineProperty(window.screen, 'orientation', {
    value: {
      type: 'landscape-primary',
      angle: 0,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    },
    writable: true,
  });
}

// Suppress console warnings in tests unless explicitly needed
const originalWarn = console.warn;
const originalError = console.error;

beforeAll(() => {
  console.warn = jest.fn((...args) => {
    // Filter out known warnings we don't want to see in tests
    const message = args[0];
    if (
      typeof message === 'string' &&
      (message.includes('Warning: ReactDOM.render') ||
       message.includes('Warning: useLayoutEffect'))
    ) {
      return;
    }
    originalWarn(...args);
  });

  console.error = jest.fn((...args) => {
    // Filter out known errors we don't want to see in tests
    const message = args[0];
    if (
      typeof message === 'string' &&
      message.includes('Not implemented: HTMLFormElement.prototype.submit')
    ) {
      return;
    }
    originalError(...args);
  });
});

afterAll(() => {
  console.warn = originalWarn;
  console.error = originalError;
});

// Global test utilities
global.waitFor = async (callback, options = {}) => {
  const { timeout = 1000, interval = 50 } = options;
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    try {
      const result = callback();
      if (result) return result;
    } catch (error) {
      // Continue waiting
    }
    await new Promise(resolve => setTimeout(resolve, interval));
  }

  throw new Error('Timeout waiting for condition');
};