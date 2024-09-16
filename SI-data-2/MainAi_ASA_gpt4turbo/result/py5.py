import os

# Define the directory to check, you can change this to your specific folder path
directory = 'path_to_your_directory'

def list_files(dir_path):
    """ List all files in the given directory """
    try:
        files = os.listdir(dir_path)
        return files
    except FileNotFoundError:
        print("Directory not found. Please check the path provided.")
        return []

def main():
    print("Listing all files in the directory:")
    files = list_files(directory)
    for file in files:
        print(file)
        
    # Additional operations can be added here based on the files found
    
if __name__ == "__main__":
    main()
