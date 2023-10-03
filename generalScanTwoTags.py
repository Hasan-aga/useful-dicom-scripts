#!/usr/bin/env python3

import os
import pydicom
import sys


def scan_directory_for_dicom(base_dir, tag1, tag2):
    dicom_info = {}

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                filepath = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(filepath)
                    tag1_result = ds.get(tag1, "")
                    tag2_result = ds.get(tag2, "")
                    
                    # Handle MultiValue
                    if isinstance(tag1_result, pydicom.multival.MultiValue):
                        tag1_result = tuple(tag1_result)
                    if isinstance(tag2_result, pydicom.multival.MultiValue):
                        tag2_result = tuple(tag2_result)
                    
                    if tag1_result not in dicom_info:
                        dicom_info[tag1_result] = set()
                    
                    dicom_info[tag1_result].add(tag2_result)
                except Exception as e:
                    print(f"Failed to read {filepath}: {e}")
                    
    # Convert sets to lists for easier JSON serialization later if needed
    for key in dicom_info:
        dicom_info[key] = list(dicom_info[key])
        
    return dicom_info


if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python script_name.py <directory_path> tag1 tag2")
        sys.exit(1)

    base_directory = sys.argv[1]
    tag1 = sys.argv[2]
    tag2 = sys.argv[3]
    result = scan_directory_for_dicom(base_directory, tag1, tag2)

    for modality, body_parts in result.items():
        print(f"{modality}={body_parts}")
