from PyQt5.QtCore import QObject

from view import EditCategoriesScreen
from model import DatabaseManager, Categories, Record

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class EditCategoriesController(QObject):
    def __init__(self, main: 'MainController', edit_categories_screen: EditCategoriesScreen, db: DatabaseManager, categories: Categories):
        super().__init__()

        self.main = main
        self.edit_categories_screen = edit_categories_screen
        self.db = db
        self.categories = categories

        # wiring
        self.edit_categories_screen.continue_clicked.connect(self.on_continue_clicked)
        self.edit_categories_screen.cancel_clicked.connect(self.on_cancel_clicked)
        self.edit_categories_screen.delete_clicked.connect(self.on_delete_clicked)

        self.categories.categories_updated.connect(self.update_category_options)

    def on_continue_clicked(self, category_changes: list[tuple[str, str, str]]):
        # Check that no text boxes are empty or contain wrong characters
        for old_category, new_category, old_type, new_type in category_changes:
            if not new_category:
                self.edit_categories_screen.show_warning('Error: Category names cannot be empty!')
                return
            if any(char in new_category for char in ['"', "'"]):
                self.edit_categories_screen.show_warning('Error: Category names cannot contain quotes!')
                return

        # Update records in database and add to categories
        for old_category, new_category, old_type, new_type in category_changes:
            if old_category == 'New Category':
                self.categories.add_new_category(new_category, new_type)

            elif old_category != new_category:
                self.db.update(old_category=old_category, new_category=new_category)
                self.categories.update_category(old_category, new_category, new_type)

            elif old_type != new_type:
                self.categories.update_category(old_category, new_category, new_type)

    def on_cancel_clicked(self):
        self.update_category_options()
        self.main.go_to_screen('home')

    def on_delete_clicked(self, selected_categories: list[str]):
        # Don't delete categories that are in use
        for category in selected_categories:
            if len(self.db.select(category=category)) > 0:
                self.edit_categories_screen.show_warning(f'Cannot delete category {category}! It is used by existing transactions in the database!')
                return

        for category in selected_categories:
            self.categories.remove_category(category)

    def update_category_options(self):
        self.edit_categories_screen.update_category_options(self.categories,
                                                            self.categories.types,
                                                            self.categories.available_types)
