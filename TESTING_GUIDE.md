# Testing Guide - Comprehensive Test Suite

## Overview

This repository now includes comprehensive unit tests for the files modified in this branch:

1. **Backend**: `backend/config.py` - Configuration management with CORS updates
2. **Frontend**: `frontend/src/components/MobileMatrixOptimizer.jsx` - Mobile optimization component

## Quick Start

### Backend Tests

```bash
# Navigate to project root
cd /home/jailuser/git

# Install pytest (already in requirements.txt)
pip install -r backend/requirements.txt

# Run all config tests
python -m pytest backend/tests/test_config.py -v

# Run with coverage
python -m pytest backend/tests/test_config.py --cov=backend.config --cov-report=html

# Run specific test
python -m pytest backend/tests/test_config.py::TestCORSConfiguration::test_cors_preview_url_updated -v
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (includes testing libraries)
yarn install

# Run all tests
yarn test

# Run tests with coverage
yarn test --coverage --watchAll=false

# Run specific test file
yarn test MobileMatrixOptimizer

# Run in watch mode for development
yarn test --watch
```

## Test Files Created

### Backend Tests
- **File**: `backend/tests/test_config.py`
- **Lines**: 600+
- **Tests**: 60+
- **Coverage**: Configuration settings, CORS, environment variables

### Frontend Tests
- **File**: `frontend/src/components/__tests__/MobileMatrixOptimizer.test.jsx`
- **Lines**: 1400+
- **Tests**: 100+
- **Coverage**: Mobile detection, orientation, touch support, style injection

### Supporting Files
- **File**: `frontend/src/setupTests.js`
- **Purpose**: Jest configuration and browser API mocks

## What's Being Tested

### Backend (config.py)

#### Core Configuration
- ✅ Database settings (MongoDB URL, database name)
- ✅ Email configuration (SendGrid, sender addresses)
- ✅ AI settings (OpenAI, models, providers)
- ✅ Security settings (JWT, secrets)
- ✅ File upload limits and allowed types
- ✅ Rate limiting configuration

#### CORS Configuration (Critical Changes)
- ✅ **Updated preview URL**: `https://create-25.preview.emergentagent.com`
- ✅ Production URL unchanged: `https://fix-it-6.emergent.host`
- ✅ Localhost included for development
- ✅ No trailing slashes in URLs
- ✅ Proper URL formatting (http/https)

#### Environment Variable Handling
- ✅ All settings can be overridden by environment variables
- ✅ Default values when no env vars set
- ✅ Case-insensitive boolean handling
- ✅ List parsing from comma-separated strings

### Frontend (MobileMatrixOptimizer.jsx)

#### Style Tag Migration (Critical Changes)
- ✅ **Changed from `<style jsx>` to `<style>`** (3 occurrences)
- ✅ Styles properly injected on mobile devices
- ✅ No jsx attribute on style tags
- ✅ All style content preserved

#### Mobile Detection
- ✅ Width-based detection (≤768px = mobile)
- ✅ User agent detection (iPhone, Android, iPad, BlackBerry, etc.)
- ✅ Combined detection logic
- ✅ Desktop vs mobile classification

#### Responsive Behavior
- ✅ Portrait orientation detection (height > width)
- ✅ Landscape orientation detection (width > height)
- ✅ Touch support detection (ontouchstart, maxTouchPoints)
- ✅ CSS custom property updates (--matrix-effects-opacity)

#### Components and Hooks
- ✅ Main MobileMatrixOptimizer component
- ✅ useMobile custom hook
- ✅ MobileMatrixRain sub-component
- ✅ MobileMatrixText sub-component

#### Event Handling
- ✅ Resize event listeners
- ✅ Orientation change listeners
- ✅ Proper cleanup on unmount
- ✅ Rapid resize handling

#### Performance Monitor
- ✅ Shows on localhost/127.0.0.1 only
- ✅ Displays mobile status, touch support, orientation
- ✅ Hidden in production environments

## Test Execution Examples

### Backend Examples

```bash
# Run all tests with verbose output
python -m pytest backend/tests/test_config.py -vv

# Run only CORS tests
python -m pytest backend/tests/test_config.py::TestCORSConfiguration -v

# Run with markers (if defined)
python -m pytest backend/tests/test_config.py -m "cors" -v

# Show print statements
python -m pytest backend/tests/test_config.py -s

# Stop on first failure
python -m pytest backend/tests/test_config.py -x

# Generate HTML coverage report
python -m pytest backend/tests/test_config.py --cov=backend.config --cov-report=html
# Then open htmlcov/index.html in browser
```

### Frontend Examples

```bash
# Run all tests
yarn test --watchAll=false

# Run specific test suite
yarn test --testNamePattern="Mobile Detection"

# Run specific test file
yarn test MobileMatrixOptimizer.test.jsx

# Watch mode with coverage
yarn test --coverage --watch

# Update snapshots (if any)
yarn test -u

# Run in CI mode
CI=true yarn test --coverage
```

## Coverage Reports

### Backend Coverage
Expected coverage for `backend/config.py`:
- **Target**: >90%
- **Statements**: All configuration properties tested
- **Branches**: Environment variable overrides tested
- **Functions**: Settings class instantiation tested

View coverage:
```bash
python -m pytest backend/tests/test_config.py --cov=backend.config --cov-report=term-missing
```

### Frontend Coverage
Expected coverage for `MobileMatrixOptimizer.jsx`:
- **Target**: >85%
- **Statements**: All code paths tested
- **Branches**: Mobile/desktop, portrait/landscape, touch/no-touch
- **Functions**: All hooks and handlers tested

View coverage:
```bash
yarn test --coverage --watchAll=false
# Coverage report saved to coverage/lcov-report/index.html
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      - name: Run backend tests
        run: |
          python -m pytest backend/tests/test_config.py --cov=backend.config --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: yarn install
      - name: Run frontend tests
        working-directory: ./frontend
        run: yarn test --coverage --watchAll=false
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Debugging Failing Tests

### Backend Debugging

**Test fails due to import error:**
```bash
# Ensure you're running from project root
cd /home/jailuser/git
python -m pytest backend/tests/test_config.py -v
```

**Test fails due to environment variable:**
```bash
# Check current environment
python -c "import os; print(os.getenv('CORS_ORIGINS'))"

# Run with clean environment
env -i python -m pytest backend/tests/test_config.py -v
```

### Frontend Debugging

**Tests fail with "Cannot find module":**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules yarn.lock
yarn install
yarn test
```

**Tests timeout:**
```bash
# Increase timeout
yarn test --testTimeout=10000
```

**Async state updates warning:**
```bash
# Already handled with waitFor() in tests
# Check test output for specific component issues
```

## Test Maintenance

### When to Update Backend Tests
- Adding new configuration properties → Add to TestSettings
- Changing CORS origins → Update TestCORSConfiguration
- Modifying environment variable names → Update relevant tests
- Changing default values → Update assertions

### When to Update Frontend Tests
- Changing mobile detection logic → Update detection tests
- Modifying breakpoints → Update responsive tests
- Adding new style injections → Add style validation tests
- Changing component props → Update component tests

## Common Issues & Solutions

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'backend'`
```bash
# Solution: Run from project root with proper Python path
cd /home/jailuser/git
PYTHONPATH=. python -m pytest backend/tests/test_config.py -v
```

**Issue**: Tests pass locally but fail in CI
```bash
# Solution: Check environment variables in CI
# Ensure .env file is not committed
# Use CI environment variable configuration
```

### Frontend Issues

**Issue**: `ReferenceError: window is not defined`
```bash
# Solution: Ensure setupTests.js is loaded
# Check test configuration in package.json
# Verify jest.config.js or craco.config.js
```

**Issue**: Tests fail with style tag assertions
```bash
# Solution: Ensure testing-library is properly configured
# Check that style tag removal (jsx attribute) is tested
# Verify querySelector is finding injected styles
```

## Best Practices

### Writing New Tests

1. **Descriptive Names**: Test names should describe what they verify
   ```javascript
   test('applies mobile-optimized class when width is 768px or less', ...)
   ```

2. **Arrange-Act-Assert**: Follow AAA pattern
   ```javascript
   // Arrange
   mockWindowProperties(375, 667);
   
   // Act
   render(<MobileMatrixOptimizer>...</MobileMatrixOptimizer>);
   
   // Assert
   expect(container.firstChild).toHaveClass('mobile-optimized');
   ```

3. **Isolation**: Each test should be independent
   ```javascript
   beforeEach(() => {
     // Reset state
     jest.clearAllMocks();
   });
   ```

4. **Edge Cases**: Test boundaries and error conditions
   ```javascript
   test('handles undefined children gracefully', ...)
   test('handles missing navigator.userAgent', ...)
   ```

## Documentation

For more detailed information, see:
- `TEST_DOCUMENTATION.md` - Comprehensive testing documentation
- `TEST_SUMMARY.md` - Summary of tests created
- Individual test files for inline documentation

## Questions?

If you encounter issues:
1. Check test output for specific error messages
2. Review test documentation files
3. Verify dependencies are installed
4. Check that you're running commands from correct directory
5. Ensure environment is properly configured

## Test Statistics

- **Total Test Files**: 3 (backend + frontend + setup)
- **Total Tests**: 160+
- **Backend Tests**: 60+
- **Frontend Tests**: 100+
- **Lines of Test Code**: 2000+
- **Code Coverage Target**: >85%
- **Files Tested**: 2 (config.py, MobileMatrixOptimizer.jsx)
- **Critical Changes Tested**: ✅ CORS URL update, ✅ Style tag migration

---

**Happy Testing! 🧪**