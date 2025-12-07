# Component Tests

This directory contains unit tests for React components.

## Running Tests

```bash
# Run all tests
yarn test

# Run tests in watch mode
yarn test --watch

# Run tests with coverage
yarn test --coverage

# Run specific test file
yarn test MobileMatrixOptimizer.test.jsx
```

## Test Structure

### MobileMatrixOptimizer.test.jsx
Comprehensive tests for the MobileMatrixOptimizer component family:
- Main MobileMatrixOptimizer component (30+ tests)
- useMobile hook (6+ tests)
- MobileMatrixRain component (7+ tests)
- MobileMatrixText component (10+ tests)
- Edge cases and integration tests (15+ tests)

**Total: 68+ test cases**

## Test Coverage

The tests cover:
- Component rendering and props
- Mobile/desktop detection logic
- Orientation detection (portrait/landscape)
- Touch support detection
- Event handling (resize, orientation change)
- CSS class application
- Style injection
- Performance monitor display
- Custom hooks behavior
- Child component interactions
- Edge cases and error handling

## Testing Best Practices

1. **Descriptive test names**: Each test clearly describes what it's testing
2. **Arrange-Act-Assert pattern**: Tests follow AAA structure
3. **Isolation**: Each test is independent and can run in any order
4. **Mocking**: Window properties are mocked for consistent test behavior
5. **Cleanup**: Event listeners and mocks are properly cleaned up
6. **Coverage**: Tests cover happy paths, edge cases, and error conditions

## Adding New Tests

When adding new tests:
1. Follow existing naming conventions
2. Group related tests in describe blocks
3. Use beforeEach/afterEach for setup/cleanup
4. Mock external dependencies
5. Test both success and failure scenarios
6. Ensure tests are deterministic