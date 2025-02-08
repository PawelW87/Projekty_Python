"""program wykrywający kodowanie"""

import chardet

with open(r'csv_files\Akcje.csv', 'rb') as file:
    raw_data = file.read(10000)  # Reads first 10KB.
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Kodowanie wykryte przez chardet: {encoding}")
