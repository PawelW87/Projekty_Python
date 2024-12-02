"""this is the first file in training repo"""
' this line is for "new-features" branch'
'this line was created in gitgub in develop branch'

class Lakiery:
    def __init__(self, rodzaj: str, kolor: str):
        self.rodzaj = rodzaj
        self.kolor = kolor

    def __str__(self):
        print(f"lakier {self.rodzaj}, kolor {self.kolor}.")

lak1 = Lakiery("nitroceluloza", "bezbarwny")
lak2 = Lakiery('akrylowy', 'biały')
lak3 = Lakiery('ftalowy', 'zielony')

list = [lak1, lak2, lak3]

for l in list:
    l.__str__()


class Transactions:
    def __init__(self, id: str, operation: str, date, amount: float, comment: str, ):
        self.id = id
        self.operation = operation
        self.date = date
        self.amount = amount
        self.comment = comment