from PyQt6.QtWidgets import QHBoxLayout, QWidget, QStackedWidget
from widgets.custom_widgets import CustomSidebar
from location_of_objects.dashboard import create_dashboard
from location_of_objects.system_page import create_system
from location_of_objects.monitoring_page import create_monitoring
from location_of_objects.control_page import create_control
from location_of_objects.visualization_page import create_visualization
from location_of_objects.settings_page import create_settings


class MainPage:
    def __init__(self):
        self.widget = QWidget()
        self.pages = QStackedWidget()
        self.sidebar = None
        self.setup_page()

    def setup_page(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = CustomSidebar(width=280, margins=(5, 30, 5, 30), spacing=12)

        btn1 = self.sidebar.add_button("Главная")
        btn2 = self.sidebar.add_button("Система")
        btn3 = self.sidebar.add_button("Мониторинг")
        btn4 = self.sidebar.add_button("Управление")
        btn5 = self.sidebar.add_button("Визуализация")
        btn6 = self.sidebar.add_button("Настройки")

        btn1.clicked.connect(lambda: self.change_page(0))
        btn2.clicked.connect(lambda: self.change_page(1))
        btn3.clicked.connect(lambda: self.change_page(2))
        btn4.clicked.connect(lambda: self.change_page(3))
        btn5.clicked.connect(lambda: self.change_page(4))
        btn6.clicked.connect(lambda: self.change_page(5))

        self.sidebar.add_stretch()
        self.sidebar.set_active_button(0)

        self.pages.addWidget(create_dashboard())
        self.pages.addWidget(create_system())
        self.pages.addWidget(create_monitoring())
        self.pages.addWidget(create_control())
        self.pages.addWidget(create_visualization())
        self.pages.addWidget(create_settings())

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)
        self.widget.setLayout(layout)

    def change_page(self, index):
        self.pages.setCurrentIndex(index)
        self.sidebar.set_active_button(index)

    def get_widget(self):
        return self.widget
