import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from widgets.custom_widgets import CustomWindow
from location_of_objects.main import MainPage


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = CustomWindow("System Monitor", 1200, 700)
        self.setup_ui()

    def setup_ui(self):
        main_page = MainPage()
        self.window.add_widget(main_page.get_widget())

    def run(self):
        self.window.show()
        return self.app.exec()


if __name__ == "__main__":
    app = App()
    sys.exit(app.run())
