from dataclasses import asdict
import datetime
from decimal import Decimal
import numbers
import numpy as np
import pandas as pd
from pathlib import Path
import sqlite3

from model.record import Record

class DatabaseManager:
    def __init__(self, db_name):
        if not Path(db_name).exists():
            print(f'Creating new database {db_name}')
            self.con = sqlite3.connect(db_name)
            self.cur = self.con.cursor()
            self.cur.execute('CREATE TABLE transactions(Date, Location, Category, Amount)')
        else:
            self.con = sqlite3.connect(db_name)
            self.cur = self.con.cursor()

        # Get table name
        res = self.cur.execute('SELECT name FROM sqlite_master')
        self.table_name = res.fetchone()[0]
        self.where = ''

    def insert_records(self, records: list[Record]):
        """
        convert records to list of dicts for named insertion
        """
        self.cur.executemany(f'INSERT INTO {self.table_name} VALUES(:date, :location, :category, :amount)', [record.asdict() for record in records])
        self.con.commit()

    #TODO need to test
    def insert_record(self, record: Record):
        self.cur.execute(f'INSERT INTO {self.table_name} VALUES(:date, :location, :category, :amount)', record.asdict())
        self.con.commit()

    def delete(self, date=None, location=None, category=None, amount=None):
        #if date:
        #    if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
        #    if not all(isinstance(elem, datetime.date) for elem in date): raise ValueError('Provide date range as a list of two dates!')

        #if amount:
        #    if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
 
        command = f"DELETE FROM {self.table_name}"

        self.build_where(date, location, category, amount)

        #XXX debug
        # print(command + self.where + order)
        #print('deleting the following records:')
        #self.select_and_print(date=date, location=location, category=category, amount=amount)

        self.cur.execute(command + self.where)
        self.con.commit()

    def select_filter(self, filters) -> list[dict[str, str]]:
        return self.select(date=filters['Date'], category=filters['Category'], amount=filters['Amount'])

    def select(self, date=None, location=None, category=None, amount=None, order_by=None) -> list[Record]:
        """ 
        Return a list of records. Any or none of the arguments can be provided.
        Also sets db.where for future use.

        Date: A list containing two datetime.date for a date range
        Location: str matching name of location (not recommended)
        Category: str or list[str] matching categories
        Amount: A list containing two numbers for an amount range
        order_by: str selecting column to order entries. Choose one of 'Date', 'Location', 'Category', 'Amount'. 
        """

        if order_by and order_by not in ['Date', 'Location', 'Category', 'Amount']:
            print('In DatabaseManager.select, order_by must be one of [\'Date\', \'Location\', \'Category\', \'Amount\']. Order ignored.')
            order_by = None

        #if date:
        #    if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
        #    if not all(isinstance(elem, datetime.date) for elem in date): raise ValueError('Provide date range as a list of two dates!')

        #if amount:
        #    if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
        
        command = f"SELECT Date, Location, Category, Amount FROM {self.table_name}"

        self.build_where(date, location, category, amount)

        if order_by:
            order = ' ORDER BY ' + order_by
        else:
            order = ''

        #print(command + self.where + order) #XXX debug

        res = self.cur.execute(command + self.where + order)
        output = res.fetchall() # list of tuples
        #return [dict(zip(['Date','Location','Category','Amount'], values)) for values in output]
        return [Record(date=values[0], location=values[1], category=values[2], amount=values[3]) for values in output]
    
    def update(self,
               old_date=None, old_location=None, old_category=None, old_amount=None,
               new_date=None, new_location=None, new_category=None, new_amount=None):
        """
        update() does an UPDATE operation on one record in the database. 

        old/new_date: datetime.date
        old/new_location: str
        old/new_category: str
        old/new_amount: number
        """
        self.build_where(old_date, old_location, old_category, old_amount)

        set_statement = 'SET'
        if new_date:
            set_statement += f' Date = "{new_date}",'

        if new_location:
            set_statement += f' Location = "{new_location}",'

        if new_category:
            set_statement += f' Category = "{new_category}",'

        if new_amount:
            if isinstance(new_amount, str):
                new_amount = Decimal(new_amount)
            set_statement += f' Amount = "{new_amount:.2f}",'

        set_statement = set_statement[:-1]

        command = f'UPDATE {self.table_name}\n{set_statement}\n{self.where}'
        #print(command) #XXX debug
        self.cur.execute(command)
        self.con.commit()

    def update_record(self, old_record: Record, new_record: Record):
        self.update(old_record.date, old_record.location, old_record.category, old_record.amount,
                    new_record.date, new_record.location, new_record.category, new_record.amount)

    def add_and(self, use_and):
        if use_and:
            self.where += ' AND '
        return True

    def build_where(self, date, location, category, amount):
        """
        adds a WHERE statement to self.where
        - date and amount can be a single value or range
        - category can be a single value or a list
        """
        if not (date or location or category or amount):
            self.where = ''
            return

        self.where = '\nWHERE '
        use_and = False

        if date:
            use_and = self.add_and(use_and)
            if isinstance(date, (list, tuple)):
                self.where += f'Date BETWEEN "{date[0]}" AND "{date[1]}"'
            else:
                self.where += f'Date="{date}"'

        if location:
            use_and = self.add_and(use_and)
            self.where += f'Location="{location}"'

        if category:
            use_and = self.add_and(use_and)
            if isinstance(category, (list, tuple)):
                category = [f'"{c}"' for c in category]
                self.where += f'Category IN ({", ".join(category)})'
            else:
                self.where += f'Category="{category}"'

        if amount:
            use_and = self.add_and(use_and)
            if isinstance(amount, (list, tuple)):
                self.where += f'abs(Amount) BETWEEN {amount[0]} AND {amount[1]}'
            elif isinstance(amount, str):
                self.where += f'Amount="{amount}"'
            else:
                self.where += f'Amount="{amount:.2f}"'

    def print_records(self, records):
        """
        Print a list of records return by db.Select
        """

        width_date = 10
        width_location = 25
        width_category = 23
        width_amount = 9

        line_separator = '-' * (13+width_date+width_amount+width_category+width_location)

        print(f'''
{line_separator}
| {"Date":^{width_date}} | {"Location":^{width_location}} | {"Category":^{width_category}} | {"Amount":^{width_amount}} |
{line_separator}''')
        for record in records:
            print(f'| {record.date_str():^{width_date}} | {record.location[:width_location]:^{width_location}} | {record.category:^{width_category}} | {record.amount:^{width_amount}} |')
        print(line_separator)

    def select_and_print(self, date=None, location=None, category=None, amount=None):
        ''' Make easy to make a selection and print it in one function '''
        records = self.select(date, location, category, amount)
        self.print_records(records)

    def list_categories(self) -> list[str]:
        ''' Return a list of all categories in the database. '''
        command = "SELECT DISTINCT Category FROM " + self.table_name
        res = self.cur.execute(command)
        return [category[0] for category in res.fetchall()]

    def totals_by_category(self, date_range=None) -> tuple[list[str], np.array]:
        ''' date_range: list of str for a range (YYYY-MM-DD YYYY-MM-DD) '''
        categories = self.list_categories()
        totals = []
        for category in categories:
            self.cur.execute(f'SELECT SUM("Amount") FROM {self.table_name} WHERE Category = ?', (category,))
            totals.append(self.cur.fetchone()[0])

        return categories, np.array(totals)
