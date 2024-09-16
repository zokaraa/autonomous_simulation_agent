import os
import glob

def folders_and_png_count():
    print("Folder name and count of PNG files:")
    
    # Loop through each folder as per previous program setup
    for i in range(1, 21):
        folder_name = f"try{i}"
        
        # Check if the folder exists
        if os.path.exists(folder_name):
            # Count PNG files in the folder
            png_files = glob.glob(os.path.join(folder_name, '*.png'))
            png_count = len(png_files)
            print(f"{folder_name}: {png_count} PNG files")
        else:
            print(f"{folder_name} does not exist.")

if __name__ == "__main__":
    folders_and_png_count()
