import os

def read_and_process_files(directory):
    """
    This function reads all files from the specified directory with a '.txt' extension,
    counts the words in each file, and logs this data to the terminal. It checks if the
    directory exists before attempting to read files.
    """
    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Error: The specified directory does not exist.")
        return []

    # List all text files in the given directory
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    # Prepare to accumulate results
    results = []
    
    # Process each text file
    for file_name in files:
        filepath = os.path.join(directory, file_name)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Compute the number of words in the document
            word_count = len(content.split())
            results.append((file_name, word_count))
            
            # Output the results crucial for subsequent tasks
            print(f"File: {file_name}, Word Count: {word_count}")
    
    # Return results for further usage
    return results

# Example usage
# Ensure you change 'path_to_files' to the path of your directory containing the data files
path_to_files = "./data"
if os.path.isdir(path_to_files):
    processed_data = read_and_process_files(path_to_files)
else:
    print(f"Directory not found: {path_to_files}")
