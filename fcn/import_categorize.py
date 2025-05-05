import datetime
import json
import pandas as pd
from pathlib import Path


class Importer():
    def __init__(self, file=''):
        self.file = ''
        self.set_file(file)
        self.rules_file = 'fcn/category_rules.json'
        self.categories_file = 'fcn/categories.json'

        self.rules = self.load_category_rules()
        self.categories = self.load_categories()
        
        # Hold the current index of the iterator for categorizing the transactions
        self.data = pd.DataFrame()
        self.index = -1
        self.length = -1

    def __iter__(self):
        assert self.length >= 0
        return self
    
    def __next__(self) -> pd.Series:
        self.index += 1
        if self.index < self.length:
            return self.data.iloc[self.index]
        raise StopIteration 


    # Set the file to be imported
    def set_file(self, file: str) -> bool:
        if Path(file).exists():
            self.file = file
            return True
        else:
            return False

    def import_file(self, account: str) -> None:
        match account:
            case 'credit':
                self.data = self.import_credit()
            case 'debit':
                self.data = self.import_debit()
            case _:
                raise ValueError(f'Invalid account import option {account}')
        self.length = self.data.shape[0]
    
    # Functions to load the file into a data frame with columns "Date", "Location", "Amount"
    def import_debit(self) -> pd.DataFrame:
        data = pd.read_csv(self.file)

        # Combine credit and debit columns
        data['Amount'] = data['Debit'].fillna(data['Credit'])

        data = data.rename(columns={'Description': 'Location'})
        data.drop(columns=['Account', 'Memo', 'Check #', 'Credit', 'Debit', 'Category'], inplace=True) #XXX dropping category

        # Remove slash at the end of debit category
        # data['Category'] = data['Category'].map(lambda x: x[:-1])

        # Remove credit card payments from debit
        data = data[~data['Location'].str.contains('CARDMEMBER SERV  WEB PYMT')]

        # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
        data['Date'] = data['Date'].apply(self.date_to_iso)

        # Negative of debit amounts so that spending is positive
        # data.Amount = data.Amount.map(lambda x: -x)
        return data

    def import_credit(self) -> pd.DataFrame:
        data = pd.read_csv(self.file)

        # Combine credit and debit columns
        data['Amount'] = data['Debit'].fillna(data['Credit'])

        data = data.rename(columns={'Description': 'Location'})
        data.drop(columns=['Account', 'Memo', 'Check #', 'Credit', 'Debit', 'Category'], inplace=True) #XXX dropping category

        # Remove slash at the end of debit category
        # data['Category'] = data['Category'].map(lambda x: x[:-1])

        # Remove credit card payments from debit
        data = data[~data['Location'].str.contains('CARDMEMBER SERV  WEB PYMT')]

        # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
        data['Date'] = data['Date'].apply(self.date_to_iso)

        # Negative of debit amounts so that spending is positive
        # data.Amount = data.Amount.map(lambda x: -x)
        return data

    def date_to_iso(self, date: str, add_year=False) -> str:
        ''' MM/DD/YYYY --> YYYY-MM-DD '''
        date = date.split('/')
        date = [date[2], date[0], date[1]]
        if add_year:
            date[0] = str(datetime.date.today())[0:2] + date[0]
        return '-'.join(date)

    def load_category_rules(self) -> dict:
        if Path(self.rules_file).exists():
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        else:
            print(f'Attempted to load rules file {self.rules_file}, but it doesn\'t exist. No rules are loaded!')
            return {}

    def dump_category_rules(self) -> None:
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
        return

    def load_categories(self) -> list[str]:
        if Path(self.categories_file).exists():
            with open(self.categories_file, 'r') as f:
                category_options = json.load(f)
            return category_options
        else:
            raise FileNotFoundError(self.categories_file)

    def dump_categories(self) -> None:
        print('dumping categories!')
        with open(self.categories_file, 'w') as f:
            json.dump(self.categories, f, indent=2)
        return
    
    def guess_category(self, location: str) -> str:
        location = location.lower()
        for keyword in self.rules.keys():
            if keyword in location:
                return self.rules[keyword]
        return 'Unknown'
