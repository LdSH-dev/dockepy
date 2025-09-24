#!/bin/bash

# Script to test CI pipeline locally
set -e

echo "🔧 Creating clean test environment..."
cd /tmp
rm -rf ci_test_env
python3 -m venv ci_test_env
source ci_test_env/bin/activate

echo "📦 Installing package with dev dependencies..."
cd /home/ldsh-dev/Projects/python--docker
pip install --upgrade pip
pip install -e ".[dev]"

echo "🎨 Running Black..."
black --check --diff .

echo "🔍 Running Flake8..."
flake8 docker_cicd_manager tests/

echo "🔧 Running MyPy..."
mypy --install-types --non-interactive docker_cicd_manager/

echo "✅ All linters passed! CI should work now."

# Cleanup
cd /tmp
rm -rf ci_test_env

echo "🎉 Local CI test completed successfully!"