from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QComboBox,
    QLabel,
    QSpinBox,
    QCheckBox,
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QKeySequence
from view.widgets.date_edit_fix import DateEditFix
from view.widgets.combo_box_fix import ComboBoxFix

import datetime

class DateFilter(QWidget):
    stateChanged = pyqtSignal(Qt.CheckState)
    date_range_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = ['last month', 'last 3 months', 'last 6 months', 'last year', 'range', 'one month', 'all time']
        self.date_range = [datetime.date.today()] * 2
        self.set_range_last_n_months(1)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # header with checkbox label and drop down menu
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)

        self.check_box = QCheckBox('Date:')
        self.check_box.setChecked(True)
        self.check_box.stateChanged.connect(lambda state: self.stateChanged.emit(state))

        self.menu = ComboBoxFix()
        self.menu.addItems(self.options)
        self.menu.setFixedWidth(200)
        self.menu.view().setMinimumWidth(206)
        self.menu.setCurrentIndex(0)
        self.menu.currentTextChanged.connect(self.on_menu_item_selected)

        self.header_layout.addWidget(self.check_box)
        self.header_layout.addSpacing(10)
        self.header_layout.addWidget(self.menu)
        self.header_layout.addStretch()
        self.main_layout.addLayout(self.header_layout)

        # date range widgets
        self.date_range_widget = QWidget()
        date_range_layout = QGridLayout()
        date_range_layout.setHorizontalSpacing(30)
        date_range_layout.setVerticalSpacing(5)
        date_range_layout.setContentsMargins(20, 5, 20, 20)

        from_label = QLabel('From:')
        to_label = QLabel('To:')
        from_label.setStyleSheet('font-size: 15px;')
        to_label.setStyleSheet('font-size: 15px;')

        self.from_date = DateEditFix()
        self.to_date = DateEditFix()
        self.from_date.setFixedWidth(120)
        self.to_date.setFixedWidth(120)
        self.from_date.setDate(QDate().fromString(str(self.date_range[0]), Qt.ISODate))
        self.to_date.setDate(QDate().fromString(str(self.date_range[1]), Qt.ISODate))
        self.set_date_limits()
        self.from_date.dateChanged.connect(self.on_date_range_changed)
        self.to_date.dateChanged.connect(self.on_date_range_changed)

        date_range_layout.addWidget(from_label, 0, 0, Qt.AlignLeft)
        date_range_layout.addWidget(to_label, 0, 1)
        date_range_layout.addWidget(self.from_date, 1, 0)
        date_range_layout.addWidget(self.to_date, 1, 1)

        date_range_layout.setColumnStretch(2, 1)

        self.date_range_widget.setLayout(date_range_layout)
        self.main_layout.addWidget(self.date_range_widget)
        self.date_range_widget.hide()

        # one month widget
        self.one_month_widget = QWidget()
        one_month_layout = QGridLayout()
        one_month_layout.setHorizontalSpacing(30)
        one_month_layout.setVerticalSpacing(5)
        one_month_layout.setContentsMargins(20, 5, 20, 10)

        month_label = QLabel('Month:')
        year_label = QLabel('Year:')
        month_label.setStyleSheet('font-size: 15px;')
        year_label.setStyleSheet('font-size: 15px;')

        self.month_box = ComboBoxFix()
        self.month_box.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        self.month_box.setCurrentIndex(datetime.date.today().month-1)
        self.month_box.setFixedWidth(150)
        self.month_box.currentIndexChanged.connect(self.on_month_selected)

        self.year_box = QSpinBox()
        self.year_box.setMinimum(2000)
        self.year_box.setMaximum(datetime.date.today().year)
        self.year_box.setFixedWidth(75)
        self.year_box.setValue(datetime.date.today().year)
        self.year_box.valueChanged.connect(self.on_month_selected)

        one_month_layout.addWidget(month_label, 0, 0, Qt.AlignLeft)
        one_month_layout.addWidget(year_label, 0, 1)
        one_month_layout.addWidget(self.month_box, 1, 0)
        one_month_layout.addWidget(self.year_box, 1, 1)
        one_month_layout.setColumnStretch(2, 1)

        self.one_month_widget.setLayout(one_month_layout)
        self.main_layout.addWidget(self.one_month_widget)
        self.one_month_widget.hide()

        self.setLayout(self.main_layout)

    def on_menu_item_selected(self, option):
        self.date_range_widget.hide()
        self.one_month_widget.hide()
        match option:
            case 'last month':
                self.set_range_last_n_months(1)

            case 'last 3 months':
                self.set_range_last_n_months(3)

            case 'last 6 months':
                self.set_range_last_n_months(6)

            case 'last year':
                self.set_range_last_n_months(12)

            case 'range':
                self.date_range_widget.show()
                self.on_date_range_changed()

            case 'one month':
                self.one_month_widget.show()
                self.on_month_selected()

            case 'all time':
                self.date_range[0] = datetime.date.today().replace(year=datetime.MINYEAR)
                self.date_range[1] = datetime.date.today()
                self.date_range_changed.emit(self.date_range)

    def set_date_limits(self):
        self.from_date.setMaximumDate(self.to_date.date())
        self.to_date.setMinimumDate(self.from_date.date())

    def on_date_range_changed(self):
        self.set_date_limits()
        self.date_range[0] = self.from_date.date().toPyDate()
        self.date_range[1] = self.to_date.date().toPyDate()
        self.date_range_changed.emit(self.date_range)

    def on_month_selected(self):
        self.date_range[0] = datetime.date(self.year_box.value(),
                                           self.month_box.currentIndex()+1,
                                           1)
        self.date_range[1] = self.date_range[0].replace(day=self.last_day_of_month(self.date_range[0]))
        self.date_range_changed.emit(self.date_range)

    def set_range_last_n_months(self, n_months: int):
        assert n_months > 0
        self.date_range[1] = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        self.date_range[0] = self.date_range[1]
        for month in range(n_months):
            self.date_range[0] = self.date_range[0].replace(day=1) - datetime.timedelta(days=1)
        self.date_range[0] += datetime.timedelta(days=1)
        self.date_range_changed.emit(self.date_range)

    def last_day_of_month(self, day: datetime.date) -> int:
        next_month = day.replace(day=28) + datetime.timedelta(days=4)
        return (next_month - datetime.timedelta(days=next_month.day)).day

    def reset(self):
        self.date_range = [datetime.date.today()] * 2
        self.set_range_last_n_months(1)
        
        self.check_box.setChecked(True)
        self.menu.setCurrentIndex(0)

        self.from_date.setDate(QDate().fromString(str(self.date_range[0]), Qt.ISODate))
        self.to_date.setDate(QDate().fromString(str(self.date_range[1]), Qt.ISODate))
        self.set_date_limits()

        self.month_box.setCurrentIndex(datetime.date.today().month-1)
        self.year_box.setValue(datetime.date.today().year)

