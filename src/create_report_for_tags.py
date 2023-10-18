#!/usr/bin/env python3

import os
import pydicom
import sys
import csv

def scan_directory_for_dicom(base_dir, tags, unique_only=False):
    report_set = set()
    report_list = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                filepath = os.path.join(root, file)
                report_entry = []
                for tag in tags:
                    try:
                        ds = pydicom.dcmread(filepath)
                        tag_result = ds.get(tag, "")
                        
                        # Handle MultiValue
                        if isinstance(tag_result, pydicom.multival.MultiValue):
                            tag_result = "|".join(map(str, tag_result))
                            
                        report_entry.append(tag_result)
                    except Exception as e:
                        print(f"Failed while creating entry for tag ({tag}) in {filepath}: {e}")

                if unique_only:
                    report_set.add(tuple(report_entry))
                else:
                    report_list.append(report_entry)
                    
    if unique_only:
        return [list(item) for item in report_set]
    else:
        return report_list

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <directory_path> tag1 tag2 tag3 ... etc [--unique]")
        sys.exit(1)

    base_directory = sys.argv[1]
    tags = sys.argv[2:]

    unique_only = False
    if "--unique" in tags:
        unique_only = True
        tags.remove("--unique")

    result = scan_directory_for_dicom(base_directory, tags, unique_only)

    absolute_base_directory = os.path.abspath(base_directory)
    output_file_path = os.path.join(absolute_base_directory, 'output.csv')
    with open(output_file_path, 'w', newline='') as csvfile:
        print(f"Your report is being created in {os.path.abspath(base_directory)}/output.csv")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(tags)  # Writing the header (tags)
        for entry in result:
            csvwriter.writerow(entry)
