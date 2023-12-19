#!/usr/bin/env python3
import sys

import numpy as np
import pydicom
from PIL import Image
from pydicom.uid import ExplicitVRLittleEndian, generate_uid


def convert_jpg_to_dcm(jpg_path, example_dcm_path, output_path):
    # Load the JPEG image
    jpg_image = Image.open(jpg_path)
    jpg_data = np.array(jpg_image)

    # Ensure the image is in RGB format
    if jpg_data.ndim == 2:  # Grayscale image
        jpg_data = np.stack((jpg_data,) * 3, axis=-1)  # Convert to RGB
    elif jpg_data.shape[2] == 4:  # RGBA image
        jpg_data = jpg_data[:, :, :3]  # Discard alpha channel

    # Load the example DICOM file
    example_dcm = pydicom.dcmread(example_dcm_path)

    # Create a new DICOM file, copying metadata from the example
    new_dcm = pydicom.Dataset()
    new_dcm.file_meta = example_dcm.file_meta
    new_dcm.update(example_dcm)

    # Set necessary values for the new DICOM file
    new_dcm.is_little_endian = True
    new_dcm.is_implicit_VR = False
    new_dcm.SOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    new_dcm.SOPInstanceUID = generate_uid()
    new_dcm.Modality = 'OT'
    new_dcm.SeriesInstanceUID = example_dcm.SeriesInstanceUID

    # Update pixel data
    rows, columns, _ = jpg_data.shape
    new_dcm.Rows, new_dcm.Columns = rows, columns
    new_dcm.PhotometricInterpretation = "RGB"
    new_dcm.SamplesPerPixel = 3
    new_dcm.BitsAllocated = 8
    new_dcm.BitsStored = 8
    new_dcm.HighBit = 7
    new_dcm.PixelRepresentation = 0
    new_dcm.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Pixel data should be in RGB format
    # PIL reads images in RGB format by default, so no additional conversion is necessary
    new_dcm.PixelData = jpg_data.tobytes()

    # Save the new DICOM file
    new_dcm.save_as(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py source_jpg example_dcm output_dcm")
        sys.exit(1)

    convert_jpg_to_dcm(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"Converted JPEG to DICOM: {sys.argv[3]}")
