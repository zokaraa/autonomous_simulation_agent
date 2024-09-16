import os

def main():
    # Check for presence of files in the current directory
    files = os.listdir('.')
    
    # If there is a file named 'output_from_previous_task.txt', process it
    target_file = 'output_from_previous_task.txt'  # Corrected the file name
    if target_file in files:
        # Read the contents of the file
        with open(target_file, 'r') as file:
            content = file.read()

        # Example Data Manipulation: Count the number of occurrences of each word (simple tokenization)
        words = content.split()
        word_count = {}  # Corrected variable name here
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1  # Corrected typo here

        # Print the results which could be useful for further processing
        print("Word Count Results:")
        for word, count in word_count.items():
            print(f"{word}: {count}")

    else:
        print("Required file is not found in the current directory. Please check the file exists and retry.")

if __name__ == "__main__":
    main()
