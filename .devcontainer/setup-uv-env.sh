#!/bin/bash

set -e

echo "Setting up Python environment with uv..."

# Check if uv is installed
if ! command -v uv &>/dev/null; then
    echo "Error: uv is not installed. Please run setup-mac.sh first."
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
else
    echo "✓ Virtual environment already exists."
fi

# Initialize uv project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "Initializing uv project..."
    uv init --no-readme
    echo "✓ Created pyproject.toml"
else
    echo "✓ pyproject.toml already exists."
fi

# Install packages from requirements.txt using uv add
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    uv add -r requirements.txt
    echo "✓ Packages installed successfully!"
else
    echo "⚠ requirements.txt not found."
fi

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
