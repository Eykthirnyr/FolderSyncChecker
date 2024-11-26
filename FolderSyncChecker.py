import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import hashlib
import os
import threading
import shutil
import webbrowser
import time

class Tooltip(object):
    '''
    It creates a tooltip for a given widget as the mouse goes on it.
    '''
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # miliseconds
        self.wraplength = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None
    def enter(self, event=None):
        self.schedule()
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)  # removes all decorations
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='yellow', relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class FileComparatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Folder Sync Checker")

        # Initialize variables
        self.folder1 = ''
        self.folder2 = ''
        self.hashes1 = {}
        self.hashes2 = {}
        self.missing_files = []
        self.is_scanning = False

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.master, text="Folder Sync Checker", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        # Subtitle
        self.subtitle_label = tk.Label(self.master, text="Compare and sync files between two folders based on their content.", font=("Helvetica", 12))
        self.subtitle_label.pack(pady=5)

        # Instructions
        self.instructions_label = tk.Label(self.master, text="Select two folders to compare. The app will identify missing files based on content, regardless of folder structure.")
        self.instructions_label.pack(pady=5)

        # Select Folder 1 Button
        self.select_folder1_button = tk.Button(self.master, text="Select First Folder", command=self.select_folder1)
        self.select_folder1_button.pack(pady=5)
        Tooltip(self.select_folder1_button, "Select the source folder (Folder 1)")

        # Folder 1 Label
        self.folder1_label = tk.Label(self.master, text="No folder selected")
        self.folder1_label.pack(pady=5)

        # Select Folder 2 Button
        self.select_folder2_button = tk.Button(self.master, text="Select Second Folder", command=self.select_folder2)
        self.select_folder2_button.pack(pady=5)
        Tooltip(self.select_folder2_button, "Select the target folder (Folder 2)")

        # Folder 2 Label
        self.folder2_label = tk.Label(self.master, text="No folder selected")
        self.folder2_label.pack(pady=5)

        # Start Scan Button (Initially disabled)
        self.start_scan_button = tk.Button(self.master, text="Start Scan", state="disabled", command=self.start_scan)
        self.start_scan_button.pack(pady=5)
        Tooltip(self.start_scan_button, "Start comparing the two folders")

        # Progress Bar
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text="Awaiting user input.")
        self.status_label.pack(pady=5)

        # Copy Missing Files Button (Initially disabled)
        self.copy_button = tk.Button(self.master, text="Copy Missing Files", state="disabled", command=self.copy_missing_files)
        self.copy_button.pack(pady=5)
        Tooltip(self.copy_button, "Copy missing files from Folder 1 to Folder 2")

        # Made by Clément GHANEME Button
        self.credit_button = tk.Button(self.master, text="Made by Clément GHANEME", command=self.open_website)
        self.credit_button.pack(side="bottom", pady=10)
        Tooltip(self.credit_button, "Visit the developer's website")

        # Exit Button
        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack(pady=5)
        Tooltip(self.exit_button, "Exit the application")

    def open_website(self):
        webbrowser.open("https://clement.business")

    def select_folder1(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder1 = folder
            self.folder1_label.config(text=self.folder1)
            self.status_label.config(text="First folder selected.")
            if self.folder1 and self.folder2:
                self.start_scan_button.config(state="normal")

    def select_folder2(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder2 = folder
            self.folder2_label.config(text=self.folder2)
            self.status_label.config(text="Second folder selected.")
            if self.folder1 and self.folder2:
                self.start_scan_button.config(state="normal")

    def start_scan(self):
        if not self.is_scanning:
            self.is_scanning = True
            self.copy_button.config(state="disabled")
            self.start_scan_button.config(state="disabled")
            self.progress["value"] = 0
            self.status_label.config(text="Scanning folders...")
            threading.Thread(target=self.scan_folders).start()

    def scan_folders(self):
        self.hashes1 = {}
        self.hashes2 = {}
        self.missing_files = []

        # First, get list of all files in both folders
        files1 = []
        for root, dirs, files in os.walk(self.folder1):
            for file in files:
                files1.append(os.path.join(root, file))

        files2 = []
        for root, dirs, files in os.walk(self.folder2):
            for file in files:
                files2.append(os.path.join(root, file))

        total_files = len(files1) + len(files2)
        self.progress["maximum"] = total_files
        progress_count = 0

        # Compute hashes for files in folder1
        for filepath in files1:
            md5_hash = self.compute_md5(filepath)
            if md5_hash:
                self.hashes1[md5_hash] = filepath
            progress_count += 1
            self.update_progress(progress_count)
        # Compute hashes for files in folder2
        for filepath in files2:
            md5_hash = self.compute_md5(filepath)
            if md5_hash:
                self.hashes2[md5_hash] = filepath
            progress_count += 1
            self.update_progress(progress_count)

        # Compare hashes to find missing files
        for md5_hash, filepath in self.hashes1.items():
            if md5_hash not in self.hashes2:
                self.missing_files.append(filepath)

        # Write missing files to txt file
        missing_files_txt = os.path.join(self.folder1, "missing_files.txt")
        with open(missing_files_txt, "w") as f:
            for filepath in self.missing_files:
                f.write(filepath + "\n")

        # Update status
        self.status_label.config(text=f"Scan complete. {len(self.missing_files)} missing files identified.")
        self.copy_button.config(state="normal")
        self.is_scanning = False

    def compute_md5(self, filepath):
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return None
        return hash_md5.hexdigest()

    def update_progress(self, value):
        self.progress["value"] = value
        self.master.update_idletasks()

    def copy_missing_files(self):
        # Multiple confirmations
        if not messagebox.askyesno("Confirmation", "Are you sure you want to copy the missing files from Folder 1 to Folder 2?"):
            return
        # Custom disclaimer dialog with 5-second delay
        if not self.disclaimer_dialog():
            return

        # Start copying in a new thread
        threading.Thread(target=self.copy_files_thread).start()

    def disclaimer_dialog(self):
        disclaimer = ("Disclaimer:\n\n"
                      "By proceeding, you acknowledge that you are responsible for your files. "
                      "The developer is not liable for any loss or damage to your data.\n\n"
                      "You can proceed in 5 seconds.")

        dialog = tk.Toplevel(self.master)
        dialog.title("Disclaimer")
        dialog.geometry("400x200")
        dialog.resizable(False, False)

        label = tk.Label(dialog, text=disclaimer, wraplength=380, justify="left")
        label.pack(pady=10)

        proceed_button = tk.Button(dialog, text="Proceed", state="disabled", command=dialog.destroy)
        proceed_button.pack(pady=10)

        # Enable button after 5 seconds
        def enable_button():
            proceed_button.config(state="normal")

        dialog.after(5000, enable_button)

        # Center the dialog
        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)

        return True

    def copy_files_thread(self):
        self.status_label.config(text="Copying missing files...")
        total_files = len(self.missing_files)
        self.progress["maximum"] = total_files
        self.progress["value"] = 0
        progress_count = 0

        for src_path in self.missing_files:
            # Determine destination path
            rel_path = os.path.relpath(src_path, self.folder1)
            dest_path = os.path.join(self.folder2, rel_path)
            dest_dir = os.path.dirname(dest_path)

            # Create destination directories if they don't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Copy file without overwriting
            if not os.path.exists(dest_path):
                try:
                    shutil.copy2(src_path, dest_path)
                except Exception as e:
                    print(f"Error copying file {src_path} to {dest_path}: {e}")
            else:
                print(f"File {dest_path} already exists. Skipping.")

            progress_count += 1
            self.update_progress(progress_count)

        self.status_label.config(text="Copying complete.")
        messagebox.showinfo("Copy Complete", "Missing files have been copied successfully.")

def main():
    root = tk.Tk()
    app = FileComparatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
