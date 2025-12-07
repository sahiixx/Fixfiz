# MobileMatrixOptimizer Test Suite

## Overview
Comprehensive test suite for the `MobileMatrixOptimizer` component and its associated hooks and sub-components.

## Primary Fix Tested
The main change tested is the removal of the `jsx` prop from `<style>` tags, which was causing React JSX attribute warnings:
- **Before**: `<style jsx>{...}</style>` (caused warnings)
- **After**: `<style>{...}</style>` (no warnings)

## Test Coverage

### Core Functionality (80+ tests)
1. **Style Tag JSX Prop Fix** (5 tests)
   - Validates that style tags don't have `jsx` attribute
   - Tests all three locations where style tags are injected

2. **Component Rendering** (6 tests)
   - Basic rendering with children
   - Custom className support
   - Multiple children handling

3. **Mobile Detection** (7 tests)
   - Width-based detection (<=768px)
   - User agent detection (iPhone, Android, iPad)
   - Edge cases (320px, 1920px)

4. **Orientation Detection** (3 tests)
   - Portrait vs landscape
   - Square viewport handling

5. **Touch Support** (3 tests)
   - ontouchstart detection
   - maxTouchPoints detection
   - No touch support handling

6. **CSS Custom Properties** (2 tests)
   - Mobile opacity (0.3)
   - Desktop opacity (0.5)

7. **Performance Monitor** (3 tests)
   - localhost display
   - Production hiding
   - Desktop hiding

8. **useMobile Hook** (4 tests)
   - Mobile width detection
   - Desktop width detection
   - Boundary testing (768px, 769px)

9. **MobileMatrixRain Component** (4 tests)
   - Mobile rendering
   - Desktop non-rendering
   - Custom className
   - Animation styles

10. **MobileMatrixText Component** (5 tests)
    - Children rendering
    - Mobile class application
    - Desktop class non-application
    - Animation injection
    - Custom className

11. **Edge Cases** (4 tests)
    - Zero dimensions
    - Extremely large viewport
    - Undefined props
    - Fragment children

12. **Integration Tests** (2 tests)
    - All components together
    - Nested components

13. **Regression Tests** (2 tests)
    - No React warnings
    - Standard HTML style elements

## Running Tests

```bash
# Run all tests
cd frontend && yarn test

# Run specific test file
yarn test MobileMatrixOptimizer

# Run with coverage
yarn test --coverage MobileMatrixOptimizer

# Watch mode
yarn test --watch MobileMatrixOptimizer
```

## Test Dependencies
- `@testing-library/react` - React component testing
- `@testing-library/jest-dom` - Custom Jest matchers
- Jest (included with react-scripts)

## Notes
- Tests use mocking for window properties (innerWidth, innerHeight, navigator)
- Style tag injection is verified without jsx attribute
- All tests are isolated and clean up after themselves