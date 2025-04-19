import json
import pandas as pd
from pathlib import Path


RULES_FILE = 'category_rules.json'
CATEGORIES_FILE = 'categories.json'

# in: df with Date, Location, Amount
# out: df with Date, Location, Amount, Category
def categorize_manual(data: pd.DataFrame) -> pd.DataFrame:
    category_options, options_print = load_categories()
    rules = load_category_rules()

    categories = []

    for row, date, location, amount in data.itertuples(name=None):
        guessed_category = guess_category(location, rules)
        print(f'Categorize transaction {location} on {date} for amount {amount}')
        print(f'''This was guessed to be {guessed_category}. Leave blank to accept this category. Options are:
0: quit
{options_print}
{len(category_options)+1}: Add a new cateogry''')

        while True:
            option = input('>>> ')

            if not option: # Accept guessed category
                categories.append(guessed_category)
                break
            else: # A number was entered
                try:
                    option = int(option)
                except:
                    print('Enter a valid number')
                    continue

                if option < 0 or option > len(category_options) + 1:
                    print('Enter a valid number')
                    continue
                elif option == 0:
                    raise Exception('quit')
                elif option == len(category_options) + 1:
                    add_new_category(category_options)
                    category_options, options_print = load_categories()
                    break
                else:
                    category = category_options[option-1]

                    if category != guessed_category:
                        add_new_category_rule(location, category, rules)
                        
                    categories.append(category_options[option-1])
                    break

    data.insert(3, 'Category', categories)
    return data


def load_category_rules() -> dict:
    if Path(RULES_FILE).exists():
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    else:
        print(f'Attempted to load rules file {file}, but it doesn\'t exist. No rules are loaded!')
        return {}


def dump_category_rules(rules: dict) -> None:
    with open(RULES_FILE, 'w') as f:
        json.dump(rules, f, indent=2)
    return


def load_categories() -> tuple[list[str], str]:
    if Path(CATEGORIES_FILE).exists():
        with open(CATEGORIES_FILE, 'r') as f:
            category_options = json.load(f)
        options_print = '\n'.join([f'{number+1}: {option}' for number, option in enumerate(category_options)])
        return category_options, options_print
    else:
        raise FileNotFoundError(CATEGORIES_FILE)


def dump_categories(categories: list[str]) -> None:
    print('dumping categories!')
    with open(CATEGORIES_FILE, 'w') as f:
        json.dump(categories, f, indent=2)
    return


def add_new_category_rule(location: str, category: str, rules: dict) -> None:
    value = input('Add a new category rule? [Y/n] >>> ')
    if not value or 'y' in value.lower():
        keyword = input('Enter keyword for this rule. Leave blank for full location. (c to cancel)\n>>> ')

        if keyword.lower() == 'c':
            return

        if not keyword:
            keyword = location

        rules[keyword.lower()] = category

        dump_category_rules(rules)
    return


def guess_category(location: str, rules: dict[str,str]) -> str:
    location = location.lower()

    for keyword in rules.keys():
        if keyword in location:
            return rules[keyword]

    return 'Unknown'


def add_new_category(category_options: list[str]) -> None:
    while True:
        new_category = input('Enter new category >>> ')
        confirm = input(f'Confirm new category {new_category}? [Y/n] >>> ')
        if not confirm or 'y' in confirm.lower() and (new_category not in category_options):
            category_options.append(new_category)
            dump_categories(category_options)
            return

