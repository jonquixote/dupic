# Tests

This directory contains all test scripts for the AI Social Media Manager project.

## Directory Structure

- `unit/` - Unit tests for individual components and modules
- `integration/` - Integration tests for API endpoints and workflows

## Test Files

### Unit Tests
- `verify_implementation.py` - Verification script for new modules and imports

### Integration Tests
- `test_endpoints.py` - API endpoint testing script

## Test Runner
- `run_tests.py` - Script to run all tests

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Unit Tests
```bash
python tests/unit/verify_implementation.py
```

### Integration Tests
```bash
# Start the backend server first
cd social-media-manager-app
python app.py

# Then run the tests in another terminal
python tests/integration/test_endpoints.py
```

## Test Coverage

### Current Coverage
- Module import verification
- File existence checks
- API endpoint testing (when server is running)

### Planned Coverage
- Full API endpoint testing
- Service layer unit tests
- Route handler tests
- Database operation tests
- Security feature tests
- Frontend component tests