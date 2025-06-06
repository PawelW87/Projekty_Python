import pandas as pd

LISTA_PLATNIKOW = 'PayMonitor/uczestnicy.txt'
WYCIAG_BANKOWY = 'PayMonitor/wyciag.xlsx'
RAPORT_PATH = 'PayMonitor/raport.txt'

class Participant:
    """
    Represents a participant who is expected to pay a specific amount.

    Attributes:
        full_name (str): The full name of the participant, in uppercase.
        expected_amount (float): The amount the participant is expected to pay.
        paid (bool): Indicates whether the participant has paid the full amount.
        amount_paid (float): The total amount the participant has paid so far.
    """

    def __init__(self, full_name, expected_amount):
        self.full_name = full_name.strip().upper()
        self.expected_amount = float(expected_amount)
        self.paid = False  # Default: unpaid
        self.amount_paid = 0.0  # Default: 0 zł

    def add_payment(self, amount):
        """
        Adds a payment amount to the participant's total paid amount.

        Args:
            amount (float): The payment amount to add.
        """
        self.amount_paid += amount
        if self.amount_paid >= self.expected_amount:
            self.paid = True

class Payment:
    """
    Represents a single payment transaction.

    Attributes:
        full_name (str): The name of the payer, in uppercase.
        amount (float): The amount of the payment.
    """

    def __init__(self, full_name, amount):
        self.full_name = full_name.strip().upper()
        self.amount = float(amount)

def load_participants(filename):
    """
    Loads a list of participants from a text file.

    Args:
        filename (str): Path to the file containing participant data.

    Returns:
        list: A list of Participant objects.
    """
    participants = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    full_name, amount = line.split(',', 1)
                    participants.append(Participant(full_name, amount))
                except ValueError:
                    print(f"Błąd w linii: {line}")
    return participants

def extract_name_from_payment_field(field):
    """
    Extracts the name from a multiline payment field.

    Args:
        field (str): The multiline string containing payment details.

    Returns:
        str: The extracted name in uppercase.
    """
    lines = field.strip().split('\n')
    if len(lines) > 1:
        name = ' '.join(lines[1].strip().split()[:2]).upper()
        return name
    else:
        return ''

def load_payments(xlsx_filename):
    """
    Loads payment data from an Excel file.

    Args:
        xlsx_filename (str): Path to the Excel file.

    Returns:
        list: A list of Payment objects.
    """
    payments = []
    df = pd.read_excel(xlsx_filename)
    for idx, row in df.iterrows():
        payer_name = extract_name_from_payment_field(str(row['Nadawca / odbiorca']))
        amount = row['Kwota']
        if payer_name and not pd.isnull(amount):
            payments.append(Payment(payer_name, amount))
    return payments

def match_payments(participants, payments):
    """
    Matches payments to participants and updates their payment status.

    Args:
        participants (list): List of Participant objects.
        payments (list): List of Payment objects.
    """
    for payment in payments:
        for participant in participants:
            if participant.full_name == payment.full_name:
                participant.add_payment(payment.amount)

def print_report(participants):
    """
    Prints and saves a report of participants who have or have not paid.

    Args:
        participants (list): List of Participant objects.
    """
    with open(RAPORT_PATH, 'w', encoding='utf-8') as f:
        print("Klienci, którzy nie zapłacili:\n")
        f.write("Klienci, którzy nie zapłacili:\n")
        for p in participants:
            if not p.paid:
                print(f"{p.full_name} - oczekiwano: {p.expected_amount} zł, wpłynęło: {p.amount_paid} zł")
                f.write(f"{p.full_name} - oczekiwano: {p.expected_amount} zł,   wpłynęło: {p.amount_paid} zł\n")

        print("\nKlienci, którzy zapłacili:\n")
        f.write("\nKlienci, którzy zapłacili:\n")
        for p in participants:
            if p.paid:
                print(f"{p.full_name} - oczekiwano: {p.expected_amount} zł, wpłynęło: {p.amount_paid} zł")
                f.write(f"{p.full_name} - oczekiwano: {p.expected_amount} zł,   wpłynęło: {p.amount_paid} zł\n")
    print("Raport został zapisany do pliku raport.txt")

def print_payment_names(payments):
    """
    Prints the names of payers from the payment list.

    Args:
        payments (list): List of Payment objects.
    """
    print("Lista osób z pliku bankowego:")
    for payment in payments:
        print(f"{payment.full_name}, {payment.amount}")

def main():
    """
    Main function to load data, match payments, and generate a report.
    """
    participants = load_participants(LISTA_PLATNIKOW)
    payments = load_payments(WYCIAG_BANKOWY)
    # print_payment_names(payments)
    match_payments(participants, payments)
    print_report(participants)

if __name__ == "__main__":
    main()
