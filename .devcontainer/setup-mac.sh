#!/bin/bash

set -e

echo "Installing .devcontainer dependencies on macOS using Homebrew..."

# Install Homebrew if not already installed
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew is already installed."
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Install Git
if ! command -v git &>/dev/null; then
    echo "Installing Git..."
    brew install git
else
    echo "✓ Git is already installed."
fi

# Install Git LFS
if ! command -v git-lfs &>/dev/null; then
    echo "Installing Git LFS..."
    brew install git-lfs
    git lfs install
else
    echo "✓ Git LFS is already installed."
fi

# Install GitHub CLI
if ! command -v gh &>/dev/null; then
    echo "Installing GitHub CLI..."
    brew install gh
else
    echo "✓ GitHub CLI is already installed."
fi

# Install AWS CLI
if ! command -v aws &>/dev/null; then
    echo "Installing AWS CLI..."
    brew install awscli
else
    echo "✓ AWS CLI is already installed."
fi

# Install uv (Python package manager)
if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    brew install uv
else
    echo "✓ uv is already installed."
fi

# Install wget
if ! command -v wget &>/dev/null; then
    echo "Installing wget..."
    brew install wget
else
    echo "✓ wget is already installed."
fi

# Install Python 3.12
echo "Checking Python 3.12..."
if ! brew list python@3.12 &>/dev/null; then
    echo "Installing Python 3.12..."
    brew install python@3.12
else
    echo "✓ Python 3.12 is already installed."
fi

# Note: Skip pip/requirements.txt installation here
# Use the setup-uv-env.sh script to set up the virtual environment and install packages with uv
echo ""
echo "Python 3.12 installation complete."
echo "Run ./.devcontainer/setup-uv-env.sh to set up your virtual environment and install packages."

echo ""
echo "✅ All dependencies installed successfully!"
echo ""
echo "Note: You may need to add Python 3.12 to your PATH:"
echo "  export PATH=\"/usr/local/opt/python@3.12/bin:\$PATH\""
