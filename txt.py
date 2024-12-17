import os
import sys

def create_path(folder, txt_files):
    """
    Takes filename to open from user or takes 1st file in folder
    """
    filename = input("Enter the name of the file to open: ")
    if filename == "":
        if txt_files:
            filename = txt_files[0]
            print(f"Selected file is '{filename}'")
        else:
            print("No .txt files in FOLDER.")
            sys.exit(1)
    path = os.path.join(folder, filename)
    return path

def create_path_write(folder):
    """
    Takes filename from user.
    """
    filename = input("Enter the name of the .txt file to write (without extension): ") + '.txt'
    path = os.path.join(folder, filename)
    return path

def open_file(path):
    """
    Opens and reads the file.
    """
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
    
def save_file(path: str, text: str, mode: str):
    """
    Write text to file.

    Parameters:

    path: Name of the file to which the text is to be written.
    text: Text to write to file.
    mode: File opening mode. Available options:
        - 'a': Append data to file.
        - 'w': Overwrite file contents.
        - 'x': Create new file (error if file already exists).

    Exceptions:
    - ValueError: when 'mode' is not one of ['a', 'w', 'x'].
    - FileNotFoundError: when paths to file are invalid.
    - PermissionError: when permissions to write file are missing.
    - OSError: for errors in other file operations.
    """

    # Mode validation
    allowed_modes = ['a', 'w', 'x']
    if mode not in allowed_modes:
        raise ValueError(f"Invalid mode {mode}. Available modes are: 'a', 'w' or 'x'")

    try:
        with open(path, mode) as file:
            file.write(text)
        print("Success")
    except FileNotFoundError:
        print(f"Error: File '{path}' not found or path is invalid.")
    except PermissionError:
        print(f"Error: No permission to write to file '{path}'.")
    except OSError as e:
        print(f"General filesystem error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def ask_for_direction(content, folder):
    """
    Asks the user what to do:

    add:    The user enters text and the program add it and write to a new file.
    y:      The program saves data to a new file.
    n:      Program ends operation.

    """
    ask_for_direction = input('Would you like to save a data to new file or add something? y/n/add: ')

    new_file = False #Flag

    if ask_for_direction.lower() == 'add':
        text = content + '\n' + input("Input text for write: ")
        new_file = True
    elif ask_for_direction.lower() == 'y':
        text = content
        new_file = True
    elif ask_for_direction.lower() == 'n':
        new_file = False
        print("Stop.")
        sys.exit(1)
    else:
        new_file = False
        print("Unexpected answer.")
        sys.exit(1)
        
    if new_file is True:
        path_1 = create_path_write(folder)
        save_file(path_1, text, mode='a')

def main():
    FOLDER = 'txt_files' 
    txt_files = os.listdir(FOLDER)
    path = create_path(FOLDER, txt_files)
    content = open_file(path)
    print(content)
    ask_for_direction(content, FOLDER)
   
if __name__ == "__main__":
    main()