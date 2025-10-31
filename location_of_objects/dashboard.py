from PyQt6.QtWidgets import QHBoxLayout
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomCard
import psutil


def create_dashboard():
    panel = CustomPanel(
        "Добро пожаловать в System Monitor", margins=(30, 25, 30, 25), spacing=20
    )

    desc = CustomLabel(
        "Программа для мониторинга и управления системой.\n\n"
        "Основные возможности:\n"
        " Сбор информации об устройстве\n"
        " Мониторинг служб и процессов\n"
        " Управление компонентами системы\n"
        " Визуализация системных параметров\n"
        " Экспорт и импорт конфигураций\n\n"
    )

    cards = QHBoxLayout()
    cards.setSpacing(20)
    cards.setContentsMargins(15, 15, 15, 15)

    cpu_percent = f"{psutil.cpu_percent(interval=1):.1f}%"
    mem = psutil.virtual_memory()
    mem_used = f"{mem.used / (1024**3):.1f} GB"
    disk = psutil.disk_usage("/")
    disk_used = f"{disk.used / (1024**3):.0f} GB"

    cpu_card = CustomCard("ЦП", cpu_percent, padding=22, spacing=8)
    mem_card = CustomCard("Память", mem_used, padding=22, spacing=8)
    disk_card = CustomCard("Диск", disk_used, padding=22, spacing=8)
    net_card = CustomCard("Сеть", "Активна", padding=22, spacing=8)

    cards.addWidget(cpu_card)
    cards.addWidget(mem_card)
    cards.addWidget(disk_card)
    cards.addWidget(net_card)

    panel.add_widget(desc)
    panel.add_layout(cards)
    return panel
