#!/usr/bin/env python3

import modify_dicom_tag
import argparse
import pydicom

def create_new_study(directory, new_study_uid, new_patient_id=None):
    # Update Study Instance UID
    modify_dicom_tag.update_dicom_tag_in_directory(directory, "StudyInstanceUID", new_study_uid)
    
    if new_patient_id:
        print(f"modifying patient id/name to {new_patient_id}")
        modify_dicom_tag.update_dicom_tag_in_directory(directory, 'PatientID', new_patient_id)
        modify_dicom_tag.update_dicom_tag_in_directory(directory, 'PatientName', new_patient_id)

    
def generate_new_study_uid():
    return pydicom.uid.generate_uid()

def main():
    parser = argparse.ArgumentParser(description='Create a new study from an existing study.')
    parser.add_argument('source_directory', help='Directory of the existing study.')
    parser.add_argument('--new-study-id', help='New Study ID. If not supplied random will be used')
    parser.add_argument('--new-patient-id', help='New Patient ID. Optional')

    args = parser.parse_args()
    new_study_uid = generate_new_study_uid() if args.new_study_id == None else args.new_study_id
    create_new_study(args.source_directory, new_study_uid, args.new_patient_id)

if __name__ == "__main__":
    main()
