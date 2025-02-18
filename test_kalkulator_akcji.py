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
    "Side": ["buy", "buy", "buy", "buy", "sell", "sell"],
    "Symbol ID": ["ABC123", "ABC123", "ABC123", "ABC123", "ABC123", "ABC123"],
    "ISIN": ["PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890", "PL1234567890"],
    "Currency": ["PLN", "PLN", "PLN", "PLN", "PLN", "PLN"],
    "Quantity": [100, 50, 200, 50, 125, 265],
    "Commission": [1.0, 1.0, 2.00, 1.0, 1.25, 2.65],
    "Commission Currency": ["PLN", "PLN", "PLN", "PLN", "PLN", "PLN"],
    "Traded Volume": [10000, 4900, 18000, 4900, 12375, 37100],
}

df = pd.DataFrame(data)
df['Time'] = pd.to_datetime(df['Time'])
add_exchange_rate(df)
calculate_pln_values(df)
add_manual_transaction(df)
df = df.sort_values(by=['Symbol ID', 'Time'])
calculate_profit(df)
print(df)
write_to_excel(df, FOLDER)



####### Printy przydatne do diagnozy

# chyba źle total_profit += (buy_quantity / super_total_sell_quantity) * total_sell_value - total_cost
# total_profit += (total_sell_quantity / super_total_sell_quantity) * total_sell_value - total_cost

# print(f"IFprzed FIFO:{buy_transaction}")
# print(f"IF PO cost:{total_cost}, profit{total_profit}\n, total_sell:{total_sell_quantity}, super total:{super_total_sell_quantity}\n, buy value:{buy_value}, buy commission:{buy_commission}")
# print(f"buy quantity:{buy_quantity}, total sell commission{total_sell_commission}, total_sell_value:{total_sell_value}\n")

# print(f"ELSEprzed FIFO:{buy_transaction}")

# print(f"ELSE PO back buy transakction: {buy_transaction}")
# print(f"cost:{total_cost}, profit{total_profit}\n, total_sell:{total_sell_quantity}, super total:{super_total_sell_quantity}\n, buy value:{buy_value}, buy commission:{buy_commission}")
# print(f"buy quantity:{buy_quantity}, total sell commission{total_sell_commission}, total_sell_value:{total_sell_value},\n,\n,\n,")