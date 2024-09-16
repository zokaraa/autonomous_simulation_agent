import zipfile
import os
import pandas as pd

def extract_zip(zip_filename, extract_to):
    """Extract the ZIP file into the specified directory."""
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Files have been extracted to {extract_to}")

def verify_files(directory):
    """Verify the contents of the extracted directory."""
    expected_files = [
        'Chain3D10.png', 
        'Chain3D50.png', 
        'Chain3D100.png', 
        'Chain3D200.png', 
        'Chain3D400.png', 
        'h2vsN.png', 
        'summary.csv', 
        'Polymer_Chain_Simulation_Report.docx', 
        'report.html'
    ]
    missing_files = [file for file in expected_files if not os.path.exists(os.path.join(directory, file))]
    if missing_files:
        print("Warning: The following files are missing:")
        for file in missing_files:
            print(f"  - {file}")
    else:
        print("All expected files are present.")

def display_summary(directory):
    """Display the content of summary CSV and report details."""
    summary_path = os.path.join(directory, 'summary.csv')
    if os.path.exists(summary_path):
        summary_df = pd.read_csv(summary_path)
        print("Summary CSV Contents:")
        print(summary_df)
    else:
        print("Warning: summary.csv is missing.")
    
    # Display additional content if necessary
    # For instance, read the HTML or DOCX file if required using appropriate libraries

def main():
    zip_filename = 'polymer_chain_simulation_results.zip'
    extract_to = 'extracted_results'
    
    # Extract ZIP contents
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    extract_zip(zip_filename, extract_to)
    
    # Verify extracted files
    verify_files(extract_to)
    
    # Display summary
    display_summary(extract_to)

if __name__ == "__main__":
    main()
