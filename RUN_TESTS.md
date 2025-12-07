# Test Execution Guide

This guide explains how to run all the unit tests generated for the git diff changes.

## Prerequisites

### Backend Tests (Python)
```bash
# Ensure pytest is installed
pip install pytest pytest-cov
```

### Frontend Tests (React/Jest)
```bash
cd frontend

# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom jest babel-jest @babel/preset-env @babel/preset-react identity-obj-proxy

# Or with yarn
yarn add --dev @testing-library/react @testing-library/jest-dom jest babel-jest @babel/preset-env @babel/preset-react identity-obj-proxy
```

## Running Backend Tests

### Run all backend tests:
```bash
cd /home/jailuser/git

# Run with verbose output
python -m pytest tests/test_config_cors_update.py -v
python -m pytest tests/test_gitignore_validation.py -v

# Run all backend tests at once
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=backend --cov-report=html --cov-report=term
```

### Run specific test class:
```bash
# Run only CORS configuration tests
python -m pytest tests/test_config_cors_update.py::TestCORSConfiguration -v

# Run only URL update tests
python -m pytest tests/test_config_cors_update.py::TestURLUpdates -v
```

## Running Frontend Tests

### Run all frontend tests:
```bash
cd /home/jailuser/git/frontend

# Run all tests
npm test

# Or with yarn
yarn test
```

### Run specific test files:
```bash
# Run MobileMatrixOptimizer tests only
npm test MobileMatrixOptimizer.test.jsx

# Run dependency integration tests only
npm test DependencyUpdate.integration.test.js
```

### Run with coverage:
```bash
# Generate coverage report
npm test -- --coverage --watchAll=false

# Or with yarn
yarn test --coverage --watchAll=false
```

### Watch mode (for development):
```bash
# Run tests in watch mode
npm test -- --watch

# Or with yarn
yarn test --watch
```

## Test File Locations

### Backend Tests:
- `tests/test_config_cors_update.py` - CORS configuration tests (23 tests)
- `tests/test_gitignore_validation.py` - Git ignore validation tests (20 tests)

### Frontend Tests:
- `frontend/src/components/__tests__/MobileMatrixOptimizer.test.jsx` - Component tests (70+ tests)
- `frontend/src/components/__tests__/DependencyUpdate.integration.test.js` - Dependency tests (27 tests)

## Expected Test Results

### Backend Tests: