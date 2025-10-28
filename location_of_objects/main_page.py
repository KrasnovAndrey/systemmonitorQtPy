from PyQt6.QtWidgets import QHBoxLayout, QWidget
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomCard, CustomSidebar


class MainPage:
    def __init__(self):
        self.widget = QWidget()
        self.setup_page()

    def setup_page(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = CustomSidebar(width=280, margins=(5, 30, 5, 30), spacing=12)
        sidebar.add_button("Главная")
        sidebar.add_button("Система")
        sidebar.add_button("Мониторинг")
        sidebar.add_button("Управление")
        sidebar.add_button("Визуализация")
        sidebar.add_button("Настройки")
        sidebar.add_stretch()
        sidebar.set_active_button(0)

        content_panel = CustomPanel(
            "Добро пожаловать в System Monitor", margins=(30, 25, 30, 25), spacing=20
        )

        description = CustomLabel(
            "Программа для мониторинга и управления системой.\n\n"
            "Основные возможности:\n"
            " Сбор информации об устройстве\n"
            " Мониторинг служб и процессов\n"
            " Управление компонентами системы\n"
            " Визуализация системных параметров\n"
            " Экспорт и импорт конфигураций\n\n"
        )

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(15, 15, 15, 15)

        cpu_card = CustomCard(
            "ЦП", "45%", padding=22, spacing=8
        )  # Тут вместо этого значения будет вставляться переменная с актуаальным значением.
        memory_card = CustomCard(
            "Память", "8.2 GB", padding=22, spacing=8
        )  # Тут вместо этого значения будет вставляться переменная с актуаальным значением.
        disk_card = CustomCard(
            "Диск", "256 GB", padding=22, spacing=8
        )  # Тут вместо этого значения будет вставляться переменная с актуаальным значением.
        network_card = CustomCard(
            "Сеть", "125 MB/s", padding=22, spacing=8
        )  # Тут вместо этого значения будет вставляться переменная с актуаальным значением.

        cards_layout.addWidget(cpu_card)
        cards_layout.addWidget(memory_card)
        cards_layout.addWidget(disk_card)
        cards_layout.addWidget(network_card)

        content_panel.add_widget(description)
        content_panel.add_layout(cards_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_panel)

        self.widget.setLayout(main_layout)

    def get_widget(self):
        return self.widget
