#!/usr/bin/env python3

import os
import sys
import tarfile
import tempfile

import modify_dicom_tag  # assuming this is the name of your existing script


def anonymize_directory(directory):
    # Define the tags and their new values for anonymization
    anonymization_tags = [
    ('PatientName', 'anonymous'),
    ('PatientID', 'anonymous'),
    ('OtherPatientIDs', 'anonymous'),
    ('PatientBirthDate', '19000101'), # or any other anonymized date
    ('PatientSex', '0'),
    ('PatientAddress', 'anonymous'),
    ('InstitutionName', 'anonymous'),
    ('ReferringPhysicianName', 'anonymous'),
    ('OperatorsName', 'anonymous'),
    ('PhysiciansOfRecord', 'anonymous'),
    ('PerformingPhysicianName', 'anonymous'),
    ('NameOfPhysiciansReadingStudy', 'anonymous'),
    ('PatientsBirthName', 'anonymous'),
    ('PatientsMotherBirthName', 'anonymous'),
    ('PatientsTelephoneNumbers', 'anonymous'),
    ('EthnicGroup', 'anonymous'),
    ('Occupation', 'anonymous'),
    ('AdditionalPatientHistory', 'anonymous'),
    ('PatientComments', 'anonymous'),
    ('DeviceSerialNumber', 'anonymous'),
    ('ProtocolName', 'anonymous'),
    # ... and so on for other tags you want to anonymize
]

    # Usage in the new script
    for tag, value in anonymization_tags:
        modify_dicom_tag.update_dicom_tag_in_directory(directory, tag, value)


def main(dcm_path, tar_path):
    # Check if it's a single file or a directory
    if os.path.isfile(dcm_path) and dcm_path.endswith('.dcm'):
        # Process single DICOM file
        with tempfile.NamedTemporaryFile(suffix='.dcm') as temp_file:
            modify_dicom_tag.update_dicom_tag_in_directory(os.path.dirname(dcm_path), os.path.basename(dcm_path), temp_file.name)
            with tarfile.open(tar_path + '.tar.gz', 'w:gz') as tar:
                tar.add(temp_file.name, arcname=os.path.basename(dcm_path))
    elif os.path.isdir(dcm_path):
        # Process all DICOM files in directory
        anonymize_directory(dcm_path)
        with tarfile.open(tar_path + '.tar.gz', 'w:gz') as tar:
            for root, _, files in os.walk(dcm_path):
                for file in files:
                    if file.lower().endswith('.dcm'):
                        file_path = os.path.join(root, file)
                        tar.add(file_path, arcname=os.path.relpath(file_path, dcm_path))
    else:
        print("Invalid DICOM path. Please provide a valid DICOM file or directory.")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python anonymize.py <dcm_path> <tar_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
