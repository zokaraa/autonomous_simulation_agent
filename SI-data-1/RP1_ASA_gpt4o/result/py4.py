import shutil
import hashlib
import os
from os import path

def move_files_to_directory(directory):
    """Move relevant files into the specified directory."""
    files_to_move = [
        'Chain3D10.png', 
        'Chain3D50.png', 
        'Chain3D100.png', 
        'Chain3D200.png', 
        'Chain3D400.png', 
        'h2vsN.png', 
        'h2vsN_verified.png',
        'Polymer_Chain_Simulation_Report.docx'
    ]
    if not os.path.exists(directory):
        os.makedirs(directory)
    for file in files_to_move:
        if path.isfile(file):
            shutil.move(file, path.join(directory, file))

def generate_checksums(directory):
    """Generate checksums for files in the specified directory."""
    checksums = {}
    for root, _, files in os.walk(directory):
      for file in files:
          file_path = path.join(root, file)
          with open(file_path, 'rb') as f:
              file_hash = hashlib.md5()
              while chunk := f.read(8192):
                  file_hash.update(chunk)
              checksums[file] = file_hash.hexdigest()
    return checksums

def write_summary_file(directory, checksums):
    """Write a summary file containing checksums of all files."""
    summary_path = path.join(directory, 'summary.txt')
    with open(summary_path, 'w') as summary_file:
        summary_file.write("File Checksum Summary:\n")
        for file_name, checksum in checksums.items():
            summary_file.write(f"{file_name}: {checksum}\n")

# Move files to results directory
results_dir = 'results'
move_files_to_directory(results_dir)

# Generate checksums for moved files
checksums = generate_checksums(results_dir)

# Write summary file in results directory
write_summary_file(results_dir, checksums)

# Summarize actions
print(f"All relevant files have been moved to the '{results_dir}' directory and checksums have been written to summary.txt.")
print("Run the following commands to list directory structure:")
print(f"cd {results_dir}")
print("cat summary.txt")
