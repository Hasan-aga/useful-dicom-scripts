#!/usr/bin/env python3


import os
import sys

import pydicom
from termcolor import colored


def truncate_value(value, length=100):
    """Truncate the value if it is longer than the specified length."""
    value_str = str(value)
    return value_str if len(value_str) <= length else value_str[:length] + "..."


def compare_dicom_tags(file1_path, file2_path):
    print(f"Comparing DICOM tags between {file1_path} and {file2_path}...")
    # Load the DICOM files
        # Check if files exist
    if not os.path.exists(file1_path):
        print(f"Error: File {file1_path} not found.")
        sys.exit(1)
    if not os.path.exists(file2_path):
        print(f"Error: File {file2_path} not found.")
        sys.exit(1)
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

    # Print the comparison results
    # print("Common Tags:")
    # for tag in common_tags:
    #     print(f"{tag}: {tags1[tag].name}")

    # print("\nUnique Tags in File 1:")
    # for tag in unique_tags_file1:
    #     print(f"{tag}: {tags1[tag].name}")

    # print("\nUnique Tags in File 2:")
    # for tag in unique_tags_file2:
    #     print(f"{tag}: {tags2[tag].name}")

    print("\nDiffering Tags:")
    for tag in differing_tags:
        print(f"{tag}:")
        print(colored(f"  File 1: {truncate_value(tags1[tag].value)}", 'red'))
        print(colored(f"  File 2: {truncate_value(tags2[tag].value)}", 'green'))

if __name__ == "__main__":
    if len(sys.argv) !=3:
        print(sys.argv)
        print("Usage: python3 compareTwoFiles path1 path2")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    compare_dicom_tags(file1_path, file2_path)
