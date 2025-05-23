import datetime
from pathlib import Path
import sqlite3

import pandas as pd
import numpy as np

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

    #Good?
    def insert(self, date=None, location=None, category=None, amount=None, array=None):
        """
        Provide date, location, category, amount as lists or single values of str, str, str, float.
        array is a df with columns Date, Location, Amount, Category
        """

        if array is None:
            # If all are lists, execute many
            if isinstance(date, list) and isinstance(location, list) and isinstance(category, list) and isinstance(amount, list):
                if not (len(date) == len(location) and len(date) == len(category) and len(date) == len(amount)): raise ValueError('All lists must be the same length!')
                if not all(isinstance(elem, str)   for elem in date):     raise TypeError('date must contain all strings!')
                for row in date: self.check_date_format(row)
                if not all(isinstance(elem, str)   for elem in location): raise TypeError('location must contain all strings!')
                if not all(isinstance(elem, str)   for elem in category): raise TypeError('category must contain all strings!')
                if not all(isinstance(elem, float) or isinstance(elem, int) for elem in amount): raise TypeError('amount must contain all floats!')

                data = list(zip(date, location, category, amount))

                self.cur.executemany('INSERT INTO ' + self.table_name + ' VALUES(?, ?, ?, ?)', data)
                self.con.commit()

                return True

            # only adding a single entry
            elif isinstance(date, str) and isinstance(location, str) and isinstance(category, str) and (isinstance(amount, float) or isinstance(amount, int)):
                self.check_date_format(date)
                self.cur.execute("INSERT INTO " + self.table_name + " VALUES ('" + date + "', '" + location + "', '" + category + "', " + str(amount) + ")")
                self.con.commit()

                return True

            else:
                raise TypeError('Error in arguments to insert(date, location, category, amount)')

        elif isinstance(array, pd.DataFrame):
            date = array['Date']
            location = array['Location']
            category = array['Category']
            amount = array['Amount']

            for date_, location_, category_, amount_ in zip(date, location, category, amount):
                self.check_date_format(date_)
                self.cur.execute(f'INSERT INTO {self.table_name} VALUES("{date_}", "{location_}", "{category_}", "{amount_}")')
            self.con.commit()

            return True

        else:
            raise TypeError('Error in arguments!')


    #Good?
    def delete(self, date=None, location=None, category=None, amount=None):
        """
        specify any or no parameters to delete command.
        date: str or [str, str]
        location: str
        category: str
        amount: float or [float, float]
        """

        while True: # Loop for changing delete command.
            # Input checks
            use_date         = isinstance(date, str)
            use_date_range   = isinstance(date, list) or isinstance(date, tuple)
            use_location     = isinstance(location, str)
            use_old_category = isinstance(category, str)
            use_amount       = isinstance(amount, float) or isinstance(amount, int)
            use_amount_range = isinstance(amount, list) or isinstance(amount, tuple)

            if use_date_range:
                if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
                if not all(isinstance(elem, str) for elem in date): raise ValueError('Provide date range as a list of two strings!')

            if use_amount_range:
                if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
                if not all(isinstance(elem, float) or isinstance(elem, int) for elem in amount): raise ValueError('Provide amount range as a list of two numbers!')

            # Build DELETE command. use_and is a flag set to true if AND needs to be added between WHERE conditions.
            command = "DELETE FROM " + self.table_name

            # Build WHERE command
            if not (use_date or use_date_range or use_location or use_old_category or use_amount or use_amount_range): # no input provided. delete all records
                self.where = ''
            else: # go through all inputs
                self.where = "\nWHERE "
                use_and = False

                if use_date:
                    self.check_date_format(date)
                    use_and = True
                    self.where += "Date=\"" + date + "\""

                if use_date_range:
                    self.check_date_format(date[0])
                    self.check_date_format(date[1])
                    use_and = True
                    self.where += "Date BETWEEN \"" + date[0] + "\" AND \"" + date[1] + "\""

                if use_location:
                    if use_and:
                        self.where += " AND "
                    else:
                        use_and = True
                    self.where += "Location=\""  + location + "\""

                if use_old_category:
                    if use_and:
                        self.where += " AND "
                    else:
                        use_and = True
                    self.where += "Category=\"" + category + "\""

                if use_amount:
                    if use_and:
                        self.where += " AND "
                    else:
                        use_and = True
                    self.where += "Amount=" + str(amount)

                if use_amount_range:
                    if use_and:
                        self.where += " AND "
                    else:
                        use_and = True
                    self.where += "Amount BETWEEN " + str(amount[0]) + " AND " + str(amount[1])

            # for debugging
            # print(command + self.where + order)

            selection = self.select(date, location, category, amount)
            if len(selection) == 0:
                print('Warning: The parameters provided resulted in no records being deleted!')
                return False
            elif len(selection) == 1:
                print("Deletion is permanent. The following record will be deleted: ")
            else:
                print("Deletion is permanent. The following records will be deleted: ")
            self.print_selection(selection)

            if 'y' in input('Confirm delete?  y/[n]:\n>>> '):
                self.cur.execute(command + self.where)
                self.con.commit()
                return True

            else:
                print('Provide more information to reduce selection.')
                choice = input('1 for date, 2 for location (not recommended), 3 for category, 4 for amount, 0 to quit.\n>>> ')

                if '0' in choice:
                    return False

                if '1' in choice:
                    date = input('Input date as YYYY-MM-DD or date range as YYYY-MM-DD YYYY-MM-DD\n>>> ')
                    if ' ' in date:
                        date = list(date.split())

                if '2' in choice:
                    location = input('Input location\n>>> ')

                if '3' in choice:
                    category = input('Input category\n>>> ')

                if '4' in choice:
                    amount = input('Input amount as XX.XX or amount range as XX.XX YY.YY\n>>> ')
                    if ' ' in amount:
                        amount = [float(elem) for elem in amount.split()]


    # Good for now?
    def update_category(self, new_category, date=None, location=None, old_category=None, amount=None):
        """
        Provide the new category and other information. If multiple entries are returned, issue a warning that
        more information is needed to update only one record.
        """

        while True:
            selection = self.select(date, location, old_category, amount)
            if len(selection) == 0:
                print('Warning: The parameters provided do not match any records!')
                return False

            # If more than one records match the condition, get confirmation that all categories need to be updated.
            elif len(selection) == 1:
                self.cur.execute("UPDATE " + self.table_name + "\nSET Category=" + new_category + self.where)
                self.con.commit()
                return True

            else:
                print('Warning: This action will update multiple records to category ' + new_category + '!')
                self.print_selection(selection)

                if 'y' in input('Confirm update? Press n to reduce selection. y/[n]:\n>>> '):
                    self.cur.execute("UPDATE " + self.table_name + "\nSET Category=" + new_category + self.where)
                    self.con.commit()
                    return True

                else:
                    print('Provide more information to reduce selection.')
                    choice = input('1 for date, 2 for location (not recommended), 3 for category, 4 for amount, 0 to quit.\n>>> ')

                    if '0' in choice:
                        return False

                    if '1' in choice:
                        date = input('Input date as YYYY-MM-DD or date range as YYYY-MM-DD YYYY-MM-DD\n>>> ')
                        if ' ' in date:
                            date = list(date.split())

                    if '2' in choice:
                        location = input('Input location\n>>> ')

                    if '3' in choice:
                        old_category = input('Input category\n>>> ')

                    if '4' in choice:
                        amount = input('Input amount as XX.XX or amount range as XX.XX YY.YY\n>>> ')
                        if ' ' in amount:
                            amount = [float(elem) for elem in amount.split()]


    # Good for now?
    def select(self, date=None, location=None, category=None, amount=None, columns=None, order_by=None, take_sum=False):
        """ Return a list of tuples, each tuple is a record in the database. Any or none of the arguments can be provided.
            Also sets db.where for future use.

            Date: eiter str (YYYY-MM-DD) or list of str for a range (YYYY-MM-DD YYYY-MM-DD)
            Location: str matching name of location (not recommended)
            Category: str matching a category in the database
            Amount: float or list of 2 floats for a range
            columns: str or list of str of data columns to select. ['Date', 'Location', 'Category', 'Amount']
            order_by: str selecting column to order entries. Choose one of 'Date', 'Location', 'Category', 'Amount'. 
            take_sum: bool to take the total amount of the selection
        """

        # Input checks
        use_date         = isinstance(date, str)
        use_date_range   = isinstance(date, list) and len(date) > 0
        use_location     = isinstance(location, str)
        use_old_category = isinstance(category, str)
        use_amount       = isinstance(amount, float) or isinstance(amount, int)
        use_amount_range = isinstance(amount, list)
        use_order        = isinstance(order_by, str)
        use_columns      = isinstance(columns, list)
        use_one_column   = isinstance(columns, str)

        if use_order and order_by not in ['Date', 'Location', 'Category', 'Amount']:
            print('In DatabaseManager.select, order_by must be one of [\'Date\', \'Location\', \'Category\', \'Amount\']. Order ignored.')
            use_order = False

        if use_columns: # list of columns provided
            if not all([column in ['Date', 'Location', 'Category', 'Amount'] for column in columns]):
                raise ValueError('In DatabaseManager.select, columns to be selected must be one of [\'Date\', \'Location\', \'Category\', \'Amount\']!') # Probably can't ignore this error.

        if use_date_range:
            if len(date) != 2: raise ValueError('Provide date range as a list of two strings!')
            if not all(isinstance(elem, str) for elem in date): raise ValueError('Provide date range as a list of two strings!')

        if use_amount_range:
            if len(amount) != 2: raise ValueError('Provide amount range as a list of two numbers!')
            if not all(isinstance(elem, float) or isinstance(elem, int) for elem in amount): raise ValueError('Provide amount range as a list of two numbers!')
        
        if not isinstance(take_sum, bool): raise ValueError('take_sum must be a boolean!')
        if take_sum and (use_columns or use_one_column):
            raise ValueError('take_sum with columns is not tested!')

        # Build SELECT command. use_and is a flag set to true if AND needs to be added between WHERE conditions.
        if take_sum:
            command = f'SELECT SUM("Amount") FROM {self.table_name}'
        elif use_columns:
            command = "SELECT " + ', '.join(columns) + ' FROM ' + self.table_name
        elif use_one_column:
            command = "SELECT " + columns + ' FROM ' + self.table_name
        else:
            command = "SELECT * FROM " + self.table_name

        # Build WHERE command
        if not (use_date or use_date_range or use_location or use_old_category or use_amount or use_amount_range): # no input provided. print all records
            self.where = ''
        else: # go through all inputs
            self.where = "\nWHERE "
            use_and = False

            if use_date:
                self.check_date_format(date)
                use_and = True
                self.where += "Date=\"" + date + "\""

            if use_date_range:
                self.check_date_format(date[0])
                self.check_date_format(date[1])
                use_and = True
                self.where += "Date BETWEEN \"" + date[0] + "\" AND \"" + date[1] + "\""

            if use_location:
                if use_and:
                    self.where += " AND "
                else:
                    use_and = True
                self.where += "Location=\""  + location + "\""

            if use_old_category:
                if use_and:
                    self.where += " AND "
                else:
                    use_and = True
                self.where += "Category=\"" + category + "\""

            if use_amount:
                if use_and:
                    self.where += " AND "
                else:
                    use_and = True
                self.where += "Amount=" + str(amount)

            if use_amount_range:
                if use_and:
                    self.where += " AND "
                else:
                    use_and = True
                self.where += "Amount BETWEEN " + str(amount[0]) + " AND " + str(amount[1])

        # Build ORDER BY command
        if use_order:
            order = ' ORDER BY ' + order_by
        else:
            order = ''

        # print(command + self.where + order) #DEBUG

        res = self.cur.execute(command + self.where + order)
        return res.fetchall() # List of tuples


    # Good for now
    def print_selection(self, selection, columns=None):
        """
        Print a list of tuples return by db.Select
        If selection only contains some columns, specify which columns in columns
        """

        width_date = 10
        width_location = 25
        width_category = 23
        width_amount = 9

        if columns is None: # selection contains 4 columns
            if not all(len(row) == 4 for row in selection): raise ValueError('Columns = None, but all rows in selection don\'t have 4 elements!')
            
            line_separator = '-' * (13+width_date+width_amount+width_category+width_location)

            print(f'''
{line_separator}
| {"Date":^{width_date}} | {"Location":^{width_location}} | {"Category":^{width_category}} | {"Amount":^{width_amount}} |
{line_separator}''')
            for row in selection:
                print(f'| {row[0]:^{width_date}} | {row[1][:width_location]:^{width_location}} | {row[2]:^{width_category}} | {row[3]:^{width_amount}} |')
            print(line_separator)

        else:
            line_separator = ''
            header = '|'
            line1='-'
            line2='|'
            use_date, use_location, use_category, use_amount = False, False, False, False
            i = 0
            if 'Date' in columns:
                use_date = True
                i_date = i
                i += 1
                line_separator += '-' * (3+width_date)
                header += f' {"Date":^{width_date}} |'
            if 'Location' in columns:
                use_location = True
                i_location = i
                i += 1
                line_separator += '-' * (3+width_location)
                header += f' {"Location":^{width_location}} |'
            if 'Category' in columns:
                use_category = True
                i_category = i
                i += 1
                line_separator += '-' * (3+width_category)
                header += f' {"Category":^{width_category}} |'
            if 'Amount' in columns:
                use_amount = True
                i_amount = i
                i += 1
                line_separator += '-' * (3+width_amount)
                header += f' {"Amount":^{width_amount}} |'

            print(f'''
{line_separator}
{header}
{line_separator}''')

            for row in selection:
                line = '| '
                if use_date:     line += f'{row[i_date]:^{width_date}} | '
                if use_location: line += f'{row[i_location][:width_location]:^{width_location}} | '
                if use_category: line += f'{row[i_category]:^{width_category}} | '
                if use_amount:   line += f'{row[i_amount]:^{width_amount}} | '
                print(line)

            print(line_separator)

        return True


    # Good for now
    def select_and_print(self, date=None, location=None, category=None, amount=None, columns=None, order_by='Date', get_selection=False):
        ''' Make easy to make a selection and print it in one function '''
        selection = self.select(date, location, category, amount, columns, order_by)
        self.print_selection(selection, columns)

        if get_selection:
            return selection
        else:
            return True


    # Good
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


    # Good for now
    def check_date_format(self, date):
        ''' This function assumes that date has already been checked to be a str. '''

        # Check date formatting
        date_length = len(date)
        if date_length != 10: raise ValueError(f'Date {date} must be in format YYYY-MM-DD!')

        try:
            datetime.date.fromisoformat(date)
        except:
            raise ValueError('Date has incorrect format and could not be converted to date object!')

        return True
    
    
