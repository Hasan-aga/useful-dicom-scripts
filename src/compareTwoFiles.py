#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile

import pydicom
from rich.console import Console
from rich.syntax import Syntax
from termcolor import colored


def load_dicom_file(file1_path, file2_path):
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
    return [dicom1, dicom2]


def truncate_value(value, length=100):
    """Truncate the value if it is longer than the specified length."""
    value_str = str(value)
    return value_str if len(value_str) <= length else value_str[:length] + "..."

def write_dicom_tags_to_file(dicom, file_path):
    with open(file_path, 'w') as f:
        for elem in dicom.iterall():
            tag_name = elem.name if hasattr(elem, 'name') else str(elem.tag)
            value = truncate_value(elem.value)
            f.write(f"{tag_name} {elem.tag}: {value}\n")
            
def use_git(file1_path, file2_path, git_diff_args):
    # Load the DICOM files
    dicom1, dicom2 = load_dicom_file(file1_path, file2_path)
        # Create temporary files to store the metadata
    with tempfile.NamedTemporaryFile(delete=False) as temp1, tempfile.NamedTemporaryFile(delete=False) as temp2:
        temp1_path = temp1.name
        temp2_path = temp2.name

    try:
        # Write DICOM tags to temporary files
        write_dicom_tags_to_file(dicom1, temp1_path)
        write_dicom_tags_to_file(dicom2, temp2_path)

        git_diff_command = ['git', 'diff', '--no-index', temp1_path, temp2_path] + git_diff_args

        # Use git diff to compare the temporary files
        result = subprocess.run(git_diff_command, capture_output=True, text=True)

        # Use rich to display the diff output with color
        console = Console()
        syntax = Syntax(result.stdout, "diff", theme="ansi_dark")
        console.print(syntax)

    finally:
        # Remove temporary files
        os.remove(temp1_path)
        os.remove(temp2_path)

def compare_dicom_tags(file1_path, file2_path, show_all=False):
    print(f"Comparing DICOM tags between {file1_path} and {file2_path}...")

    # Load the DICOM files
    dicom1, dicom2 = load_dicom_file(file1_path, file2_path)

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
    parser = argparse.ArgumentParser(description="Compare DICOM tags between two files. By default, only differing tags are displayed. You can also choose to calculate and display the diff using Git.", epilog="Example: python compareTwoFiles.py file1.dcm file2.dcm", usage="compareTwoFiles.py file1.dcm file2.dcm [--all] [--git --color-words]")
    parser.add_argument("file1", help="Path to the first DICOM file.")
    parser.add_argument("file2", help="Path to the second DICOM file.")
    parser.add_argument("--all", action="store_true", help="Display all tags including common and unique tags.")
    parser.add_argument("git_and_args", nargs=argparse.REMAINDER, help="Pass --git followed by any git diff args to use git for comparison. Example: python compareTwoFiles.py file1.dcm file2.dcm --git --color-words")


    args = parser.parse_args()
    
    if "--git" in args.git_and_args:
        use_git(args.file1, args.file2, args.git_and_args[1:])
    else:
        compare_dicom_tags(args.file1, args.file2, args.all)
