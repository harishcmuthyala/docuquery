# Tests

This folder contains a sample test to demonstrate how pytest works.

## Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_chunker.py

# Run with verbose output
pytest tests/ -v

# Run specific test function
pytest tests/test_chunker.py::test_chunk_fixed_basic
```

## Test Structure

- `test_*.py` - Test files (pytest auto-discovers files starting with `test_`)
- Each test function starts with `test_`
- Use `assert` statements to verify expected behavior
- Use `pytest.raises()` to test exceptions

## Example Test

See `test_chunker.py` for a complete example showing:
- Basic test functions
- Using fixtures (Page objects)
- Testing different scenarios
- Testing error cases with `pytest.raises()`
