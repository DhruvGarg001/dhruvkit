# DhruvKit Tests

This directory contains tests for DhruvKit functionality.

## Running Tests

### Install pytest

```bash
pip install pytest
```

### Run all tests

```bash
pytest tests/
```

### Run with verbose output

```bash
pytest tests/ -v
```

### Run specific test file

```bash
pytest tests/test_templates.py -v
```

### Run specific test

```bash
pytest tests/test_templates.py::TestTemplates::test_all_templates_exist -v
```

## Test Structure

- `test_templates.py` - Tests for template functionality
- `test_commands.py` - Tests for CLI commands (new, init, add)
- `test_licenses.py` - Tests for license handling
- `test_utils.py` - Tests for utility functions

## Coverage

To run tests with coverage:

```bash
pip install pytest-cov
pytest tests/ --cov=dhruvkit --cov-report=html
```

View the HTML report:
```bash
# On Windows
start htmlcov/index.html

# On Linux/Mac
open htmlcov/index.html
```

## Adding New Tests

When adding new functionality:

1. Create tests in the appropriate test file
2. Follow existing naming conventions (`test_*`)
3. Use descriptive test names that explain what is being tested
4. Include docstrings for test classes and methods
5. Clean up temporary files/directories after tests

## Notes

- Tests use `tempfile.TemporaryDirectory()` to avoid polluting the file system
- Tests restore the current working directory after execution
- Mock objects can be used for external dependencies
