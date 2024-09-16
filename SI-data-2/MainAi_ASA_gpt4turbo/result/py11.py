import os

def check_files_in_directory(directory_path):
    """
    Checks and prints the files in the given directory.
    Used to verify output files from previous tasks and for use in subsequent tasks.
    
    Parameters:
        directory_path (str): The path to the directory to check.
    """
    try:
        # List all files in the directory
        files = os.listdir(directory_path)
        print("Files in directory:", files)
        
        # Check for specific files you expect from previous sub-tasks
        expected_files = ['output1.txt', 'output2.txt']
        found_files = []
        
        for file in expected_files:
            if file in files:
                found_files.append(file)
        
        if len(found_files) == len(expected-get_files):
            print("All expected files are present.")
        else:
            missed_files = set(expected_files) - set(found_files)
            print("Missing files:", missed_files)
        
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Use the function - specify the path to your directory
directory_path = 'path/to/your/directory'
check_files_in_directory(directory_path)  # Fixed function call name
