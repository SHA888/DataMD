# DataMD Testing Approach

## Overview

This document describes the testing strategy and best practices for the Data Markdown (DataMD) project. The testing approach is designed to ensure code quality, maintainability, and reliability across all features.

## Testing Strategy

### 1. Unit Testing

Unit tests focus on testing individual functions and classes in isolation. Each test should:

- Test a single function or method
- Use mock objects when dependencies are involved
- Cover both normal and edge cases
- Be fast and deterministic
- Follow the Arrange-Act-Assert pattern

#### Example Unit Test Structure:
```python
def test_sanitize_numeric_input():
    """Test sanitize_numeric_input function with valid input"""
    # Arrange
    value = "123.45"
    min_val = 0
    max_val = 1000

    # Act
    result = sanitize_numeric_input(value, min_val, max_val)

    # Assert
    assert result == 123.45
```

### 2. Integration Testing

Integration tests verify that different components work together correctly. These tests:

- Test the interaction between multiple components
- Use real dependencies where possible
- Cover end-to-end workflows
- Validate data flow between components

#### Example Integration Test Structure:
```python
def test_chart_shortcode_integration():
    """Test chart shortcode processing with real data"""
    # Arrange - Create test data and DMD file
    # Act - Process the DMD file
    # Assert - Verify the output contains expected elements
```

### 3. Performance Testing

Performance tests ensure that the system meets performance requirements:

- Benchmark critical operations
- Monitor memory usage
- Test with various data sizes
- Set performance thresholds

#### Example Performance Test Structure:
```python
@pytest.mark.benchmark
def test_csv_processing_performance():
    """Benchmark CSV processing performance"""
    # Arrange - Create test data
    # Act - Measure processing time and memory usage
    # Assert - Verify performance meets thresholds
```

### 4. Regression Testing

Regression tests ensure that new changes don't break existing functionality:

- Run the full test suite on every change
- Use CI/CD to automate testing
- Maintain test coverage above 80%
- Update tests when functionality changes

## Test Organization

### Directory Structure
```
tests/
├── unit/                 # Unit tests for individual functions
├── integration/          # Integration tests for component interaction
├── performance/          # Performance benchmarks
├── fixtures/             # Test data and fixtures
└── conftest.py          # pytest configuration
```

### Test File Naming Convention
- `test_<module>_unit.py` - Unit tests for a specific module
- `test_<feature>_integration.py` - Integration tests for a feature
- `test_<component>_performance.py` - Performance tests for a component

## Testing Tools

### Core Testing Framework
- **pytest** - Primary testing framework
- **pytest-cov** - Code coverage reporting
- **pytest-benchmark** - Performance benchmarking

### Mocking and Fixtures
- **unittest.mock** - Built-in mocking framework
- **pytest fixtures** - Test setup and teardown

### Code Quality Tools
- **black** - Code formatting
- **flake8** - Code linting
- **mypy** - Type checking
- **pre-commit** - Git hooks for code quality

## Test Coverage Requirements

### Minimum Coverage Thresholds
- **Overall Project**: 80%
- **Core Modules**: 90%
- **New Features**: 100%
- **Configuration Modules**: 85%

### Coverage Measurement
Coverage is measured using pytest-cov and reported to Codecov on every CI run.

## Continuous Integration

### GitHub Actions Workflow
The CI pipeline includes:

1. **Test Matrix**: Runs on multiple Python versions (3.8, 3.9, 3.10, 3.11)
2. **Dependency Installation**: Installs all required system and Python dependencies
3. **Unit Tests**: Runs all unit tests
4. **Integration Tests**: Runs all integration tests
5. **Performance Tests**: Runs performance benchmarks
6. **Code Quality Checks**: Runs linting and formatting checks
7. **Coverage Reporting**: Uploads coverage reports to Codecov

### Branch Protection
- All pull requests require passing CI checks
- Code coverage must not decrease significantly
- At least one approval required for merging

## Best Practices

### Writing Effective Tests

1. **Use Descriptive Test Names**
   ```python
   # Good
   def test_sanitize_chart_options_with_valid_input():

   # Bad
   def test_sanitize():
   ```

2. **Follow AAA Pattern**
   - **Arrange**: Set up test data and preconditions
   - **Act**: Execute the function under test
   - **Assert**: Verify the expected outcome

3. **Test One Thing**
   Each test should verify a single behavior or requirement.

4. **Use Appropriate Assertions**
   ```python
   # Good - Specific assertion
   assert result == expected_value

   # Bad - Generic boolean check
   assert is_valid(result) is True
   ```

5. **Handle Test Data Properly**
   - Use temporary directories for file operations
   - Clean up test data after tests
   - Use pytest fixtures for common setup

### Test Data Management

1. **Small Test Files**: Keep test data small and focused
2. **Generated Data**: Use code to generate test data when possible
3. **Shared Fixtures**: Use pytest fixtures for common test data
4. **External Data**: Store large test files separately and download when needed

### Performance Considerations

1. **Fast Tests**: Unit tests should run in milliseconds
2. **Parallel Execution**: Use pytest-xdist for parallel test execution
3. **Resource Management**: Clean up resources in teardown
4. **Benchmarking**: Regularly benchmark critical operations

## Test Maintenance

### When to Update Tests

1. **New Features**: Add comprehensive tests for new functionality
2. **Bug Fixes**: Add regression tests for fixed bugs
3. **Refactoring**: Update tests if behavior changes
4. **Performance Improvements**: Update benchmarks if thresholds change

### Test Review Process

1. **Peer Review**: All tests are reviewed during code review
2. **Coverage Analysis**: Check coverage reports for gaps
3. **Performance Monitoring**: Monitor benchmark results for regressions
4. **Documentation**: Update testing documentation when processes change

## Common Testing Patterns

### Mocking External Dependencies
```python
from unittest.mock import patch, Mock

@patch('module.external_function')
def test_with_mock(mock_function):
    mock_function.return_value = "mocked_result"
    # Test code that uses external_function
```

### Testing Exception Handling
```python
def test_function_raises_exception():
    with pytest.raises(ValueError):
        function_that_raises_value_error()
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input_value,expected", [
    ("123", 123),
    ("45.6", 45.6),
    ("invalid", None),
])
def test_sanitize_numeric_input(input_value, expected):
    result = sanitize_numeric_input(input_value)
    assert result == expected
```

## Troubleshooting

### Common Test Issues

1. **Flaky Tests**: Tests that sometimes pass and sometimes fail
   - Solution: Ensure tests are deterministic and isolated

2. **Slow Tests**: Tests that take too long to run
   - Solution: Optimize test data, use mocking, or move to integration tests

3. **False Positives**: Tests that pass but shouldn't
   - Solution: Review assertions and test logic

4. **Test Dependencies**: Tests that depend on each other
   - Solution: Ensure tests are independent and use proper fixtures

### Debugging Test Failures

1. **Run Single Test**: Use `pytest -k test_name` to run specific tests
2. **Verbose Output**: Use `pytest -v` for detailed test output
3. **Debug Mode**: Use `pytest --pdb` to drop into debugger on failure
4. **Capture Output**: Use `pytest -s` to see print statements

## Future Improvements

### Planned Enhancements

1. **Property-Based Testing**: Use hypothesis for generative testing
2. **Mutation Testing**: Use mutpy to measure test quality
3. **Load Testing**: Add tests for concurrent usage scenarios
4. **Security Testing**: Add security-focused test cases

### Monitoring and Metrics

1. **Test Execution Time**: Track test suite performance over time
2. **Coverage Trends**: Monitor coverage changes across releases
3. **Flaky Test Detection**: Automatically detect and report flaky tests
4. **Performance Regressions**: Monitor benchmark results for performance issues
