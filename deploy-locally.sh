#!/bin/bash

# Script to test deployment locally (without actually uploading to PyPI)
set -e

echo "🚀 Testing deployment process locally..."
echo "========================================"

# Check if version type is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <patch|minor|major>"
    echo "Example: $0 patch"
    exit 1
fi

VERSION_TYPE="$1"

echo "📦 Installing dependencies..."
pip install -e ".[dev]"

echo ""
echo "🧪 Running tests..."
pytest tests/ -v --cov=docker_cicd_manager --cov-report=xml

echo ""
echo "🎨 Running linting..."
black --check --diff .
flake8 docker_cicd_manager tests/
mypy docker_cicd_manager/

echo ""
echo "📊 Getting current version..."
CURRENT_VERSION=$(python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])")
echo "Current version: $CURRENT_VERSION"

echo ""
echo "🔢 Calculating new version..."
# Split version into parts
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

case $VERSION_TYPE in
  major)
    NEW_MAJOR=$((MAJOR + 1))
    NEW_VERSION="$NEW_MAJOR.0.0"
    ;;
  minor)
    NEW_MINOR=$((MINOR + 1))
    NEW_VERSION="$MAJOR.$NEW_MINOR.0"
    ;;
  patch)
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
    ;;
  *)
    echo "Invalid version type: $VERSION_TYPE"
    echo "Use: patch, minor, or major"
    exit 1
    ;;
esac

echo "New version: $NEW_VERSION"

echo ""
echo "📝 Updating version in pyproject.toml..."
sed -i.bak "s/version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
echo "Updated pyproject.toml to version $NEW_VERSION"

echo ""
echo "🔨 Building package..."
python -m build

echo ""
echo "✅ Checking package..."
twine check dist/*

echo ""
echo "📋 Summary:"
echo "  Current version: $CURRENT_VERSION"
echo "  New version: $NEW_VERSION"
echo "  Version type: $VERSION_TYPE"
echo "  Package built: dist/"
echo ""
echo "🎯 Next steps for actual deployment:"
echo "  1. Review the changes: git diff"
echo "  2. Commit changes: git add . && git commit -m 'Release v$NEW_VERSION'"
echo "  3. Create tag: git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "  4. Push: git push origin main && git push origin v$NEW_VERSION"
echo "  5. Run GitHub Action: Deploy to PyPI workflow"
echo ""
echo "✅ Local deployment test completed successfully!"
echo "========================================"