#!/usr/bin/env python3

import sys

import pydicom
from pydicom.dataelem import DataElement
from pydicom.uid import generate_uid


def validate_and_correct_pn(person_name):
    """ Validates and corrects the format of DICOM Person Name (PN) """
    # Convert PersonName to string and split the name into components
    components = str(person_name).split('^')[:5]
    return '^'.join(components)

def modify_dicom_series(input_dcm_path, target_dcm_path, output_dcm_path):
    # Load the input and target DICOM files
    input_dcm = pydicom.dcmread(input_dcm_path)
    target_dcm = pydicom.dcmread(target_dcm_path)

    # Copy all tags from the target to the input DICOM, except for pixel data
    for elem in target_dcm:
        if elem.tag != pydicom.tag.Tag("7fe0", "0010"):  # Exclude pixel data tag
            input_dcm[elem.tag] = elem

    # Generate a new SOPInstanceUID for the input DICOM
    new_uid = generate_uid()
    input_dcm.SOPInstanceUID = new_uid
    if 'MediaStorageSOPInstanceUID' in input_dcm.file_meta:
        input_dcm.file_meta.MediaStorageSOPInstanceUID = new_uid

    # Correct the format of Person Name (PN) VRs
    pn_tags = ['ReferringPhysicianName', 'PerformingPhysicianName', 'PhysiciansOfRecord', 'RequestingPhysician']
    for tag in pn_tags:
        if tag in input_dcm:
            corrected_value = validate_and_correct_pn(input_dcm[tag].value)
            input_dcm[tag] = DataElement(tag, 'PN', corrected_value)
            
    input_dcm.PhotometricInterpretation = "RGB"
    input_dcm.SamplesPerPixel = 3
    input_dcm.PlanarConfiguration = 0

    # Save the modified input DICOM file
    input_dcm.save_as(output_dcm_path)
    print(f"Modified DICOM file saved as: {output_dcm_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python modify_dicom_series.py <input_dcm_path> <target_dcm_path> <output_dcm_path>")
        sys.exit(1)

    modify_dicom_series(sys.argv[1], sys.argv[2], sys.argv[3])
