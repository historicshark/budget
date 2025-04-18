import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import util


def import_file(rest):
    if rest:
        try:
            print(rest[0])
            file = Path(rest[0])
            assert file.exists()
        except:
            print(f'file "{rest[0]}" not found. Select using popup box')
            file = open_file_gui()
    else:
        file = open_file_gui()

    import_type = input('Input 1 (c) to import credit or 2 (d) for debit\n>>> ')
    if import_type.lower() in ['1', 'c']:
        data = import_credit(file)
    elif import_type.lower() in ['2', 'd']:
        data = import_debit(file)
    else:
        raise Exception('Input credit or debit!')
    return data


# df with Date, Location, Amount
def import_debit(file):
    debit_data = pd.read_csv(file)

    # Combine credit and debit columns
    debit_data['Amount'] = debit_data['Debit'].fillna(debit_data['Credit'])

    debit_data = debit_data.rename(columns={'Description': 'Location'})

    debit_data.drop(columns=['Account', 'Memo', 'Check #', 'Credit', 'Debit', 'Category'], inplace=True) #XXX dropping category

    # Remove slash at the end of debit category
    # debit_data['Category'] = debit_data['Category'].map(lambda x: x[:-1])

    # Remove credit card payments from debit
    debit_data = debit_data[~debit_data['Location'].str.contains('CARDMEMBER SERV  WEB PYMT')]

    # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
    debit_data['Date'] = debit_data['Date'].apply(util.date_to_iso)

    # Negative of debit amounts so that spending is positive
    # debit_data.Amount = debit_data.Amount.map(lambda x: -x)

    return debit_data


# df with Date, Name, Amount
def import_credit(file):
    data = pd.read_csv(file)

    # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
    # credit_data['Date'] = credit_data['Date'].apply(util.date_to_iso, args=(True,))

    data = data[~data['Name'].str.contains('INTERNET PAYMENT THANK YOU')]
    data = data.drop(columns=['Transaction', 'Memo'])
    data = data.rename(columns={'Name': 'Location'})

    return data


def open_file_gui() -> Path:
    root = tk.Tk()
    root.withdraw()
    return Path(filedialog.askopenfilename())

