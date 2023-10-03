#!/usr/bin/env python3

import os
import sys
import pydicom
from pydicom.uid import generate_uid

def set_frame_of_reference(directory):
    dicom_files = [f for f in os.listdir(directory) if f.endswith('.dcm')]
    
    # Check if any DICOM file has a FrameOfReferenceUID set
    for dicom_file in dicom_files:
        dicom_path = os.path.join(directory, dicom_file)
        ds = pydicom.dcmread(dicom_path)
        
        if hasattr(ds, 'FrameOfReferenceUID') and ds.FrameOfReferenceUID:
            print(f"Warning: DICOM file {dicom_file} already has a FrameOfReferenceUID set. Exiting.")
            sys.exit(1)

    # Generate a FrameOfReferenceUID
    frame_of_reference_uid = generate_uid()

    # Set the FrameOfReferenceUID for all DICOM files
    for dicom_file in dicom_files:
        dicom_path = os.path.join(directory, dicom_file)
        ds = pydicom.dcmread(dicom_path)
        ds.FrameOfReferenceUID = frame_of_reference_uid
        ds.save_as(dicom_path)
        print(f"Set FrameOfReferenceUID for {dicom_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script_name.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    set_frame_of_reference(directory_path)
