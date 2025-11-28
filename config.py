"""
Configuration file for wireless-income project.
Defines common paths and settings used across notebooks.
"""

from pathlib import Path

# Project root directory (where this config.py file is located)
project_root = Path(__file__).parent

# Data directory (in the same directory as project root)
data_dir = project_root / "data"

# Ensure data directory exists
data_dir.mkdir(exist_ok=True)

# Convert to string for compatibility
data_dir = str(data_dir)

print(f"Project root: {project_root}")
print(f"Data directory: {data_dir}")
