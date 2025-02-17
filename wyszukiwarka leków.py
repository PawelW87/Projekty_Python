
import json
import requests

def fetch_drug_data(active_substance):
    # Endpoint API openFDA
    base_url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"active_ingredient:\"{active_substance}\"",
        "limit": 5  # Ograniczenie do 5 wyników dla przykładu
    }
    
    try:
        # Wysyłanie żądania GET do API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Sprawdź, czy nie wystąpił błąd HTTP
        
        # Parsowanie danych w formacie JSON
        data = response.json()
        
        # Wyświetlanie nazwy leku, postaci i substancji czynnej
        print(f"Wyniki dla substancji czynnej: {active_substance}\n")
        for result in data.get("results", []):
            # brand_name = result.get("openfda", {}).get("brand_name", ["Brak danych"])[0]
            # dosage_form = result.get("dosage_and_administration", ["Brak danych"])[0]
            active_ingredient = data["results"][0]["active_ingredient"]
                     
            
            # print(f"Nazwa leku: {brand_name}")
            # print(f"Postać: {dosage_form}")
            print(f"Substancja czynna: {active_ingredient}\n")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Błąd HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Błąd połączenia: {req_err}")
    except KeyError as key_err:
        print(f"Brak klucza w danych: {key_err}")
    except json.JSONDecodeError:
        print("Nie udało się przetworzyć odpowiedzi w formacie JSON.")

# Pobranie substancji czynnej od użytkownika
active_substance = input("Podaj nazwę substancji czynnej: ")
fetch_drug_data(active_substance)

