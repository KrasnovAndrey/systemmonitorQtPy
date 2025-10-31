from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from widgets.custom_widgets import CustomPanel, CustomLabel
from widgets.simple_chart import CPUChart, MemoryChart, DiskChart


def create_visualization():
    panel = CustomPanel("Визуализация", margins=(30, 25, 30, 25), spacing=20)

    tabs = QTabWidget()
    tabs.setStyleSheet(
        """
        QTabWidget::pane {
            border: 1px solid #3498db;
            background-color: #2c3e50;
        }
        QTabBar::tab {
            background-color: #34495e;
            color: #ecf0f1;
            padding: 8px 16px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #3498db;
        }
    """
    )

    cpu_widget = QWidget()
    cpu_layout = QVBoxLayout()
    cpu_chart = CPUChart()
    cpu_layout.addWidget(cpu_chart)
    cpu_widget.setLayout(cpu_layout)
    tabs.addTab(cpu_widget, "ЦП")

    mem_widget = QWidget()
    mem_layout = QVBoxLayout()
    mem_chart = MemoryChart()
    mem_layout.addWidget(mem_chart)
    mem_widget.setLayout(mem_layout)
    tabs.addTab(mem_widget, "Память")

    disk_widget = QWidget()
    disk_layout = QVBoxLayout()
    disk_chart = DiskChart()
    disk_layout.addWidget(disk_chart)
    disk_widget.setLayout(disk_layout)
    tabs.addTab(disk_widget, "Диск")

    panel.add_widget(tabs)
    return panel
