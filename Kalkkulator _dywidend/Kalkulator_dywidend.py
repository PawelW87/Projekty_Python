import os
import pandas as pd
import requests
from datetime import timedelta

def import_transactions(csv_file):
    """
    Reads CSV. Creates DataFrame with useful columns. Converts 'When' column to datetime objects.
    """
    columns_to_load = ['Symbol ID', 'Operation type', 'When', 'Sum', 'Asset', 'Comment']

    df = pd.read_csv(csv_file, sep='\t', header=0, encoding='utf-16', usecols=columns_to_load)
    
    df['When'] = pd.to_datetime(df['When'])

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

def add_exchange_rate(row):
    """
    Assigns the currency rate and date taken from the NBP
    """

    currency = row['Asset']
    date = row['When']
    
    if currency == 'PLN':
        rate = 1
        rate_date = date.date()
    else:
        rate, rate_date = get_nbp_exchange_rate(currency, date)
    
    return pd.Series([rate, rate_date])

def extract_dividend_info(df):
    """
    Extracts and adds two new columns to the given DataFrame based on the information in the 'Comment' column.

    - The column 'DIV paid' is extracted from the text enclosed in parentheses after "(-" in the 'Comment' column. 
      The extracted value represents the percentage of the dividend paid (e.g., "-15.000%"), excluding the parentheses.
    - The column 'DIV Country' is extracted from the keyword "DivCntry" in the 'Comment' column, capturing the country code 
      (e.g., "US" or "DE") that follows it.

    Args:
        df (pandas.DataFrame): A DataFrame containing a column named 'Comment' with dividend-related information.

    Returns:
        pandas.DataFrame: The modified DataFrame with two additional columns:
            - 'DIV paid %': Contains the dividend percentage paid as a string.
            - 'DIV Country': Contains the country code of the dividend as a string.
    """
    df['DIV paid %'] = df['Comment'].apply(
    lambda comment: comment[comment.find("(-") + 2:comment.find(")", comment.find("(-"))]
    if "(-" in comment else None
)
    df['DIV Country'] = df['Comment'].str.extract(r'DivCntry (\w+)')
    return df

def create_path_write(folder):
    """
    Takes filename from user.
    """
    filename = input("Enter the name of the file to write (without extension): ") + '.xlsx'
    path = os.path.join(folder, filename)
    return path

def write_to_excel(df, folder):
    try:
        df.to_excel(create_path_write(folder), index=False, header=True)
        print(f"Writing successful")
    except Exception as e:
        print(f"Unexpected error: {e}")

def calc_the_tax(df):
    """
    Processes a DataFrame to calculate additional columns related to dividends and taxes.

    - Divides the DataFrame into rows with 'DIVIDEND' and rows with 'TAX' or 'US TAX'.
    - Joins 'DIVIDEND' rows with 'TAX/US TAX' rows based on 'Symbol ID' and 'NBP Date'.
    - Calculates the sum of '19% TAX' and 'PLN Sum' to create the 'Dopłata' column.
    - Adds a new column 'DIV paid' that maps the 'PLN Sum' from 'TAX/US TAX' rows to 'DIVIDEND' rows.

    Args:
        df (pandas.DataFrame): The input DataFrame containing columns:
            - 'Operation type'
            - 'Symbol ID'
            - 'NBP Date'
            - '19% TAX'
            - 'PLN Sum'

    Returns:
        pandas.DataFrame: The modified DataFrame with additional columns:
            - 'Dopłata': Sum of '19% TAX' and 'PLN Sum' for 'DIVIDEND' rows.
            - 'DIV paid': The 'PLN Sum' from 'TAX/US TAX' rows displayed for 'DIVIDEND' rows.
    """

    # Separate rows for 'DIVIDEND' and 'TAX/US TAX'
    dividend_df = df[df['Operation type'] == 'DIVIDEND'][['Symbol ID', 'NBP Date', '19% TAX']]
    tax_df = df[df['Operation type'].isin(['TAX', 'US TAX'])][['Symbol ID', 'NBP Date', 'PLN Sum']]

    # Join 'DIVIDEND' rows with 'TAX/US TAX' rows
    merged_df = pd.merge(dividend_df, tax_df, on=['Symbol ID', 'NBP Date'], how='left')

    # Calculate 'Dopłata'
    merged_df['Dopłata'] = merged_df['19% TAX'] + merged_df['PLN Sum']

    # Add 'DIV paid' column for 'DIVIDEND' rows
    merged_df['DIV paid'] = merged_df['PLN Sum']

    # Merge the results back into the original DataFrame
    df = pd.merge(df, merged_df[['Symbol ID', 'NBP Date', 'DIV paid', 'Dopłata']], on=['Symbol ID', 'NBP Date'], how='left')

    # Ensure 'Dopłata' and 'DIV paid' are only for 'DIVIDEND' rows
    df.loc[df['Operation type'] != 'DIVIDEND', ['DIV paid', 'Dopłata']] = None

    return df

def check_tax_corrections(df):
    """
    Assigning the 'KOREKTA' word to the 'Dopłata' column if word 'recalculation' is in 'Comment'
    """
    df['Dopłata'] = df['Dopłata'].where(~df['Comment'].str.contains('recalculation', case=False), 'KOREKTA')
    return df

def show_FUNDING_WITHDRAWAL(df):
    """
    Present fundings and withdrawals
    """
    df_FUNDING_WITHDRAWAL = df[df['Operation type'].isin(['FUNDING/WITHDRAWAL'])].copy()  
    total_sum = df_FUNDING_WITHDRAWAL['Sum'].sum()
    print(df_FUNDING_WITHDRAWAL)
    print(f"Suma wpłat i wypłat to: {total_sum} EUR")

def main():
    FOLDER = 'csv_files'
    csv_file = r'csv_files\div24.csv'
    df = import_transactions(csv_file)
    # print(df.to_string()) ### Present all rows.
    # print(df)
    # show_FUNDING_WITHDRAWAL(df)
    df_filtered = df[df['Operation type'].isin(['DIVIDEND', 'TAX', 'US TAX'])].copy()
    df_filtered[['NBP Rate', 'NBP Date']] = df_filtered.apply(add_exchange_rate, axis=1)
    df_filtered = extract_dividend_info(df_filtered)
    df_filtered['PLN Sum'] = df_filtered['NBP Rate'] * df_filtered['Sum']
    df_filtered.loc[df_filtered['Operation type'] == 'DIVIDEND', '19% TAX'] = df_filtered['PLN Sum'] * 0.19
    df_filtered2 = check_tax_corrections(calc_the_tax(df_filtered))
    print(df_filtered2)
    write_to_excel(df_filtered2, FOLDER)


if __name__ == "__main__":
    main()