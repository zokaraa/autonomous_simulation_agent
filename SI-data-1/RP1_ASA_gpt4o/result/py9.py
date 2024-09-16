import os
import shutil
import zipfile

def archive_results(zip_filename, source_dir):
    """Archive all files in source_dir into a zip file."""
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), source_dir))
    print(f"All results have been archived into {zip_filename}")

def main():
    # Path to results directory and output zip file
    results_dir = 'results'
    zip_filename = 'polymer_chain_simulation_results.zip'

    # Ensure results directory exists
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    # Check if files exist before archiving
    required_files = [
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
    missing_files = [f for f in required_files if not os.path.isfile(os.path.join(results_dir, f))]
    if missing_files:
        print(f"Warning: The following required files are missing in the '{results_dir}' directory:")
        for file in missing_files:
            print(f"  - {file}")
        return
    
    # Archive results
    archive_results(zip_filename, results_dir)

if __name__ == "__main__":
    main()
