from view import colors

default_style_sheet = f'''
QWidget {{
font-family: Monaco;
}}

QLabel {{
font-size: 18px;
color: {colors['fg']};
}}

QLabel#title {{
font-size: 25px;
margin: 10px;
}}

QLabel#footer {{
background-color: {colors['fg']};
color: {colors['bg']};
font-size: 14px;
padding: 3px;
}}

QPushButton {{
font-size: 18px;
background-color: {colors['gray']};
color: {colors['bg']};
}}

QPushButton:hover {{
background-color: {colors['purple-faded']};
color: {colors['fg']};
}}

QPushButton:disabled {{
background-color: {colors['bg1']};
color: {colors['gray']};
}}

QPushButton#home {{
font-size: 14px;
}}
QPushButton#home:hover {{
background-color: {colors['aqua-faded']};
}}

QRadioButton {{
font-size: 16px;
color: {colors['fg']};
}}

QLineEdit {{
font-size: 18px;
color: {colors['fg0']};
background-color: {colors['bg1']};
padding: 2px;
}}

QComboBox {{
font-size: 15px;
color: {colors['fg0']};
background-color: {colors['bg1']};
padding: 3px;
border: 0px solid {colors['bg']};
selection-background-color: {colors['purple-faded']};
}}

QComboBox::drop-down {{
color: {colors['fg']};
background-color: {colors['purple-faded']};
subcontrol-origin: padding;
subcontrol-position: right;
width: 0px;
}}

QComboBox:hover {{
background-color: {colors['purple-faded']};
color: {colors['fg']};
}}

QComboBox QAbstractItemView {{
background-color: {colors['bg1']};
color: {colors['fg0']};
}}

QComboBox QAbstractItemView::item:hover {{
background-color: {colors['bg2']};
color: {colors['fg0']};
}}

QSpinBox, QDoubleSpinBox {{
font-size: 15px;
color: {colors['fg0']};
background-color: {colors['bg1']};
padding: 3px;
border: 0px solid {colors['bg']};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
subcontrol-origin: border;
subcontrol-position: top right;
}}

QSpinBox::down-button, QDoubleSpinBox::down-button {{
subcontrol-origin: border;
subcontrol-position: bottom right;
}}

QDateEdit {{
font-size: 15px;
color: {colors['fg0']};
background-color: {colors['bg1']};
padding: 3px;
border: 0px solid {colors['bg']};
}}

/* This stops hover from working when focused
QDateEdit:focus {{
background-color: {colors['bg1']};
color: {colors['fg0']};
}}
*/

QDateEdit::drop-down {{
image: url(assets/pencil-square.svg);
background-color: {colors['purple']};
subcontrol-origin: padding;
subcontrol-position: right;
width: 30px;
}}

/* Annoying since it doesn't work if you move the mouse from the box to the button
QDateEdit::drop-down:hover {{
background-color: {colors['purple-faded']};
color: {colors['fg']};
}}
*/

/* not using down arrow
QDateEdit::down-arrow {{
width: 10px;
height: 8px;
}}
*/

QCalendarWidget QWidget {{
background-color: {colors['bg1']};
color: {colors['fg0']};
}}

/* top row buttons */
/*
QCalendarWidget QToolButton {{
background-color: {colors['bg1']};
color: {colors['fg']};
}}
*/

/* table of dates
QCalendarWidget QTableView {{
background-color: {colors['bg1']};
color: {colors['fg']};
}}
*/

QCalendarWidget QSpinBox {{
background-color: {colors['bg']};
color: {colors['fg']};
}}

QCalendarWidget QSpinBox::up-button {{
subcontrol-origin: border;
subcontrol-position: top right;
width: 20px;
}}

QCalendarWidget QSpinBox::down-button {{
subcontrol-origin: border;
subcontrol-position: bottom right;
width: 20px;
}}

QCheckBox {{
font-size: 15px;
color: {colors['fg']};
background-color: {colors['bg']};
spacing: 8px;
}}

QCheckBox::indicator {{
width: 15px;
height: 15px;
}}

QCheckBox::indicator:unchecked {{
border: 2px solid {colors['gray']};
background-color: {colors['bg1']};
border-radius: 3px;
}}

QCheckBox::indicator:checked {{
border: 2px solid {colors['gray']};
background-color: {colors['aqua']};
border-radius: 3px;
}}

QTableWidget {{
background-color: {colors['bg1']};
alternate-background-color: {colors['bg2']};
color: {colors['fg']};
selection-background-color: {colors['blue-faded']};
selection-color: {colors['fg']};
gridline-color: {colors['gray']};
border: 1px solid {colors['gray']};
}}

QHeaderView::section {{
background-color: {colors['bg2']};
color: {colors['fg']};
border: 0px solid white;
font-weight: bold;
}}
'''
