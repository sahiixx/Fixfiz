# Test Documentation

This document describes the comprehensive test suites created for the modified files in this branch.

## Overview

Tests have been created for the following modified files:
1. `backend/config.py` - Configuration settings with CORS updates
2. `frontend/src/components/MobileMatrixOptimizer.jsx` - Mobile optimization component

## Backend Tests

### Location
`backend/tests/test_config.py`

### Test Coverage
- **Configuration Defaults**: Tests all default configuration values
- **Environment Variables**: Tests environment variable overrides
- **CORS Configuration**: Comprehensive tests for CORS origins, including the updated preview URL
- **Security Settings**: JWT configuration validation
- **File Upload Settings**: Validation of file size and type restrictions
- **Rate Limiting**: Tests for rate limiting configuration
- **Edge Cases**: Environment variable handling and validation

### Running Backend Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run all backend tests
cd backend
pytest tests/test_config.py -v

# Run with coverage
pytest tests/test_config.py --cov=config --cov-report=html

# Run specific test class
pytest tests/test_config.py::TestSettings -v

# Run specific test
pytest tests/test_config.py::TestSettings::test_cors_preview_url_updated -v
```

### Key Test Scenarios

#### CORS Configuration Tests
- Validates the updated preview URL: `https://create-25.preview.emergentagent.com`
- Ensures old URL is not present
- Tests multiple environment configurations (local, preview, production)
- Validates URL formatting (no trailing slashes, proper protocol)

#### Environment Variable Tests
- Tests with no environment variables (defaults)
- Tests with custom environment variables
- Tests invalid values
- Tests empty strings and edge cases

## Frontend Tests

### Location
`frontend/src/components/__tests__/MobileMatrixOptimizer.test.jsx`

### Test Coverage
- **Mobile Detection**: Screen width and user agent detection
- **Orientation Detection**: Portrait/landscape handling
- **Touch Support**: Touch capability detection
- **Style Injection**: Proper style tag usage (changed from styled-jsx)
- **Performance Monitor**: Localhost-only debug display
- **Responsive Behavior**: CSS custom properties and class application
- **Event Listeners**: Resize and orientation change handling
- **Hook Testing**: useMobile custom hook
- **Sub-components**: MobileMatrixRain and MobileMatrixText
- **Edge Cases**: Error handling and boundary conditions

### Prerequisites

Add the following dependencies to `frontend/package.json`:

```json
{
  "devDependencies": {
    "@testing-library/react": "^16.1.0",
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/user-event": "^14.5.2",
    "jest-environment-jsdom": "^29.7.0"
  }
}
```

### Running Frontend Tests

```bash
# Install dependencies
cd frontend
yarn install

# Run all tests
yarn test

# Run tests in watch mode
yarn test --watch

# Run tests with coverage
yarn test --coverage

# Run specific test file
yarn test MobileMatrixOptimizer.test.jsx

# Run specific test suite
yarn test --testNamePattern="Mobile Detection"
```

### Key Test Scenarios

#### Style Tag Migration
- Validates change from `<style jsx>` to `<style>`
- Ensures styles are properly injected
- Tests that jsx attribute is not present

#### Mobile Detection Tests
- Width-based detection (≤768px)
- User agent detection (iPhone, Android, iPad, etc.)
- Combined detection logic

#### Responsive Behavior
- Portrait vs landscape orientation
- Touch vs non-touch devices
- CSS custom property updates
- Class name composition

#### Performance Tests
- Event listener cleanup
- Rapid resize handling
- Memory leak prevention

## Test Metrics

### Backend Test Coverage
- **Total Tests**: 60+
- **Test Classes**: 3 (TestSettings, TestCORSConfiguration, TestEnvironmentVariableHandling)
- **Coverage Target**: >90% of config.py

### Frontend Test Coverage
- **Total Tests**: 100+
- **Test Suites**: 10 (Component, Hook, Sub-components, Edge Cases, etc.)
- **Coverage Target**: >85% of MobileMatrixOptimizer.jsx

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Recommended CI configuration:

### Backend CI
```yaml
- name: Run Backend Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pip install pytest pytest-cov
    pytest tests/test_config.py --cov=config --cov-report=xml
```

### Frontend CI
```yaml
- name: Run Frontend Tests
  run: |
    cd frontend
    yarn install
    yarn test --coverage --watchAll=false
```

## Test Maintenance

### When to Update Tests

1. **CORS Changes**: Update `TestCORSConfiguration` when modifying CORS origins
2. **Config Changes**: Update `TestSettings` when adding/modifying configuration
3. **Component Changes**: Update MobileMatrixOptimizer tests when modifying mobile detection logic
4. **Style Changes**: Update style-related tests when changing CSS injection method

### Best Practices

1. **Run tests before committing**: Ensure all tests pass
2. **Add tests for new features**: Maintain high coverage
3. **Test edge cases**: Include boundary conditions and error scenarios
4. **Keep tests isolated**: Each test should be independent
5. **Use descriptive names**: Test names should clearly describe what they test
6. **Mock external dependencies**: Use mocks for browser APIs and external services

## Debugging Tests

### Backend Debugging
```bash
# Run tests with verbose output
pytest tests/test_config.py -vv

# Run tests with print statements visible
pytest tests/test_config.py -s

# Run specific failing test
pytest tests/test_config.py::TestSettings::test_name -vv
```

### Frontend Debugging
```bash
# Run with debug output
DEBUG_PRINT_LIMIT=0 yarn test --no-coverage

# Run single test file in watch mode
yarn test MobileMatrixOptimizer.test.jsx --watch

# Run with verbose output
yarn test --verbose
```

## Common Issues and Solutions

### Backend Issues

**Issue**: Import errors for `backend.config`
- **Solution**: Ensure you're running tests from the correct directory and PYTHONPATH is set

**Issue**: Environment variable conflicts
- **Solution**: Tests use `@patch.dict(os.environ)` to isolate environment

### Frontend Issues

**Issue**: Window/navigator mocking errors
- **Solution**: `setupTests.js` provides comprehensive mocks

**Issue**: Async state updates
- **Solution**: Use `waitFor` from `@testing-library/react`

**Issue**: Style injection not detected
- **Solution**: Use `querySelector` to find injected style tags

## Contributing

When adding new tests:

1. Follow existing test structure and naming conventions
2. Group related tests in describe blocks
3. Use clear, descriptive test names
4. Include comments for complex test logic
5. Ensure tests are deterministic and repeatable
6. Add assertions that verify expected behavior
7. Test both happy paths and error conditions

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/react)
- [Jest Documentation](https://jestjs.io/)
- [Pydantic Testing](https://docs.pydantic.dev/latest/usage/settings/)