# LingoDash Test Suite Documentation

## Overview

This test suite provides comprehensive coverage for the LingoDash Streamlit application, including unit tests, integration tests, and edge case scenarios.

## Test Structure

```
tests/
├── test_load_and_charts.py    # Original tests for data loading and basic charts
├── test_comprehensive.py       # Comprehensive unit tests for all functions
├── test_edge_cases.py         # Edge cases, error handling, and stress tests
├── requirements-test.txt       # Testing dependencies
└── README.md                  # This file
```

## Running Tests

### Quick Start

```bash
# Run all tests
python run_tests.py

# Or using pytest directly
pytest tests/ -v
```

### Running Specific Test Files

```bash
# Run only data loading tests
pytest tests/test_load_and_charts.py -v

# Run only comprehensive tests
pytest tests/test_comprehensive.py -v

# Run only edge case tests
pytest tests/test_edge_cases.py -v
```

### Running with Coverage

```bash
# Generate coverage report
pytest --cov=streamlit_app --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Running Tests in Parallel

```bash
# Requires pytest-xdist
pytest -n auto tests/
```

## Test Categories

### 1. Data Loading Tests (`test_load_and_charts.py`)
- ✅ CSV file loading and column validation
- ✅ Error handling for missing files
- ✅ Data type validation
- ✅ Calculated column verification

### 2. Visualization Tests
- ✅ Chart creation and structure
- ✅ Color palette compliance
- ✅ Accessibility attributes
- ✅ Performance benchmarks (<1s per chart)

### 3. UI Component Tests (`test_comprehensive.py`)
- ✅ Metric card generation
- ✅ Insight box creation
- ✅ Export button functionality
- ✅ Loading state displays

### 4. Edge Case Tests (`test_edge_cases.py`)
- ✅ NaN and missing data handling
- ✅ Extreme value scenarios
- ✅ Unicode and special characters
- ✅ Large dataset performance
- ✅ Empty data handling

### 5. Integration Tests
- ✅ Full visualization pipeline
- ✅ UI component integration
- ✅ Data consistency across modules

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only performance tests
pytest -m performance
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
# Run tests with XML output for CI systems
pytest --junitxml=test-results.xml

# Run with coverage and fail if below threshold
pytest --cov=streamlit_app --cov-fail-under=80
```

## Writing New Tests

When adding new features, ensure:

1. **Unit tests** for individual functions
2. **Integration tests** for feature workflows
3. **Edge case tests** for error scenarios
4. **Performance tests** for scalability

Example test structure:

```python
def test_new_feature():
    """Test description"""
    # Arrange
    test_data = create_test_data()
    
    # Act
    result = function_under_test(test_data)
    
    # Assert
    assert result.expected_property == expected_value
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're in the project root or virtual environment
2. **Missing dependencies**: Run `pip install -r tests/requirements-test.txt`
3. **Data file errors**: Ensure CSV files exist in `data/` directory

### Debug Mode

Run tests with more verbose output:

```bash
pytest -vvs tests/  # Very verbose with stdout
pytest --pdb tests/  # Drop into debugger on failure
```

## Coverage Goals

- Overall coverage: >80%
- Critical functions: 100%
- UI components: >90%
- Error handling: 100%

## Performance Benchmarks

- Chart generation: <1s per chart
- Data loading: <2s for all files
- UI rendering: <100ms per component
- Large dataset handling: <5s for 1000 rows