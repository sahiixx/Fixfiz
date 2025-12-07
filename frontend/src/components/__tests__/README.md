# MobileMatrixOptimizer Test Suite

## Overview
This directory contains comprehensive unit and integration tests for the `MobileMatrixOptimizer` component and related functionality, including tests for the critical JSX styling fix.

## Test Files

### MobileMatrixOptimizer.test.jsx
Comprehensive tests for the main component and its sub-components:
- **MobileMatrixOptimizer**: Main wrapper component with mobile optimization
- **MobileMatrixRain**: Animated background effect component
- **MobileMatrixText**: Typography optimization component

#### Key Test Coverage:
1. **Component Rendering** (15+ tests)
   - Children rendering
   - ClassName prop application
   - Default prop handling
   - Null/undefined handling

2. **JSX Styling Fix Validation** (Critical - 8+ tests)
   - Validates `<style>` tags do not have `jsx` attribute
   - Regression tests for React JSX attribute warnings
   - Mobile vs desktop style tag rendering
   - CSS content validation

3. **Mobile Detection** (10+ tests)
   - Window.matchMedia mocking and testing
   - Mobile vs desktop behavior
   - Viewport change handling
   - Orientation change support

4. **Responsive Behavior** (8+ tests)
   - Dynamic viewport changes
   - Orientation updates
   - Rerender stability

5. **Accessibility** (5+ tests)
   - Semantic HTML structure
   - ARIA attribute preservation
   - Role-based element queries

6. **Performance** (4+ tests)
   - Efficient rendering with many children
   - Memory leak prevention
   - Style injection optimization

7. **Integration Tests** (6+ tests)
   - Multi-component interaction
   - Nested component structure
   - Edge cases and error handling

### DependencyUpdate.integration.test.js
Integration tests for package.json dependency updates:
- **Axios ^1.8.4 → ^1.12.0**: API compatibility, security improvements
- **PostCSS ^8.4.49 → ^8.5.0**: Build system compatibility, Tailwind CSS support

#### Key Test Coverage:
1. **Axios Version Update** (10+ tests)
   - Import and API availability
   - Method signatures (get, post, put, delete, patch, create)
   - Interceptors support
   - FormData compatibility
   - Error handling utilities

2. **PostCSS Version Update** (6+ tests)
   - Module import validation
   - API compatibility
   - Version verification
   - CSS processing capabilities

3. **Security Validation** (4+ tests)
   - Version number verification
   - Known vulnerability checks

4. **Build System Integration** (3+ tests)
   - package.json consistency
   - yarn.lock update validation

## Running Tests

### Run all tests:
```bash
npm test
# or
yarn test
```

### Run specific test file:
```bash
npm test MobileMatrixOptimizer.test.jsx
# or
yarn test MobileMatrixOptimizer.test.jsx
```

### Run with coverage:
```bash
npm test -- --coverage
# or
yarn test --coverage
```

### Watch mode (for development):
```bash
npm test -- --watch
# or
yarn test --watch
```

## Test Utilities and Mocks

### Window.matchMedia Mock
```javascript
const mockMatchMedia = (matches = false) => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches: matches,
      media: query,
      // ... other properties
    })),
  });
};
```

### Screen Orientation Mock
```javascript
const mockOrientation = (type = 'landscape-primary', angle = 0) => {
  Object.defineProperty(window.screen, 'orientation', {
    writable: true,
    value: {
      type: type,
      angle: angle,
      // ... event listeners
    },
  });
};
```

## Critical Regression Tests

### JSX Attribute Warning Fix
The most important tests validate that the fix for React JSX attribute warnings is working:

```javascript
test('style tag does not have jsx attribute (regression test)', () => {
  // ... test implementation
  expect(styleTag.hasAttribute('jsx')).toBe(false);
});
```

This test ensures that the change from `<style jsx>` to `<style>` has eliminated the console warning: