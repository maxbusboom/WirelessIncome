"""
Library functions for wireless-income project.

Functions for downloading and loading Ookla broadband performance data.
"""

import pandas as pd
import geopandas as gpd
from urllib.parse import urlparse
import os


def download_ookla_files(files_df, years, quarters, service_type, data_dir, s3):
    """
    Download Ookla parquet files based on selection criteria.

    Args:
        files_df: DataFrame with file metadata (path, year, quarter, service_type)
        years: int or list[int]
        quarters: int or list[int]
        service_type: 'fixed' or 'mobile'
        data_dir: directory path to save downloaded files
        s3: boto3 S3 client
    Returns:
        DataFrame with selection and added 'local_path' column
    """
    # Normalize scalars to lists
    if isinstance(years, int):
        years = [years]
    if isinstance(quarters, int):
        quarters = [quarters]

    # Boolean indexing
    mask = (
        files_df["year"].isin(years)
        & files_df["quarter"].isin(quarters)
        & (files_df["service_type"] == service_type)
    )
    selection = files_df.loc[mask].copy()

    print(
        f"Found {len(selection)} {service_type} files for years={years}, quarters={quarters}"
    )

    if selection.empty:
        print("Selection is empty; nothing to download.")
        return selection

    def download_s3_file(s3_uri):
        parsed = urlparse(s3_uri)
        bucket = parsed.netloc
        key = parsed.path.lstrip("/")
        filename = os.path.basename(key)
        local_path = os.path.join(data_dir, filename)
        if os.path.exists(local_path):
            print(f"{filename} already exists, skipping")
        else:
            print(f"Downloading {filename}...")
            s3.download_file(bucket, key, local_path)
            print(f"Saved to {local_path}")
        return local_path

    selection = selection.sort_values(["year", "quarter"])
    selection["local_path"] = [download_s3_file(p) for p in selection["path"]]

    print(f"\nDownloaded {len(selection)} files")
    return selection


def get_ookla_data(files_df, year, quarter, service_type, data_dir):
    """
    Load both parquet and shapefile data for a given year, quarter, and service type.

    Args:
        files_df: DataFrame with file metadata (path, year, quarter, service_type, kind)
        year: int, the year to load
        quarter: int, the quarter (1-4) to load
        service_type: 'fixed' or 'mobile'
        data_dir: directory path where downloaded files are stored

    Returns:
        DataFrame with Ookla performance data, or None if not found
    """
    # Filter for the specific year, quarter, and service type
    mask = (
        (files_df["year"] == year)
        & (files_df["quarter"] == quarter)
        & (files_df["service_type"] == service_type)
    )
    selection = files_df.loc[mask]

    if selection.empty:
        print(
            f"No files found for year={year}, quarter={quarter}, service_type={service_type}"
        )
        return None

    def get_local_path(s3_uri):
        """Get local path for file (assumes already downloaded)."""
        parsed = urlparse(s3_uri)
        key = parsed.path.lstrip("/")
        filename = os.path.basename(key)
        local_path = os.path.join(data_dir, filename)

        if not os.path.exists(local_path):
            print(f"ERROR: {filename} not found in {data_dir}")
            print(f"  Please download first using download_ookla_files()")
            return None

        return local_path

    # Load parquet data
    parquet_path = get_local_path(selection.iloc[0]["path"])
    if not parquet_path:
        return None

    print(f"Loading {os.path.basename(parquet_path)}...")
    df = pd.read_parquet(parquet_path)
    print(f"  Loaded {len(df)} rows")

    return df


def list_ookla_objects(s3, bucket_name="ookla-open-data"):
    """
    List Ookla S3 objects and return parquet file URI list.

    Args:
        s3: boto3 S3 client configured for unsigned access
        bucket_name: name of the Ookla public bucket
    Returns:
        list of parquet S3 URIs
    """
    response = s3.list_objects_v2(Bucket=bucket_name)
    parquet_files = []

    while True:
        for obj in response.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".parquet"):
                parquet_files.append(f"s3://{bucket_name}/{key}")

        if response.get("IsTruncated"):
            response = s3.list_objects_v2(
                Bucket=bucket_name, ContinuationToken=response["NextContinuationToken"]
            )
        else:
            break

    return parquet_files


def build_files_df(parquet_files):
    """
    Build a DataFrame of file paths with extracted metadata.

    Args:
        parquet_files: list of parquet S3 URIs
    Returns:
        pandas DataFrame with columns: path, service_type, year, quarter
    """
    import re

    pattern_type = re.compile(r"/type=(fixed|mobile)/")
    pattern_year = re.compile(r"/year=(\d{4})/")
    pattern_quarter = re.compile(r"/quarter=([1-4])/")

    rows = []
    for uri in parquet_files:
        service_type = pattern_type.search(uri)
        year_match = pattern_year.search(uri)
        quarter_match = pattern_quarter.search(uri)
        rows.append(
            {
                "path": uri,
                "service_type": service_type.group(1) if service_type else None,
                "year": int(year_match.group(1)) if year_match else None,
                "quarter": int(quarter_match.group(1)) if quarter_match else None,
            }
        )

    files_df = pd.DataFrame(rows)
    return files_df
