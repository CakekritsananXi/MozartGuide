
#!/bin/bash

# Run all unit tests for Phin Isan AI

echo "🧪 Running Phin Isan AI Test Suite"
echo "=================================="

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest pytest-cov
fi

# Run tests with coverage
echo ""
echo "Running unit tests..."
pytest tests/ -v -s --cov=agents --cov=music_generator --cov-report=term-missing

# Run only fast tests
echo ""
echo "Running fast tests only..."
pytest tests/ -v -m "not slow"

# Run integration tests
echo ""
echo "Running integration tests..."
pytest tests/ -v -m "integration"

echo ""
echo "✅ Test suite completed!"
