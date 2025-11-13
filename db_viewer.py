from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QTabWidget
from PyQt6.QtCore import Qt
from widgets.custom_widgets import CustomLabel
from database import SystemDatabase


def create_db_viewer():
    widget = QWidget()
    widget.setStyleSheet("QWidget { background-color: transparent; }")
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    
    tabs = QTabWidget()
    tabs.setStyleSheet("""
        QTabWidget::pane {
            border: 2px solid #3498db;
            border-radius: 8px;
            background-color: #34495e;
        }
        QTabBar::tab {
            background-color: #2c3e50;
            color: #bdc3c7;
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar::tab:selected {
            background-color: #3498db;
            color: white;
        }
        QTabBar::tab:hover {
            background-color: #34495e;
            color: #ecf0f1;
        }
    """)

    logs_tab = create_logs_tab()
    health_tab = create_health_tab()

    tabs.addTab(logs_tab, "Логи системы")
    tabs.addTab(health_tab, "Сканирования")

    layout.addWidget(tabs)
    widget.setLayout(layout)
    return widget


def create_logs_tab():
    widget = QWidget()
    widget.setStyleSheet("QWidget { background-color: transparent; }")
    layout = QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { 
            border: none; 
            background-color: transparent; 
        }
        QScrollBar:vertical {
            background-color: #2c3e50;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #3498db;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #5dade2;
        }
    """)

    content_widget = QWidget()
    content_widget.setStyleSheet("QWidget { background-color: transparent; }")
    content_layout = QVBoxLayout()
    content_layout.setSpacing(8)

    try:
        db = SystemDatabase()
        logs = db.get_all_logs()

        if logs:
            for log in logs:
                try:
                    log_text = f"{str(log[1])[:16]} | CPU: {float(log[2]):.1f}% | Память: {float(log[3]):.1f}% | Диск: {float(log[4]):.1f}% | Своп: {float(log[5]):.1f}% | Время: {log[6]}ч | Темп: {float(log[7]):.1f}°C"
                    label = CustomLabel(log_text)
                    content_layout.addWidget(label)
                except Exception as e:
                    content_layout.addWidget(CustomLabel(f"Ошибка записи: {str(e)}"))
        else:
            content_layout.addWidget(CustomLabel("Нет данных"))
    except Exception as e:
        content_layout.addWidget(CustomLabel(f"Ошибка загрузки: {str(e)}"))

    content_widget.setLayout(content_layout)
    scroll.setWidget(content_widget)
    layout.addWidget(scroll)
    widget.setLayout(layout)
    return widget


def create_health_tab():
    widget = QWidget()
    widget.setStyleSheet("QWidget { background-color: transparent; }")
    layout = QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { 
            border: none; 
            background-color: transparent; 
        }
        QScrollBar:vertical {
            background-color: #2c3e50;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #3498db;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #5dade2;
        }
    """)

    content_widget = QWidget()
    content_widget.setStyleSheet("QWidget { background-color: transparent; }")
    content_layout = QVBoxLayout()
    content_layout.setSpacing(8)

    try:
        db = SystemDatabase()
        scans = db.get_all_health_scans()

        if scans:
            for scan in scans:
                scan_text = f"{scan[1][:16]} | CPU: {scan[2]} | Память: {scan[3]} | Диск: {scan[4]} | Своп: {scan[5]} | Темп: {scan[6]} | Время: {scan[7]}ч"
                label = CustomLabel(scan_text)
                content_layout.addWidget(label)
        else:
            content_layout.addWidget(CustomLabel("Нет данных"))
    except Exception as e:
        content_layout.addWidget(CustomLabel(f"Ошибка загрузки: {str(e)}"))

    content_widget.setLayout(content_layout)
    scroll.setWidget(content_widget)
    layout.addWidget(scroll)
    widget.setLayout(layout)
    return widget
