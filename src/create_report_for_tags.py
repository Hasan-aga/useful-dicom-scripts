#!/usr/bin/env python3

import os
import pydicom
import sys


def scan_directory_for_dicom(base_dir, tags):
    report_set = set()

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                filepath = os.path.join(root, file)
                report_entry = ""
                for tag in tags:
                    try:
                        ds = pydicom.dcmread(filepath)
                        tag_result = ds.get(tag, "")
                        
                        # Handle MultiValue
                        if isinstance(tag_result, pydicom.multival.MultiValue):
                            tag_result = tuple(tag_result)
                            
                        report_entry = f"{report_entry} {tag_result},"
                        report_set.add(report_entry)
                    except Exception as e:
                        print(f"Failed while creating entry for tag ({tag}) in {filepath}: {e}")

                    
    return report_set


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <directory_path> tag1 tag2 tag3 ... etc")
        sys.exit(1)

    base_directory = sys.argv[1]
    tags = sys.argv[1::]
    result = scan_directory_for_dicom(base_directory, tags)

    for entry in result:
        print(f"{entry}")
