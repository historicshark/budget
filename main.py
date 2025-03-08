#!/home/historicshark/Documents/budget/venv_budget/bin/python

import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import easygui

from database import DatabaseManager
from import_csv import import_file
from categorize import categorize_manual

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('command', help=main_commands_help())
    parser.add_argument('rest', nargs='*')
    args = parser.parse_args()

    db = DatabaseManager('transactions')

    match args.command:
        case 'import':
            data = import_file(args.rest)
            data = categorize_manual(data)
            db.insert(array=data)
            db.select_and_print()


    return


def main_commands_help():
    return '''Available commands:
    import'''

if __name__ == '__main__':
    main()