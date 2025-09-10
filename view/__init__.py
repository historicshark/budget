import json

with open('view/colors.json', 'r') as f:
    colors = json.load(f)
from .default_style_sheet import default_style_sheet

from .base_screen import BaseScreen
from .main_window import MainWindow
from .home_screen import HomeScreen
from .import_screen import ImportScreen
from .categorize_screen import CategorizeScreen
from .add_new_rule_screen import AddNewRuleScreen
from .import_complete_screen import ImportCompleteScreen
from .filter_screen import FilterScreen
from .expenses_screen import ExpensesScreen
from .list_screen import ListScreen
from .edit_record_screen import EditRecordScreen
from .create_record_screen import CreateRecordScreen
from .add_new_category_screen import AddNewCategoryScreen
from .edit_categories_screen import EditCategoriesScreen

__all__ = [
    'MainWindow',
    'HomeScreen',
    'ImportScreen',
    'CategorizeScreen',
    'AddNewRuleScreen',
    'ImportCompleteScreen',
    'FilterScreen',
    'ExpensesScreen',
    'ListScreen',
    'EditRecordScreen',
    'CreateRecordScreen',
    'AddNewCategoryScreen',
    'EditCategoriesScreen',
]
