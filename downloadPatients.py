#!/usr/bin/env python3

import requests
import sys
import os

AUTH = None  # Change to tuple e.g. ('username', 'password') if you have authentication set up

def download_study_as_zip(base_url, study_id, output_folder):
    """Download the study with the given ID and save it as a zip file."""
    url = f"{base_url}/studies/{study_id}/archive"
    response = requests.get(url, auth=AUTH, stream=True)

    # Check if request was successful
    response.raise_for_status()

    output_path = os.path.join(output_folder, f"{study_id}.zip")
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded study {study_id} to {output_path}")


def main(base_url, patient_ids):
    # For each patient ID, get their studies and download them
    for patient_id in patient_ids:
        response = requests.get(f"{base_url}/patients/{patient_id}", auth=AUTH)
        response.raise_for_status()

        patient_data = response.json()
        study_ids = patient_data.get("Studies", [])

        for study_id in study_ids:
            download_study_as_zip(base_url, study_id, "downloads")  # 'downloads' is the folder where zips will be saved


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py BASE_URL patient_id1 patient_id2 ...")
        sys.exit(1)

    base_url = sys.argv[1]
    patient_ids = sys.argv[2:]
    main(base_url, patient_ids)
