import csv, os, sys

def csv_open(path):
    with open(path, newline='',encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        list=[]
        for r in reader:
            list.append(r)
    return list

def csv_write(path, mode, list):
    """
    Write data to file.

    Parameters:

    path: Name of the file to which the text is to be written.
    text: Text to write to file.
    mode: File opening mode. Available options:
        - 'a': Append data to file.
        - 'w': Overwrite file contents.
        - 'x': Create new file (error if file already exists).
    
    """
    with open(path, mode, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)
        print(f"Writting to the {path} file succuessful.")

def create_path_write(folder):
    """
    Takes filename from user.
    """
    filename = input("Enter the name of the file to write (with extension): ")
    path = os.path.join(folder, filename)
    return path

def present(list):
    for l in list:
        print(l, '\n')
    
def main():
    FOLDER = 'csv_files' 
    FILE = r'csv_files\div.csv'
    list = csv_open(FILE)
    present(list)
    ask_for_direction = input('Would you like to save a data to new file? y/n: ')
    if ask_for_direction.lower() == 'y':
        path = create_path_write(FOLDER)
        csv_write(path, 'x', list)
    else:
        print("Stop")
        sys.exit(1)
          
if __name__ == "__main__":
    main()