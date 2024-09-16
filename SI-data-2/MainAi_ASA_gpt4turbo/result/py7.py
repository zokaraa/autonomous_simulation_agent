import os

def read_and_process_files(directory):
    # List all files in the given directory that end with .txt
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    # Initialize a container to accumulate results
    results = []
    
    # Process each file
    for file_name in files:
        filepath = os.path.join(directory, file_name)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Here we simply count the words in each file
            word_count = len(content.split())
            results.append((file_name, word_count))
            
            # Print the results needed for subsequent tasks
            print(f"File: {file_name}, Word Count: {word_count}")
    
    # Optionally, return the results to be used further
    return results

# Usage example (change the path to your directory)
path_to_files = "./data"
processed_data = read_and_processstandard_files(path_to_files)
