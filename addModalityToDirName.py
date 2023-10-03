#!/usr/bin/env python3

import os
import pydicom
import shutil
import sys

def extract_modalities_from_directory(directory):
    modalities = set()

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            try:
                ds = pydicom.dcmread(filepath)
                modality = ds.Modality
                modalities.add(modality)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return modalities

def rename_directory(directory, modalities):
    modalities_str = "-".join(sorted(list(modalities)))

    parent_directory_path = os.path.dirname(directory)
    new_directory_name = f"{modalities_str}-{os.path.basename(directory)}"

    new_directory_path = os.path.join(parent_directory_path, new_directory_name)
    
    if directory != new_directory_path:  # Ensure it's actually being renamed to something new
        shutil.move(directory, new_directory_path)
        print(f"Renamed {directory} to {new_directory_name}")

def main(directory=None):
    if directory is None:
        directory = os.getcwd()

    # Get all sub-directories in the provided directory
    sub_directories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    for sub_directory in sub_directories:
        modalities = extract_modalities_from_directory(sub_directory)
        rename_directory(sub_directory, modalities)

if __name__ == "__main__":
    directory = None
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    main(directory)
