import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import sqlite3

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

    def insert_records(self, records: list[dict[str, str]]):
        """
        Records is a list of dict with keys 'Date', 'Location', 'Amount', 'Category'
        """
        self.cur.executemany(f'INSERT INTO {self.table_name} VALUES(:Date, :Location, :Category, :Amount)', records)
        self.con.commit()

    # test
    def insert_record(self, record: dict[str, str]):
        self.cur.execute(f'INSERT INTO {self.table_name} VALUES(:Date, :Location, :Category, :Amount)', record)
        self.con.commit()

    def delete(self, date=None, location=None, category=None, amount=None):
        """
        Date: A list containing two datetime.date for a date range
        Location: str matching name of location (not recommended)
        Category: str or list[str] matching categories
        Amount: A list containing two numbers for an amount range
        """

        if date:
            if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
            if not all(isinstance(elem, datetime.date) for elem in date): raise ValueError('Provide date range as a list of two dates!')

        if amount:
            if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
 
        command = "DELETE FROM " + self.table_name

        self.build_where(date, location, category, amount)

        # for debugging
        # print(command + self.where + order)

        self.cur.execute(command + self.where)
        self.con.commit()

    def select(self, date=None, location=None, category=None, amount=None, order_by=None):
        """ 
        Return a list of tuples, each tuple is a record in the database. Any or none of the arguments can be provided.
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

        if date:
            if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
            if not all(isinstance(elem, datetime.date) for elem in date): raise ValueError('Provide date range as a list of two dates!')

        if amount:
            if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
        
        command = f"SELECT Date, Location, Category, Amount FROM {self.table_name}"

        self.build_where(date, location, category, amount)

        if order_by:
            order = ' ORDER BY ' + order_by
        else:
            order = ''

        # print(command + self.where + order) #DEBUG

        res = self.cur.execute(command + self.where + order)
        output = res.fetchall() # list of tuples
        return [dict(zip(['Date','Location','Category','Amount'], values)) for values in output]

    def add_and(self, use_and):
        if use_and:
            self.where += ' AND '
        else:
            use_and = True

    def build_where(self, date, location, category, amount):
        if not (date or location or category or amount):
            self.where = ''
            return

        self.where = '\nWHERE '
        use_and = False

        if date:
            self.add_and(use_and)
            self.where += f'Date BETWEEN "{date[0]}" AND "{date[1]}"'

        if location:
            self.add_and(use_and)
            self.where += f'Location="{location}"'

        if category:
            self.add_and(use_and)
            if isinstance(category, list):
                self.where += f'Category IN ({", ".join(category)})'
            else:
                self.where += f'Category={category}'

        if amount:
            self.add_and(use_and)
            self.where += f'Amount BETWEEN {amount[0]} AND {amount[1]}'

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
            print(f'| {record["Date"]:^{width_date}} | {record["Location"][:width_location]:^{width_location}} | {record["Category"]:^{width_category}} | {record["Amount"]:^{width_amount}} |')
        print(line_separator)

    def select_and_print(self, date=None, location=None, category=None, amount=None, order_by=None):
        ''' Make easy to make a selection and print it in one function '''
        records = self.select(date, location, category, amount, order_by)
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
            # self.cur.execute(f'SELECT SUM("Amount") FROM {self.table_name} WHERE Category = ?', (category,))
            total = self.select(category=category, date=date_range, take_sum=True)[0][0]
            #totals.append(self.cur.fetchone()[0])
            totals.append(total)

        return categories, np.array(totals)

