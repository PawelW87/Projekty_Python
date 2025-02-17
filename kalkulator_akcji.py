import os
import numpy as np
import pandas as pd
import requests
from datetime import timedelta

def create_path_write(folder):
    """
    Takes filename from user.
    """
    filename = input("Enter the name of the file to write (without extension): ") + '.xlsx'
    path = os.path.join(folder, filename)
    return path

def import_transactions(csv_file):
    """
    Reads CSV. Creates DataFrame with useful columns. Converts 'Time' column to datetime objects.
    """
    columns_to_load = ['Time', 'Side', 'Symbol ID', 'ISIN', 'Currency', 'Quantity', 'Commission', 'Commission Currency', 'Traded Volume']

    df = pd.read_csv(csv_file, sep='\t', header=0, encoding='utf-16', usecols=columns_to_load)

    df['Time'] = pd.to_datetime(df['Time'])
    
    return df  

def get_nbp_exchange_rate(currency, date):

    """
    Gets the exchange rate from the NBP API website for the previous business day.

    Parameters:

    currency: Three letters currency shortcut
    date: Date in datetime format object.
    
    Returns:

    Rate
    Date of the course

    """
   
    new_date = date - timedelta(days=1)

    has_date = False

    while not has_date:        
        format_date = new_date.strftime('%Y-%m-%d')
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}/{format_date}/?format=json"
        try:                                   
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            has_date = True                                  
        except:                                
            has_date = False            # back one day before
            print(f"Brak kursu dla {currency.upper()} z dnia {format_date}.\nSzukam w poprzednim dniu")  
            new_date -= timedelta(days=1)

    rate = (data["rates"][0]['mid'])
    rate_date = (data["rates"][0]['effectiveDate'])
    return rate, rate_date

def assign_exchange_rate(row):
    """
    Assigns the currency rate and date taken from the NBP
    """

    currency = row['Currency']
    date = row['Time']
    
    if currency == 'PLN':
        rate = 1
        rate_date = date.date()
    else:
        rate, rate_date = get_nbp_exchange_rate(currency, date)
    
    return pd.Series([rate, rate_date])

def write_to_excel(df, folder):
    try:
        df.to_excel(create_path_write(folder), index=False, header=True)
        print(f"Writing successful")
    except Exception as e:
        print(f"Unexpected error: {e}")

def add_exchange_rate(df):
    """
    Adds the NBP exchange rate and the exchange rate date to the DataFrame.

    The function calls `assign_exchange_rate` for each row,
    to fill the 'NBP Rate' and 'NBP Date' columns.

    Args:
    df (pd.DataFrame): DataFrame with stock market transaction data.

    Returns:
    pd.DataFrame: Updated DataFrame with added columns.
    """
    df[['NBP Rate', 'NBP Date']] = df.apply(assign_exchange_rate, axis=1)
    return df

def calculate_pln_values(df):
    """
    Calculates and adds columns to the DataFrame representing financial values in PLN (Polish Zloty).
    
    The function performs the following operations:
    1. Calculates 'PLN Traded Volume' by multiplying the 'NBP Rate' with 'Traded Volume'.
    2. Calculates 'PLN Commission' based on the 'NBP Rate' and 'Commission', if the 'Currency' matches the 'Commission Currency'.
       Otherwise, it returns 'Currency error'.
    3. Calculates 'PLN Values minus costs' by adjusting the 'PLN Traded Volume' with the 'PLN Commission'.
       The result is different for 'buy' and 'sell' sides: for 'buy', it adds the values, while for 'sell', it subtracts them.
       If the 'Side' is not 'buy' or 'sell', it returns 'Calculation error'.
    
    Args:
        df (pandas.DataFrame): A DataFrame containing columns 'NBP Rate', 'Traded Volume', 'Currency', 'Commission Currency', 'Commission', and 'Side'.
    
    Returns:
        pandas.DataFrame: The updated DataFrame with the added columns 'PLN Traded Volume', 'PLN Commission', and 'PLN Values minus costs'.
    """
    df['PLN Traded Volume'] = df['NBP Rate'] * df['Traded Volume']
    
    df['PLN Commission'] = df.apply(
    lambda row: row['NBP Rate'] * row['Commission'] if row['Currency'] == row['Commission Currency'] else 'Currency error',
    axis=1)

    df['PLN Values minus costs'] = df.apply(
    lambda row: row['PLN Traded Volume'] + row['PLN Commission'] if row['Side'] == 'buy' else 
    (row['PLN Traded Volume'] - row['PLN Commission'] if row['Side'] == 'sell' else 'Calculation error'), axis=1)
    
    return df

def add_manual_transaction(df):
    """
    Allows the user to manually add a transaction to the DataFrame.
    This feature now ensures that missing columns (such as purchases from previous years) are added to manually entered rows.
    """
    while True:
        add_transaction = input("Do you want to add a manual transaction? (y/n): ").strip().lower()
        
        if add_transaction == 'n':
            break
        
        try:
            symbol_id = input("Enter Symbol ID: ").strip().upper()
            time_str = input("Enter Time (YYYY-MM-DD HH:MM:SS): ").strip()
            time = pd.to_datetime(time_str)
            quantity = float(input("Enter Quantity: "))
            pln_values = float(input("Enter PLN Values minus costs: "))
            
            # Create a new DataFrame for the new transaction with columns required by other functions
            new_transaction = pd.DataFrame({
                'Symbol ID': [symbol_id],
                'Time': [time],
                'Side': ['buy'],
                'Quantity': [quantity],
                'PLN Values minus costs': [pln_values],
                'Currency': ['PLN'],  # Assuming PLN currency for the transaction
                'Commission': [0],
                'Commission Currency': ['PLN'],
                'Traded Volume': [0],
                'NBP Rate': [1],  # Set default exchange rate as 1 for PLN (since it's in PLN)
                'NBP Date': [time.date()]  # Use the entered time as the exchange rate date
            })

            # Display transaction details for confirmation
            print(f"Transaction Details:")
            print(new_transaction.to_string(index=False))
            confirm = input("Confirm this transaction? (y/n): ").strip().lower()
            
            if confirm == 'y':
                df = pd.concat([df, new_transaction], ignore_index=True)
                print("Transaction added successfully.\n")
            else:
                print("Transaction discarded.\n")

        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Please try again and ensure all fields are entered correctly.\n")
    
    return df

def calculate_profit(df):
    """
    Calculates the profit for each 'sell' transaction by matching it with previous 'buy' transactions
    using FIFO principle. The function calculates profit for each sale as the difference between the 
    sale value and the corresponding buy value for each unique 'Symbol ID'.

    Adds a new column 'Profit' to the DataFrame, where for 'buy' transactions the value is 'null',
    and for 'sell' transactions the value is the calculated profit.

    Args:
        df (pandas.DataFrame): DataFrame with stock market transaction data including 'PLN Values minus costs',
        'Side', 'Time', 'Symbol ID', 'Quantity' and other relevant columns.

    Returns:
        pandas.DataFrame: The updated DataFrame with the added 'Profit' column.
    """
    # Dictionary to store the FIFO queue for each Symbol ID
    fifo_queues = {}
    profits = []  # To store the profit for each transaction
   
    for _, row in df.iterrows():
        symbol = row['Symbol ID']
        transaction_type = row['Side']
        quantity = row['Quantity']
        value = row['PLN Values minus costs']
        
        if symbol not in fifo_queues:
            fifo_queues[symbol] = []

        if transaction_type == 'buy':
            # Add the buy transaction to the FIFO queue for the current Symbol ID
            fifo_queues[symbol].append({
                'PLN Values minus costs': value,
                'Quantity': quantity,
                })
            profits.append(np.nan)  # For buys, profit is NaN (null)
            
        elif transaction_type == 'sell':
            total_sell_value = value
            total_sell_quantity = quantity
            total_profit = 0
            super_total_sell_quantity = quantity

            # Process the sell transaction, matching with buys in FIFO order for the current Symbol ID
            while fifo_queues[symbol] and total_sell_quantity > 0:
                buy_transaction = fifo_queues[symbol].pop(0)  # Get the oldest buy transaction
                buy_value = buy_transaction['PLN Values minus costs']
                buy_quantity = buy_transaction['Quantity']
                                            
                # Calculate the proportional buy value based on the quantity being sold
                if buy_quantity <= total_sell_quantity:
                    # If buy quantity is smaller or equal to the quantity sold
                    total_profit += (total_sell_value * (buy_quantity / super_total_sell_quantity)) - buy_value
                    total_sell_quantity -= buy_quantity
                    
                else:
                    # If buy quantity is larger, adjust the remaining sell quantity
                    total_profit += total_sell_value * (total_sell_quantity / super_total_sell_quantity) - (total_sell_quantity / buy_quantity) * buy_value
                    buy_price = buy_value / buy_quantity
                    buy_transaction['PLN Values minus costs'] -= total_sell_quantity * buy_price
                    buy_transaction['Quantity'] -= total_sell_quantity
                    fifo_queues[symbol].insert(0, buy_transaction)  # Put back the remaining buy portion
                    break
            
            profits.append(total_profit)
        else:
            profits.append(np.nan)  # In case there's an invalid 'Side' value

    df['Profit'] = profits
    
    return df

def main():
    FOLDER = 'csv_files'
    # csv_file = r'csv_files\Akcje.csv'
    csv_file = input("Enter the path to the CSV file: ").strip()
    df = import_transactions(csv_file)
    add_exchange_rate(df)
    calculate_pln_values(df)
    df = add_manual_transaction(df)
    df = df.sort_values(by=['Symbol ID', 'Time'])
    df = calculate_profit(df)
    # print(df)
    print(df.to_string()) ### Present all rows.
    # write_to_excel(df, FOLDER)

if __name__ == "__main__":
    main()