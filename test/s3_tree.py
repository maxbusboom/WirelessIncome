#!/usr/bin/env python3
"""
Display a tree-style view of files in an S3 bucket.
Usage: python test/s3_tree.py [bucket-name] [--no-sign-request]
"""

import subprocess
import sys
from collections import defaultdict
from typing import Set, Tuple


def get_s3_files(bucket: str, no_sign_request: bool = False) -> list[str]:
    """Get list of all files in S3 bucket."""
    cmd = ["aws", "s3", "ls", "--recursive"]
    if no_sign_request:
        cmd.append("--no-sign-request")
    cmd.append(f"s3://{bucket}/")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    files = []
    for line in result.stdout.strip().split('\n'):
        if line:
            # Parse: date time size filename
            parts = line.split(None, 3)
            if len(parts) == 4:
                files.append(parts[3])

    return files


def build_tree(files: list[str]) -> dict[str, Set[Tuple]]:
    """Build tree structure from file paths."""
    tree = defaultdict(set)

    for path in files:
        parts = path.split('/')

        # Add all directory levels
        for i in range(len(parts)):
            if i == len(parts) - 1:
                # It's a file
                parent = '/'.join(parts[:i]) if i > 0 else ''
                tree[parent].add(('file', parts[i]))
            else:
                # It's a directory
                parent = '/'.join(parts[:i]) if i > 0 else ''
                current = '/'.join(parts[:i+1])
                tree[parent].add(('dir', parts[i], current))

    return tree


def print_tree(tree: dict, path: str = '', prefix: str = '', is_last: bool = True):
    """Print tree structure recursively."""
    items = sorted(tree.get(path, []))
    dirs = [item for item in items if item[0] == 'dir']
    files = [item for item in items if item[0] == 'file']

    all_items = dirs + files

    for idx, item in enumerate(all_items):
        is_last_item = (idx == len(all_items) - 1)
        connector = '└── ' if is_last_item else '├── '

        if item[0] == 'dir':
            print(f'{prefix}{connector}{item[1]}/')
            extension = '    ' if is_last_item else '│   '
            print_tree(tree, item[2], prefix + extension, is_last_item)
        else:
            print(f'{prefix}{connector}{item[1]}')


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(
            "Usage: python test/s3_tree.py <bucket-name> [--no-sign-request]")
        sys.exit(1)

    bucket = sys.argv[1]
    no_sign_request = '--no-sign-request' in sys.argv

    print(f"Fetching file list from s3://{bucket}/...")
    files = get_s3_files(bucket, no_sign_request)

    if not files:
        print("No files found in bucket.")
        return

    print(f"\n{bucket}/")
    tree = build_tree(files)
    print_tree(tree)

    print(f"\nTotal files: {len(files)}")


if __name__ == '__main__':
    main()
