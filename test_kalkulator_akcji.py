import pandas as pd
from kalkulator_akcji import add_exchange_rate, calculate_pln_values, calculate_profit, write_to_excel, add_manual_transaction

FOLDER = 'csv_files'
 # def report_():
    #     print(f"cała kolejka:{fifo_queues},\n Oldest_transakcja kupna:{buy_transaction},\n zysk:{profits}, zysk_total:{total_profit}, ilość super_sprzedaży:{super_total_sell_quantity}, wartość sprzedaży:{total_sell_value}, ilość sprzedana:{total_sell_quantity},\n wartość kupna:{buy_value}, ilość kupna:{buy_quantity} ")

data = {
    "Time": [
        "2025-02-01T10:15:30",
        "2025-02-02T14:20:00",
        "2025-02-03T11:45:00",
        "2025-02-03T15:00:00",
        "2025-02-04T09:30:00",
        "2025-02-04T16:10:00",
    ],
    "Side": ["buy", "sell", "buy", "buy", "sell", "sell"],
    "Symbol ID": ["ABC123", "ABC123", "ABC123", "ABC123", "ABC123", "ABC123"],
    "ISIN": ["PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890"],
    "Currency": ["PLN", "PLN", "PLN", "PLN", "PLN", "PLN"],
    "Quantity": [100, 50, 200, 150, 50, 250],
    "Commission": [1.50, 0.75, 2.00, 1.75, 0.60, 2.20],
    "Commission Currency": ["PLN", "PLN", "PLN", "PLN", "PLN", "PLN"],
    "Traded Volume": [10000, 5000, 20000, 15000, 5000, 25000],
}

df = pd.DataFrame(data)
df['Time'] = pd.to_datetime(df['Time'])
add_exchange_rate(df)
add_manual_transaction(df)
calculate_pln_values(df)

calculate_profit(df)

# print(df)
# write_to_excel(df, FOLDER)

