#!/usr/bin/env python3

import argparse
import os
import sys

import pydicom
from termcolor import colored


def truncate_value(value, length=100):
    """Truncate the value if it is longer than the specified length."""
    value_str = str(value)
    return value_str if len(value_str) <= length else value_str[:length] + "..."

def compare_dicom_tags(file1_path, file2_path, show_all=False):
    print(f"Comparing DICOM tags between {file1_path} and {file2_path}...")

    # Check if files exist
    if not os.path.exists(file1_path):
        print(f"Error: File {file1_path} not found.")
        sys.exit(1)
    if not os.path.exists(file2_path):
        print(f"Error: File {file2_path} not found.")
        sys.exit(1)

    # Load the DICOM files
    dicom1 = pydicom.dcmread(file1_path)
    dicom2 = pydicom.dcmread(file2_path)

    # Extract the tags from both files
    tags1 = {elem.tag: elem for elem in dicom1.iterall()}
    tags2 = {elem.tag: elem for elem in dicom2.iterall()}

    # Find common, unique, and differing tags
    common_tags = set(tags1.keys()) & set(tags2.keys())
    unique_tags_file1 = set(tags1.keys()) - set(tags2.keys())
    unique_tags_file2 = set(tags2.keys()) - set(tags1.keys())
    differing_tags = {tag for tag in common_tags if tags1[tag].value != tags2[tag].value}

    if show_all:
        print("\nCommon Tags:")
        for tag in common_tags:
            tag_name = tags1[tag].name if hasattr(tags1[tag], 'name') else str(tag)
            print(f"{tag_name} {tag}:")
            print(colored(f"  File 1: {truncate_value(tags1[tag].value)}", 'blue'))
            print(colored(f"  File 2: {truncate_value(tags2[tag].value)}", 'blue'))
            print()

        print("\nUnique Tags in File 1:")
        for tag in unique_tags_file1:
            tag_name = tags1[tag].name if hasattr(tags1[tag], 'name') else str(tag)
            print(f"{tag_name} {tag}:")
            print(colored(f"  File 1: {truncate_value(tags1[tag].value)}", 'blue'))
            print()

        print("\nUnique Tags in File 2:")
        for tag in unique_tags_file2:
            tag_name = tags2[tag].name if hasattr(tags2[tag], 'name') else str(tag)
            print(f"{tag_name} {tag}:")
            print(colored(f"  File 2: {truncate_value(tags2[tag].value)}", 'blue'))
            print()

    print("\nDiffering Tags:")
    for tag in differing_tags:
        tag_name = tags1[tag].name if hasattr(tags1[tag], 'name') else str(tag)
        print(f"{tag_name} {tag}:")
        print(colored(f"  File 1: {truncate_value(tags1[tag].value)}", 'red'))
        print(colored(f"  File 2: {truncate_value(tags2[tag].value)}", 'green'))
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare DICOM tags between two files.")
    parser.add_argument("file1", help="Path to the first DICOM file.")
    parser.add_argument("file2", help="Path to the second DICOM file.")
    parser.add_argument("--all", action="store_true", help="Display all tags including common and unique tags.")

    args = parser.parse_args()

    compare_dicom_tags(args.file1, args.file2, args.all)
