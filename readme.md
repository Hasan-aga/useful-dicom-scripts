## DICOM Tag Modifier Script

This script allows you to update the value of a specified DICOM tag across all DICOM files in a given directory. It's designed to be run as a standalone script or be imported as a module in other Python scripts.

### Usage

#### Standalone:

```bash
python modifydicomtag.py <directory_path> <dicom_tag_name> <value>
```

- `<directory_path>`: Path to the directory containing the DICOM files.
- `<dicom_tag_name>`: Name of the DICOM tag to be updated.
- `<value>`: New value for the specified DICOM tag.

Example:
```bash
python modifydicomtag.py ./dicom_files "BodyPartExamined" "Head"
```

#### As a Module:

```python
import modifydicomtag

# Define the parameters
directory_path = './dicom_files'
dicom_tag_name = 'BodyPartExamined'
new_value = 'Head'

# Call the function
modifydicomtag.update_dicom_tag_in_directory(directory_path, dicom_tag_name, new_value)
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