#!/bin/bash

# Script to run exact CI commands locally
set -e

echo "🚀 Running exact CI pipeline locally..."
echo "========================================"

echo "📦 Installing dependencies..."
pip install -e ".[dev]"

echo ""
echo "🎨 Running Black..."
black --check --diff .

echo ""
echo "🔍 Running Flake8..."
flake8 docker_cicd_manager tests/

echo ""
echo "🔧 Running MyPy..."
mypy docker_cicd_manager/

echo ""
echo "🧪 Running tests..."
pytest tests/ -v --cov=docker_cicd_manager --cov-report=xml --cov-report=html

echo ""
echo "✅ All CI checks passed! Ready to commit."
echo "========================================"