-- Wybierz wszystkie kolumny z tabeli pracownicy
-- SELECT *
-- FROM pracownicy

-- --  SQL, które wybiera imiona i zarobki pracowników z działu "IT".
-- SELECT imie, zarobki
-- FROM pracownicy
-- WHERE dzial = "IT"

-- -- SQL, które wybiera imiona pracowników, którzy zarabiają więcej niż 5000.
SELECT imie, dzial
FROM pracownicy
WHERE zarobki > 5000

-- -- SQL, które wybiera wszystkie informacje (wszystkie kolumny) o pracownikach z działu "Sprzedaż".
-- SELECT *
-- FROM pracownicy
-- WHERE dzial = 'Sprzedaz'