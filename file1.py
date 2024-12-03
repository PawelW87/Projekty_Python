"""this is the first file in training repo"""
' this line is for "new-features" branch'
'this line was created in gitgub in develop branch'

# class Lakiery:
#     def __init__(self, rodzaj: str, kolor: str):
#         self.rodzaj = rodzaj
#         self.kolor = kolor

#     def __str__(self):
#         print(f"lakier {self.rodzaj}, kolor {self.kolor}.")

# lak1 = Lakiery("nitroceluloza", "bezbarwny")
# lak2 = Lakiery('akrylowy', 'biały')
# lak3 = Lakiery('ftalowy', 'zielony')

# list = [lak1, lak2, lak3]

# for l in list:
#     l.__str__()


import csv 
from dataclasses import dataclass
from datetime import datetime

# csv_file = 
# with open(csv_file, encoding="utf-8") as stream:
#             reader = csv.DictReader(stream)

date_str = "29.12.2023 14:16"

def convert_date(date_str):
    date_obj = datetime.strptime(date_str.strip(), "%d.%m.%Y %H:%M")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

print(convert_date(date_str))

class Transactions:
    def __init__(self, id: str, operation: str, date, amount: float, comment: str, ):
        self.id = id
        self.operation = operation
        self.date = date
        self.amount = amount
        self.comment = comment

    def convert_date(self):
        date_format = self.time

    def show_transaction(self):
        print(f"{self.id} {self.operations} {self.date_format} {self.amount}{self.comment}")