# MobileMatrixOptimizer Tests

## Overview
This directory contains comprehensive unit tests for the `MobileMatrixOptimizer` component and its related exports.

## What Changed
The component was updated to fix JSX attribute warnings by replacing `<style jsx>` tags with standard `<style>` tags. This change eliminates React warnings while maintaining all functionality.

### Before (Problematic):
```jsx
<style jsx>{`...`}</style>
```

### After (Fixed):
```jsx
<style>{`...`}</style>
```

## Test Coverage

### Main Component Tests
- ✅ Component rendering with children
- ✅ Custom className application
- ✅ Mobile detection (viewport width ≤768px)
- ✅ Mobile detection (user agent)
- ✅ Orientation detection (portrait/landscape)
- ✅ Touch support detection
- ✅ Style injection without JSX attribute warnings
- ✅ Performance monitor (localhost only)
- ✅ Event listener setup and cleanup
- ✅ CSS custom properties for effects

### useMobile Hook Tests
- ✅ Returns correct values for desktop/mobile
- ✅ Updates on window resize
- ✅ Cleanup on unmount

### MobileMatrixRain Component Tests
- ✅ Renders only on mobile
- ✅ Custom className support
- ✅ Animation styles without JSX attribute
- ✅ Correct opacity and pointer-events

### MobileMatrixText Component Tests
- ✅ Renders children correctly
- ✅ Mobile-specific styling
- ✅ Responsive text scaling
- ✅ Glow animations

### Edge Cases
- ✅ Missing/undefined children
- ✅ Rapid viewport changes
- ✅ Multiple style elements

### Integration Tests
- ✅ All mobile optimizations together
- ✅ Multiple exported components working together

## Running Tests

### Install dependencies:
```bash
cd frontend
yarn install
```

### Run all tests:
```bash
yarn test
```

### Run tests in watch mode:
```bash
yarn test --watch
```

### Run with coverage:
```bash
yarn test --coverage
```

### Run specific test file:
```bash
yarn test MobileMatrixOptimizer
```

## Key Test Scenarios

### 1. JSX Attribute Fix Verification
The tests verify that:
- Style elements are created without `jsx` attribute
- No React warnings are generated
- All CSS content is properly injected
- Functionality remains identical to previous version

### 2. Responsive Behavior
Tests cover:
- Desktop viewport (>768px)
- Mobile viewport (≤768px)
- Tablet breakpoint (exactly 768px)
- Portrait vs landscape orientation
- Touch vs non-touch devices

### 3. Performance
- Verifies CSS custom properties are set correctly
- Confirms animations use optimized mobile versions
- Tests that performance monitor only shows in development

## Dependencies Required

The tests require these packages (already added to package.json):
- `@testing-library/react` - React component testing utilities
- `@testing-library/jest-dom` - Custom jest matchers for DOM
- `@testing-library/user-event` - User interaction simulation

## Notes

1. **Window Mocking**: Tests mock `window.innerWidth`, `window.innerHeight`, and `navigator.userAgent` to simulate different devices.

2. **Async Behavior**: Many tests use `waitFor` to handle React's asynchronous state updates.

3. **Event Cleanup**: Tests verify that event listeners are properly removed on component unmount to prevent memory leaks.

4. **Isolation**: Each test resets window properties to ensure test isolation.

## Troubleshooting

### Tests fail with "Not implemented: HTMLCanvasElement.prototype.getContext"
This is expected in jsdom environment. Add canvas mock if needed.

### Tests fail with matchMedia errors
The `setupTests.js` file includes matchMedia mock. Ensure it's being loaded.

### Style injection tests failing
Verify that React is rendering the component fully before checking for style elements.

## Future Improvements

- Add visual regression tests
- Add accessibility tests (a11y)
- Add performance benchmarks
- Test with actual mobile devices using Playwright/Cypress