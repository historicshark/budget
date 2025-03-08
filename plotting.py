import pandas as pd
import matplotlib.pyplot as plt
import numpy as  np

from database import DatabaseManager

def plot_main(args, db: DatabaseManager):
    plot_pie_by_category(args, db)

    plt.show()
    return


def plot_pie_by_category(args, db):
    #TODO: date range
    categories, totals = db.totals_by_category()

    expenses = [[],[]]
    income = [[],[]]

    for category, total in zip(categories, totals):
        if total < 0:
            expenses[0].append(category)
            expenses[1].append(-total)
        else:
            income[0].append(category)
            income[1].append(total)

    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_size_inches(12, 4)

    ax1.pie(income[1], labels=income[0])
    ax1.set_title('Income')
    ax1.set_xlabel(f'Total = ${np.sum(income[1])}')

    ax2.pie(expenses[1], labels=[f'{name}: ${value:.2f}' for name, value in zip(expenses[0], expenses[1])])
    ax2.set_title('Expenses')
    ax2.set_xlabel(f'Total = ${np.sum(expenses[1])}')
    return
