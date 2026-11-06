# Directory Organizer

A Python command-line utility that sorts files in a folder into category subfolders.

## What's included

- `organizer.py`: the updated organizer.
- `create_test_files.py`: creates sample files in an `organizer_test` folder.

## Requirements

- Python 3.9 or newer recommended.
- No third-party packages required.

## Open and run in VS Code

1. Extract this ZIP file.
2. Open the extracted `directory-organizer` folder in VS Code.
3. Open Terminal > New Terminal.

### First, create sample files

```powershell
py create_test_files.py
```

This creates an `organizer_test` folder containing sample `.py`, `.pdf`, `.xlsx`,
`.jpg`, `.txt`, and `.csv` files.

### Preview the organization

Always preview first:

```powershell
py organizer.py organizer_test --dry-run
```

### Organize the sample folder

If the preview looks correct:

```powershell
py organizer.py organizer_test
```

Expected categories include:

- `Code`: `.py`
- `Documents`: `.pdf`, `.txt`
- `Spreadsheets`: `.xlsx`, `.csv`
- `Images`: `.jpg`
- `Misc`: file extensions not listed in the mapping

### Organize another folder

Use the full folder path in quotes, especially if it contains spaces:

```powershell
py organizer.py "C:\\Users\\acer\\Downloads" --dry-run
```

If the preview is correct, run it without `--dry-run`:

```powershell
py organizer.py "C:\\Users\\acer\\Downloads"
```

### Include files in subfolders

```powershell
py organizer.py "C:\\Users\\acer\\Downloads" --recursive --dry-run
```

Remove `--dry-run` to perform the moves.

## Safety and behaviour

- `--dry-run` previews changes without moving files.
- Existing files are not overwritten. A suffix such as `_1` is added when a name already exists.
- Hidden files and hidden folders are skipped.
- Existing category folders directly inside the target folder are not scanned again.
- By default, only files directly inside the target folder are organized.
- Recursive mode moves files found in subfolders into category folders at the target folder's top level.
- The sample PDF, XLSX, and JPG files are placeholders. They test extension-based classification only; they are not valid documents or images.

## Supported categories

Documents, Spreadsheets, Presentations, Images, Videos, Audio, Archives, Code, and Misc.
