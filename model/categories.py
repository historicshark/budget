from collections.abc import Sequence
import json
from pathlib import Path

class Categories(Sequence):
    def __init__(self):
        self.rules_file = 'model/category_rules.json'
        self.categories_file = 'model/categories.json'

        self.rules = self.load_category_rules()
        self.categories = self.load_categories()

    def __getitem__(self, i):
        return self.categories[i]

    def __len__(self):
        return len(self.categories)

    def load_category_rules(self) -> dict[str, str]:
        """
        Load json file containing category rules of {"keyword": "category"}
        """
        if Path(self.rules_file).exists():
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        else:
            print(f'Attempted to load rules file {self.rules_file}, but it doesn\'t exist. No rules are loaded!')
            return {}

    def dump_category_rules(self) -> None:
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
        return

    # Load json file containing a list of categories
    def load_categories(self) -> list[str]:
        if Path(self.categories_file).exists():
            with open(self.categories_file, 'r') as f:
                category_options = json.load(f)
            return category_options
        else:
            raise FileNotFoundError(self.categories_file)

    def dump_categories(self) -> None:
        print('dumping categories!')
        with open(self.categories_file, 'w') as f:
            json.dump(self.categories, f, indent=2)
        return
 
    def add_new_category(self, new_category: str) -> None:
        if new_category in self.categories:
            raise ValueError(f'Category {new_category} already exists!')

        self.categories.append(new_category)
        self.dump_categories()
        return

    def add_new_category_rule(self, keyword: str, category: str) -> None:
        self.rules[keyword.lower()] = category
        self.categories.dump_category_rules()
        return

