from enum import IntEnum
import json
from pathlib import Path


with open('ui/colors.json', 'r') as f:
    COLORS = json.load(f)

class SCREENS(IntEnum):
    HOME = 0,
    IMPORT = 1

