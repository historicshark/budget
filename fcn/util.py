import datetime
from pathlib import Path

def column(array, i):
    return [row[i] for row in array]


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

