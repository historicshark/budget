import json

with open('view/colors.json', 'r') as f:
    colors = json.load(f)

default_style_sheet = f'''
QLabel {{
font-family: Monaco;
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
font-family: Monaco;
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
font-family: Monaco;
font-size: 16px;
color: {colors['fg']};
}}
'''
