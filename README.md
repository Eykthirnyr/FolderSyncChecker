# Folder Sync Checker

**Folder Sync Checker** is a Python GUI application that helps you compare and synchronize files between two folders. It uses MD5 hashes to identify files based on their content, ensuring an accurate comparison regardless of the folder structure. The application identifies missing files in the second folder and offers the option to copy them safely from the first folder to the second.

---

## Features

- **Accurate File Comparison**: Compares files based on their content (MD5 hashes), ignoring differences in folder structure.
- **Missing Files Report**: Generates a `missing_files.txt` file listing the absolute paths of missing files in the second folder.
- **Safe Copying**: Copies missing files from the first folder to the second without overwriting existing files. 
- **User-Friendly GUI**:
  - Intuitive interface with tooltips on all main buttons.
  - Progress bar and status messages to keep you informed during operations.
- **Manual Control**:
  - The user starts the scan manually with a dedicated button.
  - Multiple confirmations before copying files, including a disclaimer with a timeout.
- **Cross-Platform**: Built with Python and Tkinter, compatible with Windows, macOS, and Linux.

---

## How It Works

1. **Select Folders**:
   - Select the source folder (`Folder 1`) where files are stored.
   - Select the target folder (`Folder 2`) to compare against.

2. **Start Scan**:
   - Click the **"Start Scan"** button to compare the two folders.
   - The app computes MD5 hashes for all files in both folders and identifies missing files in the second folder.

3. **Review Results**:
   - The app generates a `missing_files.txt` in the first folder, listing the paths of all missing files.

4. **Copy Missing Files** (Optional):
   - Click the **"Copy Missing Files"** button to copy missing files from `Folder 1` to `Folder 2`.
   - Confirm the action through prompts and a disclaimer.
   - The app safely copies files without overwriting existing files.

---

## Installation

### Prerequisites

- Python 3.7 or higher installed on your system.
- No external libraries are required; the app uses Python's standard library.

## Usage

1. Launch the app by running the `folder_sync_checker.py` file.
2. Use the **"Select First Folder"** button to choose the source folder (`Folder 1`).
3. Use the **"Select Second Folder"** button to choose the target folder (`Folder 2`).
4. Click **"Start Scan"** to begin comparing the two folders.
5. Once the scan is complete:
   - Review the `missing_files.txt` generated in `Folder 1`.
   - Optionally, use the **"Copy Missing Files"** button to copy missing files to `Folder 2`.
6. Follow the prompts to confirm and complete the copy operation.

---

## Screenshots

![FolderSyncChecker](https://github.com/user-attachments/assets/904e230d-866d-49fa-a66c-2c5ee15d1f8e)

---

## Features in Detail

### Tooltips
- Hover over any main button to see detailed explanations of their functionality.

### Progress Bar
- Displays the progress of scanning and copying tasks.

### Status Messages
- Keeps you informed of the app's current state, e.g., "Awaiting user input," "Scanning folders," or "Copying missing files."

### Safe Copying
- Files are copied without overwriting existing files in `Folder 2`.

### Disclaimer
- A confirmation dialog with a 5-second delay ensures users acknowledge responsibility for their files before proceeding with copying.

---

## Author

**Clément GHANEME**

- [Website](https://clement.business)
- Initial Release : 26/11/2024
