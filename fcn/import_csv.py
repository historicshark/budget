import datetime
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog


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
def import_debit(file: str) -> pd.DataFrame:
    data = pd.read_csv(file)

    # Combine credit and debit columns
    data['Amount'] = data['Debit'].fillna(data['Credit'])

    data = data.rename(columns={'Description': 'Location'})

    data.drop(columns=['Account', 'Memo', 'Check #', 'Credit', 'Debit', 'Category'], inplace=True) #XXX dropping category

    # Remove slash at the end of debit category
    # data['Category'] = data['Category'].map(lambda x: x[:-1])

    # Remove credit card payments from debit
    data = data[~data['Location'].str.contains('CARDMEMBER SERV  WEB PYMT')]

    # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
    data['Date'] = data['Date'].apply(date_to_iso)

    # Negative of debit amounts so that spending is positive
    # data.Amount = data.Amount.map(lambda x: -x)

    return data


# df with Date, Location, Amount
def import_credit(file: str) -> pd.DataFrame:
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


def date_to_iso(date, add_year=False) -> str:
    ''' MM/DD/YYYY --> YYYY-MM-DD '''
    date = date.split('/')
    date = [date[2], date[0], date[1]]
    if add_year:
        date[0] = str(datetime.date.today())[0:2] + date[0]
    return '-'.join(date)

