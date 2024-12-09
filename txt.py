import os
import sys

# txt_files path
FOLDER = 'txt_files' 

# List of .txt files in FOLDER
txt_files = os.listdir(FOLDER)

filename = input("Enter the name of the file to open: ")
if filename == "":
    if txt_files:
        filename = txt_files[0]
    else:
        print("No .txt files in FOLDER.")
        sys.exit(1)


# A path for the selected file in Folder
path = os.path.join(FOLDER, filename) 


def open_file(path):
    """Opens and reads the file."""
    try:
        with open(path, 'r') as file:
            content = file.read()
            return content    
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    

def main():
    content = open_file(path)
    print(content)
    
    
if __name__ == "__main__":
    main()