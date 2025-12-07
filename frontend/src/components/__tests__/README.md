# MobileMatrixOptimizer Component Tests

## Overview
Comprehensive unit tests for the MobileMatrixOptimizer React component, covering mobile detection, responsive behavior, touch support, and performance optimizations.

## Test Coverage

### 1. Mobile/Desktop Detection (8 tests)
- Desktop environment detection
- Mobile detection by screen width (≤768px)
- Mobile detection by User-Agent (iPhone, Android, iPad)
- Boundary case testing at 768px
- Dynamic resize detection

### 2. Orientation Handling (6 tests)
- Portrait vs landscape detection
- Square screen handling
- Dynamic orientation changes
- Orientation CSS class application

### 3. Touch Support Detection (5 tests)
- Touch capability detection via ontouchstart
- Touch detection via navigator.maxTouchPoints
- Non-touch device handling
- Touch CSS class application

### 4. CSS Style Injection (7 tests)
- Verification that style tags no longer use `jsx` attribute (fix for React warnings)
- Mobile-specific CSS injection
- Responsive text scaling
- Grid layout optimizations
- Touch target sizing (44px minimum)

### 5. Performance Optimizations (4 tests)
- CSS custom property management
- Opacity settings for mobile vs desktop
- Performance monitor display (localhost only)

### 6. Custom Hooks (6 tests)
- useMobile hook functionality
- Resize event handling
- Event listener cleanup
- Breakpoint accuracy

### 7. Component Exports (6 tests)
- MobileMatrixRain component
- MobileMatrixText component
- Animation and styling
- className prop handling

### 8. Edge Cases (8+ tests)
- Null/undefined children handling
- Rapid resize events
- Multiple component instances
- Event listener cleanup
- Accessibility preservation

## Running Tests

```bash
# Run all tests
cd frontend
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- MobileMatrixOptimizer.test.jsx
```

## Required Dependencies

The tests require the following packages (already included in package.json):
- @testing-library/react
- @testing-library/jest-dom
- @testing-library/user-event
- jest (via react-scripts)

## Test Structure

Each test follows the Arrange-Act-Assert pattern:
1. **Arrange**: Set up test conditions (mock window dimensions, user agent, etc.)
2. **Act**: Render component or trigger actions
3. **Assert**: Verify expected behavior

## Important Changes Tested

### JSX Attribute Fix
The tests verify that the component no longer uses the `jsx` attribute on `<style>` tags, which was causing React warnings. The fix changed:
```jsx
// Before (caused warnings)
<style jsx>{`...`}</style>

// After (fixed)
<style>{`...`}</style>
```

All style tag tests now verify that `hasAttribute('jsx')` returns `false`.

## Continuous Integration

These tests are designed to run in CI/CD pipelines and include:
- Comprehensive coverage of all component features
- Edge case handling
- Performance and accessibility checks
- Mock cleanup between tests

## Maintenance

When updating the MobileMatrixOptimizer component:
1. Update corresponding tests for changed functionality
2. Add new tests for new features
3. Ensure test coverage remains above 80%
4. Run full test suite before committing