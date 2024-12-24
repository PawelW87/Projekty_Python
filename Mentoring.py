#   https://docs.google.com/document/d/1iJyhmVdYkBUF_lFekd1ZIm_9Y8Oa2FWMjTxlfUYVZcc/edit?tab=t.0#heading=h.yf97mum0tywb
#   https://docs.google.com/document/d/1iJyhmVdYkBUF_lFekd1ZIm_9Y8Oa2FWMjTxlfUYVZcc/edit?usp=sharing

# a = 5 / 10
# def dodaj(a: int , b):
#     """ opis funkcji """ 
#     return a + b

# class Animal:
#     colour = 'black'
#     def __init__(self, age, weight):
#         self.age = age
#         self.weight = weight

#     def parameter(self):
#         return self.age * self.weight
    


# dog = Animal(15, 5.3)
# print(dog)
# print(dog.colour)
# print(dog.age)
# dog_2 = Animal(10, 11)
# print(dog_2)
# print(dog_2.colour)
# print(dog_2.age)

# Animal.colour = 'white'
# print(Animal.colour)
# print(dog.colour)

# dog.age = 20
# print(dog.age)
# print(dog_2.age)
# dog.weight = 5.3
# print(dog.weight)
# print(dog_2.weight)
# print(dog.parameter())

# przerobić:
#     programowanie obiektowe (OOP python)
# https://www.w3schools.com/python/python_classes.asp
# + kolejne tematy do modułów i jak będzie czas to wiecej

# D:\IT\pwproject\cwicznie.py

# class Kot:
#     def miałcz(self):
#         print('miau')

# k1 = Kot()
# k1.miałcz()

### DZIEDZICZENIE###

# class Pojazd:
#     def __init__(self, marka: str):
#         self.marka = marka

#     def przedstaw_sie(self):
#         print(f'Jestem pojazdem marki {self.marka}.')


# class Motocykl(Pojazd):
#     def __init__(self, marka: str, typ_motocykla: str):
#         super().__init__(marka)
#         self.typ_motocykla = typ_motocykla
    
#     def przedstaw_sie(self):
#         print(f"Motocykl marki {self.marka}, typ {self.typ_motocykla}.")

# class Enduro(Motocykl):
#     def __init__(self, marka: str, typ_motocykla: str, zawieszenie: str = 'standardowe'):
#         super().__init__(marka, typ_motocykla) 
#         self.zawieszenie = zawieszenie
    
#     def przedstaw_sie(self):
#         # print(f"Motocykl marki {self.marka}, typ {self.typ_motocykla}, zawieszenie {self.zawieszenie}.")
#         super().przedstaw_sie()                             ###alternatywnie
#         print(f'Zawieszenie: {self.zawieszenie}.')          ###alternatywnie

# # "Python język interpretowany - "


# enduro1 = Enduro('BMW', 'turystyczny')
# enduro1.przedstaw_sie()




### DZIEDZICZENIE###

# class Pojazd:
#     def __init__(self, marka: str):
#         self.marka = marka

#     def przedstaw_sie(self):
#         print(f'Jestem pojazdem marki {self.marka}.')


# class Motocykl(Pojazd):
#     def __init__(self, marka: str, typ_motocykla: str, silnik: 'Motocykl.Silnik', opony: 'Motocykl.Opony'):
#         super().__init__(marka)
#         self.typ_motocykla = typ_motocykla
#         self.silnik = silnik
#         self.opony = opony

#     @staticmethod
#     def przypomnienie_olej():
#         print('Remember to change an oil every 5000 km!')

#     class Opony:
#         def __init__(self, srednica: int, grubosc: float):
#             self.srednica = srednica
#             self.grubosc = grubosc


#     class Silnik:
#         def __init__(self, pojemnosc: int, typ: str, paliwo : str = 'benzyna', chlodzenie: str = 'powietrzem'):
#             self.pojemnosc = pojemnosc
#             self.typ = typ
#             self.paliwo = paliwo
#             self.chlodzenie = chlodzenie
        
#         # def przedstaw_sie(self):
#             # print(f"Silnik o pojemności {self.pojemnosc} cm3, typ {self.typ}, paliwo: {self.paliwo}, chlodzenie: {self.chlodzenie}")
    
#     def przedstaw_sie(self):
#         silnik_info = f"Silnik o pojemności {self.silnik.pojemnosc} cm3, typ {self.silnik.typ}, paliwo: {self.silnik.paliwo}, chlodzenie: {self.silnik.chlodzenie}"
#         opony_info = f"Rozmiar opon: {self.opony.srednica} cali srednica, {self.opony.grubosc} cali profil."
#         print(f"Motocykl marki {self.marka}, typ {self.typ_motocykla}.")
#         print(silnik_info)
#         print(opony_info)
#         Motocykl.przypomnienie_olej()

#         # print(f"Motocykl marki {self.marka}, typ {self.typ_motocykla}.")
#         # self.silnik.przedstaw_sie()

# silnik1 = Motocykl.Silnik(350, 'dwusuwowy')
# silnik2 = Motocykl.Silnik(250, 'czterosuwowy', chlodzenie='cieczą')
# silnik3 = Motocykl.Silnik(650, 'czterosuwowy', 'benzyna')
# opony1 = Motocykl.Opony(18, 3.50)
# opony2 = opony1
# opony4 = Motocykl.Opony(17, 2.75)
# opony3 = Motocykl.Opony(18, 4.00)


# motocykl1 = Motocykl('Jawa', 'turystyczny', silnik1, opony1)
# motocykl1.przedstaw_sie()

# motocykl2 = Motocykl('CZ', 'sportowy', silnik2, opony2)
# motocykl2.przedstaw_sie()

# motocykl3 = Motocykl('BMW', 'szosowo-turystyczny', silnik3, opony3)
# motocykl3.przedstaw_sie()

# silnik4 = Motocykl.Silnik(350, 'dwusuw', 'benzyna z olejem')
# motocykl4 = Motocykl('Iż', 'terenowo ruski', silnik4, opony4)
# motocykl4.przedstaw_sie()

# Motocykl.przypomnienie_olej()


# """POLIMORFIZM"""
# class Instrument:
#     def zagraj(self):
#         print("nuty proszę")
    
#     def opis(self):
#         return "jestem instrumentem muzycznym"

# class Gitara(Instrument,):
#     def zagraj(self):
#         print("dring")

#     def opis(self):
#         return "jestem gitarą"

# class Pianino(Instrument):
#     def zagraj(self):
#         print("a a a")
    
#     def opis(self):
#         return "jestem pianino"

# class Perkusja(Instrument):
#     def zagraj(self):
#         print("bum bum bum")

#     def opis(self):
#         return "jestem perkusja"

# instruments = [Gitara(), Pianino(), Perkusja()]

# # for i in instruments:
# #     print("\n",i.opis())
# #     i.zagraj()

# class Orkiestra:
#     def __init__(self, instruments):
#         self.instruments = instruments

#     def koncert(self):
#         print("Zaczynamy koncert. Instrumenty:")
#         for i in self.instruments:
#             print(i.opis())
#             i.zagraj()

# orkiestra = Orkiestra(instruments)
# orkiestra.koncert()

# class Pojazd:
#     def opis(self):
#         print('to jest pojazd')

# class Samochód(Pojazd):
#     def opis(self):
#         print('to jest samochód osobowy z 4 kołami')

# class Motocykl(Pojazd):
#     def opis(self):
#         print('to jest motocykl z 2 kołami')

# list = [Samochód(), Motocykl()]

# for l in list:
#     l.opis()

# """USUWANIE ATRYBUTÓW OBIEKTÓW"""
# class Telefon:
#     def __init__(self, marka):
#         self.marka = marka
    
#     def przedstaw_sie(self):
#         if hasattr(self, 'marka'):
#             print(f"jestem telefon firmy {self.marka}.")
#         else:
#             print('nie podano marki telefonu')

# telef1 = Telefon('Nokia')
# telef1.przedstaw_sie()
# del telef1.marka
# telef1.przedstaw_sie()

# """ITERATORY"""

# class Liczby:
#     def __init__(self, start, stop):
#         if start % 2 != 0:
#             start += 1
#         self.start = start
#         self.stop = stop
#         self.current = start
        

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.current > self.stop:
#             raise StopIteration
#         else:
#             self.current += 2
#             return self.current - 2

# # Tworzymy iterator
# liczby = Liczby(2, 20)

# # Używamy go w pętli
# for liczba in liczby:
#     print(liczba)

# Praca domowa: zabawa z plikami :) godz. 21:15
# context menager - zarządzanie kontekstem 21:19
# zapis 
# 1. stworzyć nowy program zapis do pliku i odczyt .txt . 21:21
# 2. zapis i odczyt csv. Moduł CSV z Pythona. 
# 3. SQLite podstawowa baza danych - jeśli starczy czasu to stworzyć bazę. 21:28



#18-12-2024   self introduction musi mówić co ja chce. praktyczny python.
#doświadczenie na dół bo nie jest ważne. na górze projekty
#umiejętności rozpisac. biblioteki pythona. co osiągnąłem.


#no flaw jobs poszukać 

#justjoin.it
#https://justjoin.it/  #ogłoszenia prac IT
#zakładka analityka, data, other, pySPark, Power BI
# nofluffjobs.com/pl
# https://nofluffjobs.com/pl
# https://bulldogjob.com/
# pracuj.pl

# 19-12-2024
# 20:41
# Zadanie: 1. Grafika, wizualizacja wyników działań. Wykresy. ogarnąć bibliotekę Plotly! jakie funkcje, (dash) 
# 1a) NumPy

# 2. komunikacja z bazami danych
# 3. menu w formie pęti while do csv_1.py ->modyfikacja ask_for_direktion()