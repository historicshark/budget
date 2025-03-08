import pandas as pd

# in: df with Date, Location, Amount
# out: df with Date, Location, Amount, Category
def categorize_manual(data: pd.DataFrame):
    options = ['Income',
               'Rent & Utilities',
               'Transportation',
               'Groceries',
               'Eating Out',
               'Subscriptions',
               'Clothing',
               'Personal',
               'Hobbies']

    options_print = ' | '.join([f'{option}: {number+1}' for number, option in enumerate(options)])

    categories = []

    for row, date, location, amount in data.itertuples(name=None):
        print(f'Categorize transaction {location} on {date} for amount {amount}')
        print(f'Categories are:\n{options_print}')

        keepgoing = True
        while keepgoing:
            option = int(input('>>> '))
            if option > 0 and option <= len(options):
                categories.append(options[option-1])
                keepgoing = False
            elif option == 0:
                raise Exception('quit')

    data.insert(3, 'Category', categories)
    return data