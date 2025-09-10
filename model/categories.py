from PyQt5.QtCore import pyqtSignal, QObject

from collections.abc import Sequence
import json
from pathlib import Path
from model.file_handling import get_data_path

class Categories(QObject):
    categories_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.rules_file = get_data_path('category_rules.json')
        self.categories_file = get_data_path('categories.json')

        self.rules = self.load_category_rules()
        self.categories = self.load_categories()

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
        default_categories = ['Rent', 'Income', 'Groceries', 'Transportation', 'Other']
        self.categories = default_categories
        self.dump_categories()
        return default_categories

    # Load json file containing a list of categories
    def load_categories(self) -> list[str]:
        if self.categories_file.exists():
            with open(self.categories_file, 'r') as f:
                category_options = json.load(f)
            return category_options
        else:
            return self.create_categories_file()

    def dump_categories(self) -> None:
        #print('dumping categories!')
        with open(self.categories_file, 'w') as f:
            json.dump(self.categories, f, indent=2)
   
    def guess_category(self, location: str) -> str:
        location = location.lower()
        for keyword in self.rules.keys():
            if keyword in location:
                return self.rules[keyword]
        return self.categories[0]
 
    def add_new_category(self, new_category: str) -> None:
        if new_category in self.categories:
            raise ValueError(f'Category {new_category} already exists!')

        self.categories.append(new_category)
        self.dump_categories()
        self.categories_updated.emit()

    def remove_category(self, category: str):
        self.categories.remove(category)
        self.dump_categories()
        self.categories_updated.emit()

    def update_category(self, old_category: str, new_category: str):
        i = self.categories.index(old_category)
        self.categories[i] = new_category
        self.dump_categories()
        self.categories_updated.emit()

    def add_new_category_rule(self, keyword: str, category: str) -> None:
        self.rules[keyword.lower()] = category
        self.dump_category_rules()
