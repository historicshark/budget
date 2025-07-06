from PyQt5.QtCore import QObject

from view import PlotScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class PlotController(QObject):
    def __init__(self, main: "MainController", plot_screen: PlotScreen):
        super().__init__()
