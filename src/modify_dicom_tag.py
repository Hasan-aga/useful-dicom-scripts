#!/usr/bin/env python3

import os
import sys
import pydicom

def update_dicom_tag_in_directory(directory, tag_name, value):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".dcm"):
                filepath = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(filepath)
                    setattr(ds, tag_name, value)
                    ds.save_as(filepath)
                except Exception as e:
                    print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <directory_path> <dicom_tag_name> <value>")
        sys.exit(1)

    directory = sys.argv[1]
    dicom_tag = sys.argv[2]
    value = sys.argv[3]

    update_dicom_tag_in_directory(directory, dicom_tag, value)
