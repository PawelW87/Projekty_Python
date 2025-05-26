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
    columns_to_load = ['Time', 'Side', 'Symbol ID', 'ISIN', 'Price', 'Currency', 'Quantity', 'Commission', 'Commission Currency', 'Traded Volume']

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
    Calculates PLN-related financial values for a given DataFrame.

    This function adds the following columns to the DataFrame:
    - 'PLN Traded Volume': The traded volume converted to PLN using the NBP exchange rate.
    - 'PLN Commission': The commission converted to PLN based on the NBP rate, 
      with validation that the currency matches the commission currency.
      If the currencies do not match, an error message 'Currency error' is added.
    - 'PLN INCOME': The traded volume in PLN for rows where the 'Side' is 'sell'; 
      for other rows, this value is set to 0.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the transaction data. 
        Required columns: 
        - 'NBP Rate'
        - 'Traded Volume'
        - 'Commission'
        - 'Currency'
        - 'Commission Currency'
        - 'Side'

    Returns:
    -------
    pandas.DataFrame
        The updated DataFrame with the calculated columns.
    """
    df['PLN Traded Volume'] = df['NBP Rate'] * df['Traded Volume']
    
    df['PLN Commission'] = df.apply(
    lambda row: row['NBP Rate'] * row['Commission'] if row['Currency'] == row['Commission Currency'] else 'Currency error',
    axis=1)
    
    df['PLN INCOME - PRZYCHÓD'] = np.where(df['Side'] == 'sell', df['PLN Traded Volume'], 0)

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
            pln_values = float(input("Enter PLN Traded Volume: "))
            commision = float(input("Enter PLN Commission: "))
            # Create a new DataFrame for the new transaction with columns required by other functions
            new_transaction = pd.DataFrame({
                'Symbol ID': [symbol_id],
                'Time': [time],
                'Side': ['buy'],
                'Quantity': [quantity],
                'PLN Traded Volume': [pln_values],
                'Currency': ['PLN'],  # Assuming PLN currency for the transaction
                'PLN Commission': [commision],
                'Commission Currency': ['PLN'],
                'Traded Volume': [0],
                'NBP Rate': [1],  # Set default exchange rate as 1 for PLN (since it's in PLN)
                'NBP Date': ['---'],  # Use the entered time as the exchange rate date
                'Price': [0]
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
    Calculates the profit and costs for 'sell' transactions using the FIFO principle to match them 
    with previous 'buy' transactions for each unique 'Symbol ID'.

    For each 'sell', the function computes the profit as the difference between the sell value and 
    the matched buy costs, including proportional commissions. Adds two new columns to the DataFrame:
        - 'Costs': Total costs (including commissions) for each transaction.
        - 'Profit': Profit for 'sell' transactions (NaN for 'buy').

    Args:
        df (pandas.DataFrame): DataFrame containing columns:
            'Symbol ID', 'Side', 'Quantity', 'PLN Traded Volume', and 'PLN Commission'.

    Returns:
        pandas.DataFrame: Updated DataFrame with 'Profit' and 'Costs' columns.
    """
    # Dictionary to store the FIFO queue for each Symbol ID
    fifo_queues = {}
    profits = []  # To store the profit for each transaction
    costs = []  # To store the cost for each transaction
    status = [] # To store the status for 'sell' transaction
    warnings = []   # To track missing 'buy' for 'sell' transactions

    for _, row in df.iterrows():
        symbol = row['Symbol ID']
        transaction_type = row['Side']
        quantity = row['Quantity']
        value = row['PLN Traded Volume']
        commission = row['PLN Commission']
        
        if symbol not in fifo_queues:
            fifo_queues[symbol] = []

        if transaction_type == 'buy':
            # Add the buy transaction to the FIFO queue for the current Symbol ID
            fifo_queues[symbol].append({
                'PLN Traded Volume': value,
                'Quantity': quantity,
                'PLN Commission': commission,
                })
            profits.append(np.nan)
            costs.append(np.nan)
            status.append(np.nan)  # For buys, profit, cost and status is NaN (null)
            warnings.append(None)
            
        elif transaction_type == 'sell':
            total_sell_value = value
            total_sell_quantity = quantity
            total_sell_commission = commission
            total_cost = 0
            super_total_sell_quantity = quantity
            
            if not fifo_queues[symbol]:
                # If no 'buy' transactions are available
                warnings.append(f"Missing 'buy' for 'sell' transaction of {quantity} units in {symbol}.")
                profits.append(None)
                costs.append(None)
                status.append(None)
                continue

            # Process the sell transaction, matching with buys in FIFO order for the current Symbol ID
            while fifo_queues[symbol] and total_sell_quantity > 0:
                buy_transaction = fifo_queues[symbol].pop(0)  # Get the oldest buy transaction
                buy_value = buy_transaction['PLN Traded Volume']
                buy_quantity = buy_transaction['Quantity']
                buy_commission = buy_transaction['PLN Commission']
                                            
                if buy_quantity <= total_sell_quantity:
                    # If buy quantity is smaller or equal to the quantity sold
                    total_cost += buy_value + buy_commission + (buy_quantity / super_total_sell_quantity) * total_sell_commission       
                    total_sell_quantity -= buy_quantity
                    summary = 'Settled'
                else:
                    # If buy quantity is larger, adjust the remaining sell quantity
                    total_cost += (total_sell_quantity / buy_quantity) * (buy_value + buy_commission) + (total_sell_quantity / super_total_sell_quantity) * total_sell_commission
                    # Returns unsold units to the FIFO queue
                    buy_transaction['PLN Traded Volume'] -= (total_sell_quantity / buy_quantity) * buy_value
                    buy_transaction['Quantity'] -= total_sell_quantity
                    buy_transaction['PLN Commission'] -= (total_sell_quantity / buy_quantity) * buy_commission
                    fifo_queues[symbol].insert(0, buy_transaction)  # Put back the remaining buy portion
                    summary = f"Remains: {sum(transaction['Quantity'] for transaction in fifo_queues[symbol])}"
                    break
            
            profits.append(total_sell_value - total_cost)
            costs.append(total_cost)
            status.append(summary)
            warnings.append(None)

        else:
            profits.append(np.nan)  # In case there's an invalid 'Side' value
            costs.append(np.nan)
            status.append(np.nan)
            warnings.append(None)

    df['COSTS - KOSZT'] = costs
    df['PROFIT - DOCHÓD'] = profits
    df['STATUS'] = status
    df['Warnings'] = warnings
        
    return df

def map_exchange_to_country(df):
    """
    Maps stock exchange identifiers to country codes based on the 'Side' column value.

    If the 'Side' column is 'sell', the function extracts the exchange from the 'Symbol ID'
    and returns the corresponding country code. If 'Side' is not 'sell', it returns None.

    Args:
        df (pandas.DataFrame): A DataFrame containing the 'Symbol ID' and 'Side' columns.

    Returns:
        pandas.DataFrame: The original DataFrame with an additional 'Exchange country' column.
    """

    exchange_to_country = {
        "WSE": "PL",
        "EURONEXT": "Check",
        "XETRA": "DE",
        "NYSE": "US",
        "NASDAQ": "US",
        "BATS": "US",
        "AMEX": "US",
        "ARCA": "US",
        "SIX": "CH",
        "LSE": "GB",
        "SOMX": "SE",
        "TSX": "CA",
        "ASX": "AU",    
    }
    
    def get_country(row):
        if row['Side'] == 'sell':
            exchange = row['Symbol ID'].split('.')[-1]
            return exchange_to_country.get(exchange, "UNKNOWN")
        else:
            return None
    
    df['Exchange country'] = df.apply(get_country, axis=1)

    return df

def main():
    FOLDER = 'csv_files'
    csv_file = input("Enter the path to the CSV file: ").strip()
    df = import_transactions(csv_file)
    add_exchange_rate(df)
    calculate_pln_values(df)
    df = add_manual_transaction(df)
    df = df.sort_values(by=['Symbol ID', 'Time'])
    df = calculate_profit(df)
    df = map_exchange_to_country(df)
    # print(df.to_string()) ### Present all rows.
    write_to_excel(df, FOLDER)

if __name__ == "__main__":
    main()