import os
import hashlib
import csv
from os import path

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

def write_csv_summary(directory, h2_values, scaling_exponent, file_checksums):
    """Write a CSV file summarizing h2 values and checksums."""
    csv_path = path.join(directory, 'summary.csv')
    N_values = [10, 50, 100, 200, 400]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['N', 'h2(N)', 'File', 'Checksum'])
        
        h2_index = 0
        for file_name, checksum in file_checksums.items():
            if file_name.startswith("Chain3D") and file_name.endswith(".png"):
                N = N_values[h2_index]
                h2_N = h2_values[h2_index]
                csv_writer.writerow([N, h2_N, file_name, checksum])
                h2_index += 1
        
        # Append the scaling exponent information
        csv_writer.writerow([])
        csv_writer.writerow(['Scaling exponent v', scaling_exponent])
    
    # Print console message
    print(f"Summary CSV created at: {csv_path}")

# Summarize relevant outputs
results_dir = 'results'
h2_values = [
    10.126149898135866,
    48.84597309146922,
    99.67816248963773,
    202.85695577701915,
    405.66744630809154
]
scaling_exponent = 1.002402565584748

# Generate file checksums
file_checksums = generate_checksums(results_dir)

# Write summary CSV
write_csv_summary(results_dir, h2_values, scaling_exponent, file_checksums)
