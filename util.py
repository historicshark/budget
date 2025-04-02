import datetime
from pathlib import Path

def column(array, i):
    return [row[i] for row in array]


def read_categories(categories_filepath):
    if Path(categories_filepath).exists():
        categories_file = open(categories_filepath, 'r')
    else:
        raise FileNotFoundError(categories_filepath)
    
    categories = categories_file.readline()
    categories_file.close()
    return categories.split(',')[:-1] # last comma means -1 entry is ''


def add_category(categories_filepath, category):
    if Path(categories_filepath).exists():
        categories_file = open(categories_filepath, 'a')
    else:
        raise FileNotFoundError(categories_filepath)
    
    if category[-1] != ',':
        category += ','
        
    categories_file.write(category)
    categories_file.close()


def date_to_iso(date, add_year=False):
    ''' MM/DD/YYYY --> YYYY-MM-DD '''
    date = date.split('/')
    date = [date[2], date[0], date[1]]
    if add_year:
        date[0] = str(datetime.date.today())[0:2] + date[0]
    return '-'.join(date)


def last_day_of_month(day: datetime.date) -> int:
    next_month = day.replace(day=28) + datetime.timedelta(days=4)
    return (next_month - datetime.timedelta(days=next_month.day)).day


def input_month_to_number(month: str) -> int:
    month = month.lower()
    if month in ['january', 'jan', '1']:
        return 1
    elif month in ['february', 'feb', '2']:
        return 2
    elif month in ['march', 'mar', '3']:
        return 3
    elif month in ['april', 'apr', '4']:
        return 4
    elif month in ['may', '5']:
        return 5
    elif month in ['june', 'jun', '6']:
        return 6
    elif month in ['july', 'jul', '7']:
        return 7
    elif month in ['august', 'aug', '8']:
        return 8
    elif month in ['september', 'sep', '9']:
        return 9
    elif month in ['october', 'oct', '10']:
        return 10
    elif month in ['november', 'nov', '11']:
        return 11
    elif month in ['december', 'dec', '12']:
        return 12
    else:
        raise ValueError(f'In input_month_to_number(), month "{month}" is  not recognized!')


category_options = ['Income',
                    'Rent & Utilities',
                    'Transportation',
                    'Groceries',
                    'Eating Out',
                    'Subscriptions',
                    'Clothing',
                    'Personal',
                    'Hobbies']
