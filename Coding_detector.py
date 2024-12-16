"""program wykrywający kodowanie"""

import chardet

with open(r'csv_files\Custom_.csv', 'rb') as file:
    raw_data = file.read()  # Wczytaj pierwsze 10KB pliku
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Kodowanie wykryte przez chardet: {encoding}")
