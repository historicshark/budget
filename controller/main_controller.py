from model import *
from view import *
from controller import *

class MainController:
    def __init__(self):
        self.db = DatabaseManager('transactions')
        self.categories = Categories()
        self.importer = Importer(self.db)

        self.main_window = MainWindow()
        self.screens = {
            'home': HomeScreen(),
            'import': ImportScreen(),
            'categorize': CategorizeScreen(),
            'add_new_rule': AddNewRuleScreen(),
            'import_complete': ImportCompleteScreen(),
            'filter': FilterScreen(),
            'expenses': ExpensesScreen(),
            'list': ListScreen(),
            'edit_record': EditRecordScreen(),
            'create_record': CreateRecordScreen(),
            'add_new_category': AddNewCategoryScreen(),
            'edit_categories': EditCategoriesScreen(),
            'edit_budget': EditBudgetScreen(),
        }
        self.screen_indexes = {}
        self.register_screens()

        self.controllers = {
            'import': ImportController(self, self.screens['import'], self.importer),
            'categorize': CategorizeController(self, self.screens['categorize'], self.screens['add_new_rule'], self.screens['import_complete'], self.importer, self.categories),
            'filter': FilterController(self, self.screens['filter'], self.db, self.categories),
            'expenses': ExpensesController(self, self.screens['expenses'], self.db),
            'list': ListController(self, self.screens['list'], self.db),
            'edit_record': EditRecordController(self, self.screens['edit_record'], self.db, self.categories),
            'create_record': CreateRecordController(self, self.screens['create_record'], self.db, self.categories),
            'add_new_category': AddNewCategoryController(self, self.screens['add_new_category'], self.categories),
            'edit_categories': EditCategoriesController(self, self.screens['edit_categories'], self.db, self.categories),
        }

        # connections
        self.screens['home'].import_clicked.connect(self.start_import)
        self.screens['home'].expenses_clicked.connect(self.start_expenses)
        self.screens['home'].list_clicked.connect(self.start_list)
        self.screens['home'].create_clicked.connect(self.start_create_record)
        self.screens['home'].categories_clicked.connect(lambda: self.go_to_screen('edit_categories'))
        self.screens['home'].edit_budget_clicked.connect(lambda: self.go_to_screen('edit_budget'))

    def register_screens(self):
        for name, screen in self.screens.items():
            self.main_window.stack.addWidget(screen)
            self.screen_indexes[name] = self.main_window.stack.indexOf(screen)

            if hasattr(screen, 'home_clicked'):
                screen.home_clicked.connect(lambda: self.go_to_screen('home'))
    
    def debug(self):
        self.go_to_screen('edit_categories')

    def start(self):
        self.main_window.show()
        self.categories.categories_updated.emit()
        self.go_to_screen('home')
        #self.debug() #XXX debug

    def go_to_screen(self, name):
        if name in self.screens.keys():
            #print(f'go to {name}') XXX debug
            self.main_window.stack.setCurrentIndex(self.screen_indexes[name])
        else:
            print(f'screen {name} not implemented')

    def start_import(self):
        self.go_to_screen('import')
        self.controllers['add_new_category'].connect_continue_cancel(self.add_new_category_continue_to_categorize_screen,
                                                                     self.add_new_category_cancel_to_categorize_screen)

    def import_to_categorize_screen(self):
        self.go_to_screen('categorize')
        self.controllers['categorize'].start()

    def reset_import_process(self):
        self.controllers['import'].reset()
        self.controllers['categorize'].reset()

    def start_expenses(self):
        self.go_to_screen('filter')
        self.controllers['filter'].connect_continue_cancel(self.set_records_and_go_to_expenses_screen,
                                                           lambda: self.go_to_screen('home'))
        self.screens['expenses'].load_widgets()

    def start_list(self):
        self.go_to_screen('filter')
        self.controllers['filter'].connect_continue_cancel(self.set_records_and_go_to_list_screen,
                                                           lambda: self.go_to_screen('home'))

        self.controllers['add_new_category'].connect_continue_cancel(self.add_new_category_continue_to_edit_record_screen,
                                                                     self.add_new_category_cancel_to_edit_record_screen)

    def start_create_record(self):
        self.go_to_screen('create_record')
        self.controllers['add_new_category'].connect_continue_cancel(self.add_new_category_continue_to_create_record_screen,
                                                                     self.add_new_category_cancel_to_create_record_screen)

    def set_records_and_go_to_expenses_screen(self):
        self.controllers['expenses'].records = self.controllers['filter'].records
        self.go_to_screen('expenses')
        self.controllers['expenses'].update_views()

    def set_records_and_go_to_list_screen(self):
        self.controllers['list'].records = self.controllers['filter'].records
        self.controllers['list'].sort_records_by_date()
        self.controllers['list'].update_table()
        self.go_to_screen('list')

    def list_screen_to_edit_record_screen(self, records_to_edit: list[Record]):
        self.controllers['edit_record'].records_to_edit = records_to_edit
        self.controllers['edit_record'].display_record()
        self.go_to_screen('edit_record')

    def go_to_add_new_category_screen(self, record):
        self.controllers['add_new_category'].display_record(record)
        self.go_to_screen('add_new_category')

    def add_new_category_continue_to_categorize_screen(self, new_category):
        self.controllers['categorize'].on_new_category_added(new_category)
        self.go_to_screen('categorize')

    def add_new_category_cancel_to_categorize_screen(self):
        self.controllers['categorize'].guess_category()
        self.go_to_screen('categorize')

    def add_new_category_continue_to_edit_record_screen(self, new_category):
        self.controllers['edit_record'].on_new_category_added(new_category)
        self.go_to_screen('edit_record')

    def add_new_category_cancel_to_edit_record_screen(self):
        self.controllers['edit_record'].display_record()
        self.go_to_screen('edit_record')

    def add_new_category_continue_to_create_record_screen(self, new_category):
        self.controllers['create_record'].on_new_category_added(new_category)
        self.go_to_screen('create_record')

    def add_new_category_cancel_to_create_record_screen(self):
        self.controllers['create_record'].reset_category_dropdown()
        self.go_to_screen('create_record')

    def update_records_in_list_controller_screen(self):
        """ after updating or deleting records from the list, use the filters to get the
        updated records from the database """
        self.controllers['list'].records = self.db.select_filter(self.controllers['filter'].filter)
        self.controllers['list'].sort_records(self.screens['list'].drop_down.currentText())

    def print_records(self):
        records = self.controllers['filter'].records
        self.db.print_records(records)
