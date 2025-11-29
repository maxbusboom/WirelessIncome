# GitHub Copilot Instructions for wireless-income

## Project Overview
This project analyzes the relationship between median household income and wireless/broadband data speeds using:
- Census tract data (ACS 5-Year median household income)
- Ookla open data (fixed and mobile broadband performance tiles)

## Development Setup

### Environment Setup
- **Mac users**: Run `.devcontainer/setup-mac.sh` to install Homebrew, AWS CLI, `uv`, and other dependencies
- **Virtual environment**: Run `.devcontainer/setup-uv-env.sh` to set up Python environment with `uv`
- **Python version**: 3.12+
- **Package manager**: Use `uv` for all Python package management

### Project Structure
```
wireless-income/
├── config.py              # Configuration (defines data_dir)
├── notebooks/
│   └── ericbusboom/      # Personal analysis notebooks
├── data/                  # Local data directory (not in git)
├── .devcontainer/        # Setup scripts
└── .github/              # GitHub config & this file
```

## Code Conventions

### Notebooks
- **First cell**: Always load configuration with `%run ../../config.py`
- **Data directory**: Use `data_dir` variable defined in `config.py`
- **Cell order**: Design notebooks to run sequentially from top to bottom
- **Markdown cells**: Include section headers and explanations
- **Variable naming**: Use descriptive names (e.g., `files_df`, `tracts_gdf`, `paths_2022`)

### Geospatial Data
- **Library**: Use `geopandas` for geospatial operations
- **CRS handling**: 
  - Convert to projected CRS (EPSG:3857 Web Mercator) for geometric operations like centroids
  - Convert back to WGS84 (EPSG:4326) for lat/lon coordinates
  - Example: `gdf.to_crs(epsg=3857)` → compute → `to_crs(epsg=4326)`
- **Census tracts**: Filter to contiguous US states (exclude Alaska FIPS=02, Hawaii FIPS=15, and territories FIPS>=60)

### Data Sources
- **Ookla S3 bucket**: `s3://ookla-open-data/` (public, no auth)
- **File organization**: Ookla files use path pattern: `/type=(fixed|mobile)/year=YYYY/quarter=Q/`
- **Data formats**: 
  - Shapefiles (`.zip`) for tile geometries
  - Parquet (`.parquet`) for performance metrics
- **Download strategy**: Check if file exists locally before downloading

### Code Style
- **Imports**: Group stdlib, third-party, and local imports
- **Comments**: Explain the "why" not the "what"
- **Error handling**: Check for required variables/files before use
- **Progress output**: Print informative messages for long operations
- **Display Head**: do *not* print(df.head(); always put the df.head() at the end of the cell for the notebook to render it nicely

### Common Patterns

If you need to create a temporary dataframe for used in a single cell, always
name it `t`. You can reassign `t` as needed in different cells. 

For the primary analysis dataframe, use `gdf` for a geo frame, and `df` for a
regular dataframe.

Do not use `print` to dispay a lot of diagnostic data unless the user asks for
it, 

