from collections.abc import Sequence
import datetime
import json
import pandas as pd
from pathlib import Path
from ofxparse import OfxParser

from fcn.database import DatabaseManager

class Importer(Sequence):
    def __init__(self, db: DatabaseManager, file=''):
        super().__init__()
        self.file = ''
        self.set_file(file)
        self.rules_file = 'fcn/category_rules.json'
        self.categories_file = 'fcn/categories.json'
        self.db = db

        self.rules = self.load_category_rules()
        self.categories = self.load_categories()
        self.data: list[dict[str, str]] = []  # Amount, Location, Date, (Category)
    
    def __getitem__(self, i):
        return self.data[i]
    
    def __len__(self):
        return len(self.data)

    # Set the file to be imported
    def set_file(self, file: str) -> bool:
        if Path(file).exists():
            self.file = file
            return True
        else:
            return False
    
    # Import the file set by set_file
    def import_file(self, account: str) -> None:
        assert Path(self.file).exists()
        if self.file.lower().endswith(('.csv', '.txt')):
            self.import_file_csv(account)
        elif self.file.lower().endswith(('.ofx','.qbo','.qfx')):
            self.import_file_ofx()

    # Functions to load a csv file. Different processing is needed for each account because the format is different.
    def import_file_csv(self, account: str) -> None:
        match account:
            case 'credit':
                self.data = self.import_credit_csv()
            case 'debit':
                self.data = self.import_debit_csv()
            case _:
                raise ValueError(f'Invalid account import option {account}')
    
    def import_debit_csv(self) -> list[dict[str, str]]:
        data = pd.read_csv(self.file, dtype=str)

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
        return data.to_dict('records')

    def import_credit_csv(self) -> list[dict[str, str]]:
        data = pd.read_csv(self.file, dtype=str)

        # Change date format from 'MM/DD/YYYY' (or MM/DD/YY' if add_year=True) to 'YYYY-MM-DD'
        # credit_data['Date'] = credit_data['Date'].apply(util.date_to_iso, args=(True,))

        data = data[~data['Name'].str.contains('INTERNET PAYMENT THANK YOU')]
        data = data.drop(columns=['Transaction', 'Memo'])
        data = data.rename(columns={'Name': 'Location'})
        return data.to_dict('records')
    
    # Function to import ofx-type files.
    def import_file_ofx(self) -> None:
        with open(self.file) as f:
            ofx = OfxParser.parse(f)
        self.data = [
            {
                'Amount':   str(transaction.amount),
                'Location': str(transaction.payee),
                'Date':     str(transaction.date.date())
            }
            for transaction in ofx.account.statement.transactions
        ]

    def set_category(self, index: int, category: str):
        assert 0 <= index < len(self.data)
        assert category in self.categories #XXX add category?
        self.data[index]["Category"] = category

    def date_to_iso(self, date: str, add_year=False) -> str:
        ''' MM/DD/YYYY --> YYYY-MM-DD '''
        date = date.split('/')
        date = [date[2], date[0], date[1]]
        if add_year:
            date[0] = str(datetime.date.today())[0:2] + date[0]
        return '-'.join(date)

    # Load json file containing category rules of {"keyword": "category"}
    def load_category_rules(self) -> dict[str, str]:
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

    # Load json file containing a list of categories
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
    
    def guess_category(self, index: int) -> str:
        location = self.data[index]['Location'].lower()
        for keyword in self.rules.keys():
            if keyword in location:
                return self.rules[keyword]
        return self.categories[0]

    def add_new_category_rule(self, keyword: str, category: str) -> None:
        self.rules[keyword.lower()] = category
        self.dump_category_rules()
        return
    
    def add_new_category(self, new_category: str) -> None:
        if new_category in self.categories:
            raise ValueError(f'Category {new_category} already exists!')
        
        self.categories.append(new_category)
        self.dump_categories()
        return
    