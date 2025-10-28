from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QMainWindow,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal


class CustomButton(QPushButton):
    def __init__(self, text="", min_height=45, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(min_height)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2980b9;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #21618c;
                transform: translateY(0px);
            }
        """
        )


class SidebarButton(QPushButton):
    clicked_signal = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(55)
        self.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                color: #bdc3c7;
                border: none;
                border-left: 3px solid transparent;
                padding: 16px 20px;
                text-align: left;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.15);
                color: #ecf0f1;
                border-left: 3px solid #3498db;
            }
        """
        )
        self.clicked.connect(self.clicked_signal.emit)


class CustomSidebar(QWidget):
    tab_changed = pyqtSignal(int)

    def __init__(self, width=260, margins=(0, 25, 0, 25), spacing=8, parent=None):
        super().__init__(parent)
        self.setFixedWidth(width)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)

        title = QLabel("System Monitor")
        title.setStyleSheet(
            """
            QLabel {
                color: #ecf0f1;
                font-size: 20px;
                font-weight: 700;
                padding: 25px 20px;
                text-align: center;
                border-bottom: 2px solid #34495e;
                margin-bottom: 20px;
            }
        """
        )

        self.buttons = []
        self.layout = layout

        layout.addWidget(title)

        version = QLabel("v0.0.1")
        version.setStyleSheet(
            """
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                padding: 15px 20px;
                text-align: center;
                border-top: 1px solid #34495e;
            }
        """
        )
        layout.addWidget(version)

        self.setLayout(layout)

    def add_button(self, text):
        btn = SidebarButton(text)
        index = len(self.buttons)
        btn.clicked_signal.connect(lambda: self.tab_changed.emit(index))
        self.buttons.append(btn)
        self.layout.insertWidget(self.layout.count() - 2, btn)
        return btn

    def add_stretch(self):
        self.layout.addStretch()

    def add_version(self, version_text="v0.0.1"):
        version = QLabel(version_text)
        version.setStyleSheet(
            """
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                padding: 15px 20px;
                text-align: center;
                border-top: 1px solid #34495e;
            }
        """
        )
        self.layout.addWidget(version)

    def set_active_button(self, index):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: rgba(52, 152, 219, 0.2);
                        color: #3498db;
                        border: none;
                        border-left: 3px solid #3498db;
                        padding: 16px 20px;
                        text-align: left;
                        font-size: 15px;
                        font-weight: 600;
                    }
                """
                )
            else:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background: transparent;
                        color: #bdc3c7;
                        border: none;
                        border-left: 3px solid transparent;
                        padding: 16px 20px;
                        text-align: left;
                        font-size: 15px;
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: rgba(52, 152, 219, 0.15);
                        color: #ecf0f1;
                        border-left: 3px solid #3498db;
                    }
                """
                )


class CustomPanel(QWidget):
    def __init__(self, title="", margins=(25, 20, 25, 20), spacing=18, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin: 8px;
            }
        """
        )

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(*margins)
        self.layout.setSpacing(spacing)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet(
                """
                QLabel {
                    color: #ecf0f1;
                    font-size: 20px;
                    font-weight: 700;
                    padding-bottom: 12px;
                    border-bottom: 2px solid #3498db;
                    margin-bottom: 15px;
                }
            """
            )
            self.layout.addWidget(self.title_label)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(12)
        self.layout.addLayout(self.content_layout)
        self.setLayout(self.layout)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)


class CustomCard(QFrame):
    def __init__(self, title="", value="", padding=18, spacing=6, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #3498db;
                border: none;
                border-radius: 10px;
                padding: {padding}px;
            }}
            QFrame:hover {{
                background-color: #5dade2;
                transform: translateY(-2px);
            }}
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(spacing)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 4px;
                padding: 4px 8px;
            }
        """
        )

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: 700;
                margin-top: 6px;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
            }
        """
        )

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        self.setLayout(layout)

    def update_value(self, value):
        self.value_label.setText(value)


class CustomWindow(QMainWindow):
    def __init__(self, title="Application", width=1000, height=700, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(width, height)
        self.center_window()
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QStackedWidget {
                background-color: transparent;
                border-left: 2px solid #34495e;
            }
        """
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.central_widget.setLayout(self.main_layout)

    def center_window(self):
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        )

    def add_widget(self, widget):
        self.main_layout.addWidget(widget)

    def add_layout(self, layout):
        self.main_layout.addLayout(layout)


class CustomLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            """
            QLabel {
                color: #e2e8f0;
                font-size: 15px;
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-weight: 500;
                line-height: 1.7;
                padding: 12px 8px;
                background-color: rgba(52, 73, 94, 0.3);
                border-radius: 8px;
                margin: 5px 0px;
            }
        """
        )
        self.setWordWrap(True)
