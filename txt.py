import os
import sys

def create_path(folder, txt_files):
    """Takes filename from user or takes 1st file in folder"""
    filename = input("Enter the name of the file to open: ")
    if filename == "":
        if txt_files:
            filename = txt_files[0]
        else:
            print("No .txt files in FOLDER.")
            sys.exit(1)
    path = os.path.join(folder, filename)
    return path

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
    
def save_file(nazwa_pliku, tekst):
    
    with open(nazwa_pliku, 'w') as file:
        file.write(tekst)

# Wywołanie funkcji
zapisz_do_pliku('przykladowy_plik.txt', "To jest przykładowy tekst.")


def main():
    FOLDER = 'txt_files' 
    txt_files = os.listdir(FOLDER)
    path = create_path(FOLDER, txt_files)
    content = open_file(path)
    print(content) 
    
if __name__ == "__main__":
    main()