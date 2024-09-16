import os
import subprocess
import shutil
import glob

def execute_task():
    total_png_count = 0

    for i in range(1, 21):  # Execute for 20 rounds
        folder_name = f"try{i}"
        os.makedirs(folder_name, exist_ok=True)  # Step (1): Create folder

        # Step (1): Execute the command in the created folder
        command = f'python AI4SCI_VE13.py -s p1.txt -n {i}'
        result = subprocess.run(command, shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if result is completed successfully
        if result.returncode != 0:
            print(f"Error in executing command for round {i}: {result.stderr.decode()}")
            continue  # Skips to the next iteration

        # Step (2): Move PNG and Word documents into the folder
        png_files = glob.glob('*.png')
        word_files = glob.glob('*.docx')

        for file in png_files + word_files:
            shutil.move(file, folder_name)  # Move files to the respective folder

        # Count PNG files in the current folder
        png_count = len(glob.glob(os.path.join(folder_name, '*.png')))
        total_png_count += png_count  # Aggregate count of PNG files

    # Compute the average number of PNG files in each round
    average_png_count = total_png_count / 20
    print("Average number of PNG boxes across all folders:", average_png_count)

if __name__ == "__main__":
    execute_task()
