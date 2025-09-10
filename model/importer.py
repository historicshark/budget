from collections.abc import Sequence
import datetime
import pandas as pd
from pathlib import Path
from ofxparse import OfxParser

from model.database import DatabaseManager
from model.record import Record

class Importer(Sequence):
    def __init__(self, db: DatabaseManager, file=''):
        super().__init__()
        self.file = file
        self.set_file(file)
        self.db = db
        self.data: list[Record] = []
        self.records_to_skip: set[int] = set()

    def __getitem__(self, i: int) -> Record:
        return self.data[i]

    #def __setitem__(self, i: int, item: dict[str, str]):
    #    assert isinstance(item, dict)
    #    for key in ['Date', 'Location', 'Amount']:
    #        assert key in item.keys()
    #    self.data.__setitem__(i, item)

    #def __delitem__(self, i: int):
    #    self.data.__delitem__(i)

    def __len__(self):
        return len(self.data)

    #def insert(self, i: int, item: dict[str, str]):
    #    assert isinstance(item, dict)
    #    for key in ['Date', 'Location', 'Amount']:
    #        assert key in item.keys()
    #    self.data.insert(i, item)

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
        self.records_to_skip = set()
        if self.file.lower().endswith(('.csv', '.txt')):
            self.import_file_csv(account)
        elif self.file.lower().endswith(('.ofx','.qbo','.qfx')):
            self.import_file_ofx()

    # Functions to load a csv file. Different processing is needed for each account because the format is different.
    def import_file_csv(self, account: str) -> None:
        raise NotImplementedError('todo') #TODO dict -> Record
        match account:
            case 'credit':
                self.data = self.import_credit_csv()
            case 'debit':
                self.data = self.import_debit_csv()
            case _:
                raise ValueError(f'Invalid account import option {account}')
    
    def import_debit_csv(self) -> list[Record]:
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

        #return data.to_dict('records')
        return [Record(row.Date, row.Location, '', row.Amount) for row in data.itertuples(index=False)]

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
        self.data = []
        for transaction in ofx.account.statement.transactions:
            if 'INTERNET PAYMENT THANK YOU' in transaction.payee or 'CARDMEMBER SERV  WEB PYMT' in transaction.payee: #TODO skip rules?
                print(f'skipping transaction {transaction.payee} {transaction.date.date()} on import') #XXX debug
                continue

            self.data.append(Record(date=str(transaction.date.date()),
                                    location=str(transaction.payee),
                                    amount=f'{transaction.amount:.2f}', # transaction.amount is a Decimal type
                                    category='')
                            )

    def set_category(self, index: int, category: str):
        assert 0 <= index < len(self.data)
        #print(f'categorized transaction {self.data[index].location} as {category}') #XXX debug
        self.data[index].category = category

    def date_to_iso(self, date: str, add_year=False) -> str:
        ''' MM/DD/YYYY --> YYYY-MM-DD '''
        date = date.split('/')
        date = [date[2], date[0], date[1]]
        if add_year:
            date[0] = str(datetime.date.today())[0:2] + date[0]
        return '-'.join(date)

    def skip_record(self, i: int):
        self.records_to_skip.add(i)

    def insert_records_into_database(self):
        self.data = [record for i, record in enumerate(self.data) if i not in self.records_to_skip]
        for record in self.data:
            assert bool(record.category)
        self.db.insert_records(self.data)
