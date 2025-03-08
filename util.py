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