#!/usr/bin/env python3

import argparse

from database import DatabaseManager
from import_csv import import_file
from categorize import categorize_manual
from plotting import plot_main
from list_transactions import list_main

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
            # db.select_and_print()

        case 'plot':
            plot_main(args.rest, db)

        case 'list':
            list_main(args.rest, db)

    return


def main_commands_help():
    return '''Available commands:
    import
    plot
    list'''

if __name__ == '__main__':
    main()
