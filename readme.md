# Useful Dicom Scripts
This repository contains scripts to manipulate/read DICOM files by updating specific tags or creating new studies from existing ones. 
These scripts are designed to be modular, allowing usage as standalone applications or imported as modules in other Python projects.

There are two types of operations:

  1.  Manipulating a dicom tag (create_study_from, modify_dicom_tag)
  2.  Reading a dicom tag (generalScanTwoTags)



## Installation
Clone this repo and add it to your terminal's `$PATH` variable, example (.zshrc)
```
export PATH=$PATH:/home/hasan/work/useful-scripts/src
```

Notice that because the scripts the shebang tag at the top, you can run them without needing to write `python` keyword in the terminal.
## DICOM Tag Modifier Script

This script allows you to update the value of a specified DICOM tag across all DICOM files in a given directory. It's designed to be run as a standalone script or be imported as a module in other Python scripts.

### Usage


#### Standalone:

```bash
modifydicomtag.py <directory_path> <dicom_tag_name> <value>
```

- `<directory_path>`: Path to the directory containing the DICOM files.
- `<dicom_tag_name>`: Name of the DICOM tag to be updated.
- `<value>`: New value for the specified DICOM tag.

Example:
```bash
smodifydicomtag.py ./dicom_files "BodyPartExamined" "Head"
```

#### As a Module:

```python
import modify_dicom_tag

# Define the parameters
directory_path = './dicom_files'
dicom_tag_name = 'BodyPartExamined'
new_value = 'Head'

# Call the function
modify_dicom_tag.update_dicom_tag_in_directory(directory_path, dicom_tag_name, new_value)
```

### Dependencies

- `pydicom`: A Python package for working with DICOM files.
  
  Install via pip:
  ```bash
  pip install pydicom
  ```

### Error Handling

The script skips files where the specified DICOM tag is not found, and prints a message indicating so. Any other exceptions encountered while processing a file will result in an error message being printed, but the script will continue processing the remaining files.

### Notes

- The script only processes files with a `.dcm` extension.
- Modified files are saved in-place, overwriting the original files.

Make sure to create a backup of your original DICOM files before running this script, as the modifications are irreversible.

## Create New Study Script

This script is utilized to create a new study from an existing study by modifying the DICOM tags 'StudyInstanceUID', and optionally 'PatientID' and 'PatientName' of all the DICOM files within the specified directory.

### Usage

```bash
create_new_study.py <source_directory> [--new-study-id <new_study_id>] [--new-patient-id <new_patient_id>]
```

### Arguments

- `source_directory` (required): The directory containing the DICOM files of the existing study.
- `--new-study-id` (optional): The new Study Instance UID for the new study. If not supplied, a random UID will be generated.
- `--new-patient-id` (optional): The new Patient ID for the new study. If supplied, the 'PatientID' and 'PatientName' tags will be updated.

### Functions

- `create_new_study(directory, new_study_uid, new_patient_id=None)`: Updates the 'StudyInstanceUID', and if a new patient ID is provided, 'PatientID' and 'PatientName' of all DICOM files in the specified directory.
- `generate_new_study_uid()`: Generates a random DICOM UID for the new study.
- `main()`: Parses command line arguments and calls `create_new_study` with the provided arguments.

### Dependency

This script depends on the `modify_dicom_tag.py` script to perform the DICOM tag updates. Ensure that `modify_dicom_tag.py` is in the same directory as this script or is available in your Python path.

### Examples

Create a new study with a random Study Instance UID:
```bash
create_new_study.py /path/to/existing/study
```

Create a new study with a specified Study Instance UID and a new Patient ID:
```bash
create_new_study.py /path/to/existing/study --new-study-id 1.2.3.4.5 --new-patient-id NEWPATIENTID
```

### Notes

- The DICOM files in the specified directory will be modified in-place. Ensure to have backups or work on a copy of the original data to prevent any data loss.
- This script uses the `pydicom` library to generate new UIDs and to read and write DICOM files. Ensure `pydicom` is installed in your Python environment.

## General scan two tags
This script scans a directory of dicom files generating a list of all unique combinations of the given two tags.

Example:
```
generalScanTwoTags.py <directory_path> tag1 tag2
```

For example, If I wanted to know all the possible values of the `BodypartExamined` tag grouped by `SeriesDescription` I can do that using this command:
```
generalScanTwoTags.py . "SeriesDescription" "BodypartExamined"
```

### Notes

The script only reports unique values, if the same combination appears twice it will displayed as one.
