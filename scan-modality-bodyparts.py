#!/usr/bin/env python3

import os
import pydicom
import sys


# scan directories for dcm files and generate a set of bodyparts for each modality 
def scan_directory_for_dicom(base_dir):
    dicom_info = {}

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                filepath = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(filepath)
                    modality = ds.get("Modality", "")
                    body_part = ds.get("BodyPartExamined", "")
                    
                    if modality not in dicom_info:
                        dicom_info[modality] = set()
                    
                    dicom_info[modality].add(body_part)
                except Exception as e:
                    print(f"Failed to read {filepath}: {e}")
                    
    # Convert sets to lists for easier JSON serialization later if needed
    for key in dicom_info:
        dicom_info[key] = list(dicom_info[key])
        
    return dicom_info

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)

    base_directory = sys.argv[1]
    result = scan_directory_for_dicom(base_directory)

    for modality, body_parts in result.items():
        print(f"{modality}={body_parts}")
