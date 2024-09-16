import os

def read_and_plot_files(directory):
    """
    This function reads all files from the specified directory with a '.txt' extension,
    counts the words in each file, and logs this data to the terminal.
    """
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
            print(f"File: {file_name}, Word Count: {word_to_count}")
    
    # Optional: return results for further usage
    return results

# Example usage (change 'path_to_files' to the path of your directory)
path_to_files = "./data"
processed_data = read_and_process_files(path_to_files)
