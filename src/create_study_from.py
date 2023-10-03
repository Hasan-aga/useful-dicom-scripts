#!/usr/bin/env python3

import os
import uuid
import pydicom
import modify_dicom_tag

def create_new_study(directory, new_study_uid):
    # Update Study Instance UID
    modify_dicom_tag.update_dicom_tag_in_directory(directory, "StudyInstanceUID", new_study_uid)
    
    # Optionally, update other tags as necessary
    # ...
    
def generate_new_study_uid():
    return "1.2.840." + str(uuid.uuid4()).replace('-', '.')

def main():
    current_directory = os.getcwd()  # Assumes existing study is in the current directory
    new_study_uid = generate_new_study_uid()
    create_new_study(current_directory, new_study_uid)

if __name__ == "__main__":
    main()
