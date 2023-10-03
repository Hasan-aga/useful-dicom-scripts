#!/usr/bin/env python3

import http.client
import json
import sys
import os
from urllib.parse import urlparse

def get_response(url_str, method="GET", body=None, headers={}):
    """Helper function to retrieve response using http.client."""
    print(f"downloading from {url_str}")
    url = urlparse(url_str)
    conn = http.client.HTTPConnection(url.hostname, url.port)
    conn.request(method, url.path, body, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    if response.status >= 400:
        raise Exception(f"HTTP error {response.status}: {data.decode('utf-8')}")
    return data

def get_uuid_for_patient(patient_id):
    """Retrieve the UUID for a given patient ID using the /tools/find endpoint."""
    url = ORTHANC_URL + "/tools/find"
    body = json.dumps({
        "Level": "Patient",
        "Query": {
            "PatientID": patient_id
        }
    })
    headers = {"Content-Type": "application/json"}
    data = get_response(url, method="POST", body=body, headers=headers)
    return json.loads(data)

def get_studies_for_uuid(uuid):
    """Retrieve a list of study IDs for a given UUID."""
    url = ORTHANC_URL + f"/patients/{uuid}"
    data = get_response(url)
    return json.loads(data).get('Studies', [])

def download_study(study_id, save_path):
    """Download a study from Orthanc server given its study ID."""
    url = ORTHANC_URL + f"/studies/{study_id}/archive"
    data = get_response(url)

    file_path = os.path.join(save_path, f"{study_id}.zip")
    with open(file_path, 'wb') as f:
        f.write(data)

    print(f"Downloaded study {study_id} to {file_path}")

def main(patient_ids, save_path):
    for patient_id in patient_ids:
        uuids = get_uuid_for_patient(patient_id)
        for uuid in uuids:
            study_ids = get_studies_for_uuid(uuid)
            for study_id in study_ids:
                download_study(study_id, save_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py http://localhost:8042 patient_id1 patient_id2 ...")
        sys.exit(1)
    print(f"Current working directory: {os.getcwd()}")
    save_path = "."
    ORTHANC_URL = sys.argv[1]
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    patient_ids = sys.argv[2:]
    main(patient_ids, save_path)
