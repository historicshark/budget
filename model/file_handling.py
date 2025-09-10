import sys
from pathlib import Path
import os

def is_app_frozen():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_asset_path(relative_path) -> Path:
    if is_app_frozen():
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path.cwd()

    return base_path / relative_path

def get_data_path(file_name) -> Path:
    if is_app_frozen():
        app_name = 'budget_program'
        if os.name == 'nt':
            data_dir = Path.home() / 'Documents' / app_name
        else:
            data_dir = Path.home() / app_name
    else:
        data_dir = Path.cwd() / 'data'

    data_dir.mkdir(exist_ok=True)
    return data_dir / file_name
