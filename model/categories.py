from PyQt5.QtCore import pyqtSignal, QObject

from collections.abc import Sequence
import json
from model.file_handling import get_data_path

class Categories(QObject):
    categories_updated = pyqtSignal()
    amounts_updated = pyqtSignal()
    available_types: dict[str, int] = {'income': 1, 'expense': -1, 'savings': -1}

    def __init__(self):
        super().__init__()
        self.rules_file = get_data_path('category_rules.json')
        self.categories_file = get_data_path('categories.json')

        self.categories: list[str] = []
        self.types: list[str] = []
        self.amounts: list[float] = []

        self.rules = self.load_category_rules()
        self.load_categories()

    def __getitem__(self, i):
        return self.categories[i]

    def __len__(self):
        return len(self.categories)

    def __contains__(self, o):
        return self.categories.__contains__(o)

    def __iter__(self):
        return self.categories.__iter__()

    def __reversed__(self):
        return self.categories.__reversed__()

    def index(self, value, start=0, stop=None):
        return self.categories.index(value, start, stop)

    def count(self, value):
        return self.categories.count(value)
    
    def items(self):
        return zip(self.categories, self.types, self.amounts)

    def load_category_rules(self) -> dict[str, str]:
        """
        Load json file containing category rules of {"keyword": "category"}
        """
        if self.rules_file.exists():
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        else:
            print(f'Attempted to load rules file {self.rules_file}, but it doesn\'t exist. No rules are loaded!')
            return {}

    def dump_category_rules(self) -> None:
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)

    def create_categories_file(self):
        self.categories = ['Rent', 'Income', 'Groceries', 'Transportation', 'Other']
        self.types = ['expense', 'income', 'expense', 'expense', 'expense']
        self.amounts = [0.0 for x in default_categories]
        self.dump_categories()

    def load_categories(self) -> None:
        self.categories.clear()
        self.types.clear()
        self.amounts.clear()

        if self.categories_file.exists():
            with open(self.categories_file, 'r') as f:
                file = json.load(f)
                for category, (category_type, budget) in file.items():
                    self.categories.append(category)
                    self.types.append(category_type)
                    self.amounts.append(budget)
        else:
            self.create_categories_file()

    def dump_categories(self) -> None:
        #print('dumping categories!')
        with open(self.categories_file, 'w') as f:
            output = {c: (t, a) for c, t, a in zip(self.categories, self.types, self.amounts)}
            json.dump(output, f, indent=2)
   
    def guess_category(self, location: str) -> str:
        location = location.lower()
        for keyword in self.rules:
            if keyword in location:
                return self.rules[keyword]
        return self.categories[0]
 
    def add_new_category(self, new_category: str, new_type: str, new_amount=0.0) -> None:
        if new_category in self.categories:
            raise ValueError(f'Category {new_category} already exists!')
        assert new_type in self.available_types

        self.categories.append(new_category)
        self.types.append(new_type)
        self.amounts.append(new_amount)

        self.dump_categories()
        self.categories_updated.emit()

    def remove_category(self, category: str):
        i = self.categories.index(category)
        self.categories.pop(i)
        self.types.pop(i)
        self.amounts.pop(i)

        self.dump_categories()
        self.categories_updated.emit()

    def update_category(self, old_category: str, new_category: str, new_type: str):
        assert new_type in self.available_types

        i = self.categories.index(old_category)
        self.categories[i] = new_category
        self.types[i] = new_type

        self.dump_categories()
        self.categories_updated.emit()

    def update_amount(self, category: str, new_amount: float):
        i = self.categories.index(category)
        self.amounts[i] = new_amount

        self.dump_categories()
        self.amounts_updated.emit()

    def update_amounts(self, new_amounts: list[float]):
        self.amounts = new_amounts.copy()
        self.dump_categories()
        self.amounts_updated.emit()

    def add_new_category_rule(self, keyword: str, category: str) -> None:
        self.rules[keyword.lower()] = category
        self.dump_category_rules()
