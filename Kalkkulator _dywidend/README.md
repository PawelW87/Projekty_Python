# Dividend Tax Calculation Tool

This Python script processes CSV files containing financial transactions, calculates dividend-related taxes, retrieves exchange rates from the NBP API, and exports the results to an Excel file.

## Features

- **CSV Import:** Reads transaction data from a CSV file with specific columns.
- **Exchange Rates:** Fetches historical exchange rates for different currencies from the NBP API.
- **Dividend Information:** Extracts dividend percentage and country information from comments.
- **Tax Calculation:** Calculates 19% dividend tax and provides adjustments based on recalculations.
- **Funding/Withdrawal Summary:** Displays funding and withdrawal operations with totals.
- **Excel Export:** Saves processed data into an Excel file.

## Installation

1. Ensure you have Python 3.9+ installed.
2. Install the required libraries:
    ```bash
    pip install pandas requests
    ```

## Usage

1. Place your input CSV file in the `csv_files` folder.
2. Modify the `csv_file` path in the script if necessary.
3. Run the script:
    ```bash
    python script_name.py
    ```
4. Follow the prompt to name the output Excel file.

## Input CSV Format

The script expects a tab-separated CSV file (`UTF-16` encoded) with the following columns:
- **Symbol ID**
- **Operation type**
- **When**
- **Sum**
- **Asset**
- **Comment**

## Output Excel

The resulting Excel file will contain:
- Exchange rates and dates from the NBP.
- Dividend percentage and country.
- Tax and adjustment calculations.

## Example Workflow

1. **Import Transactions:** Load transaction data into a DataFrame.
2. **Filter Operations:** Process rows related to dividends and taxes.
3. **Retrieve Exchange Rates:** Fetch the exchange rate for each transaction.
4. **Calculate Taxes:** Compute dividend taxes and adjustments.
5. **Export Results:** Save the final DataFrame to an Excel file.

## Error Handling

- If no exchange rate is available for the given date, the script looks for the previous business day.
- Handles unexpected errors when writing to an Excel file.

## Folder Structure

project/
├── script_name.py
├── csv_files/
│ └── div24.csv
├── output/


## License

This project is licensed. See the LICENSE file for details.


# Narzędzie do obliczania podatku od dywidend

Ten skrypt w Pythonie przetwarza pliki CSV zawierające dane transakcji finansowych, oblicza podatki od dywidend, pobiera kursy walut z API NBP oraz eksportuje wyniki do pliku Excel.

## Funkcje

- **Import CSV:** Odczytuje dane transakcji z pliku CSV z określonymi kolumnami.
- **Kursy walut:** Pobiera historyczne kursy walut dla różnych walut z API NBP.
- **Informacje o dywidendach:** Wyciąga procent dywidendy oraz kraj z kolumny z komentarzami.
- **Obliczenia podatkowe:** Oblicza 19% podatku od dywidend oraz uwzględnia korekty na podstawie adnotacji.
- **Podsumowanie wpłat/wypłat:** Wyświetla operacje wpłat i wypłat wraz z sumą.
- **Eksport do Excela:** Zapisuje przetworzone dane do pliku Excel.

## Instalacja

1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.9+.
2. Zainstaluj wymagane biblioteki:
    ```bash
    pip install pandas requests
    ```

## Użycie

1. Umieść plik CSV wejściowy w folderze `csv_files`.
2. W razie potrzeby zmodyfikuj ścieżkę `csv_file` w skrypcie.
3. Uruchom skrypt:
    ```bash
    python script_name.py
    ```
4. Podaj nazwę dla pliku wynikowego w formacie Excel.

## Format pliku wejściowego CSV

Skrypt oczekuje pliku CSV rozdzielonego tabulatorami (`UTF-16`) z następującymi kolumnami:
- **Symbol ID**
- **Operation type**
- **When**
- **Sum**
- **Asset**
- **Comment**

## Wynikowy plik Excel

Wynikowy plik Excel będzie zawierał:
- Kursy walut i daty pobrane z NBP.
- Procent dywidendy i kraj jej wypłaty.
- Obliczenia podatkowe i ewentualne korekty.

## Przykładowy przepływ pracy

1. **Import danych:** Wczytaj dane transakcji do DataFrame.
2. **Filtrowanie operacji:** Przetwarzaj wiersze związane z dywidendami i podatkami.
3. **Pobieranie kursów walut:** Pobierz kurs waluty dla każdej transakcji.
4. **Obliczanie podatków:** Oblicz podatki od dywidend i dopłaty.
5. **Eksport wyników:** Zapisz końcowe dane do pliku Excel.

## Obsługa błędów

- Jeśli kurs waluty nie jest dostępny dla wskazanej daty, skrypt wyszukuje dane dla wcześniejszego dnia roboczego.
- Obsługuje nieoczekiwane błędy podczas zapisu do pliku Excel.

## Struktura katalogów

projekt/
├── script_name.py
├── csv_files/
│ └── div24.csv
├── output/


## Licencja

Ten projekt jest licencjonowany. Szczegóły znajdziesz w pliku LICENSE.
