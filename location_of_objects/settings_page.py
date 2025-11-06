from PyQt6.QtWidgets import QSlider, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomButton


def set_brightness(value):
    pass


def set_volume(value):
    pass


def toggle_wifi(enabled):
    pass


def toggle_bluetooth(enabled):
    pass


def sleep_mode():
    pass


def restart_system():
    pass


def shutdown_system():
    pass


def open_autostart_page():
    pass


def create_settings():
    panel = CustomPanel("Управление")

    brightness_layout = QHBoxLayout()
    brightness_layout.addWidget(CustomLabel("Яркость"))
    brightness_slider = QSlider(Qt.Orientation.Horizontal)
    brightness_slider.setRange(0, 100)
    brightness_slider.setValue(50)
    brightness_slider.valueChanged.connect(set_brightness)
    brightness_layout.addWidget(brightness_slider)

    volume_layout = QHBoxLayout()
    volume_layout.addWidget(CustomLabel("Громкость"))
    volume_slider = QSlider(Qt.Orientation.Horizontal)
    volume_slider.setRange(0, 100)
    volume_slider.setValue(75)
    volume_slider.valueChanged.connect(set_volume)
    volume_layout.addWidget(volume_slider)

    panel.add_layout(brightness_layout)
    panel.add_layout(volume_layout)

    wifi_check = QCheckBox("WiFi")
    wifi_check.setChecked(True)
    wifi_check.toggled.connect(toggle_wifi)
    bluetooth_check = QCheckBox("Bluetooth")
    bluetooth_check.toggled.connect(toggle_bluetooth)

    panel.add_widget(wifi_check)
    panel.add_widget(bluetooth_check)

    autostart_btn = CustomButton("Управление автозагрузкой")
    autostart_btn.clicked.connect(open_autostart_page)

    sleep_btn = CustomButton("Спящий режим")
    sleep_btn.clicked.connect(sleep_mode)

    restart_btn = CustomButton("Перезагрузка")
    restart_btn.clicked.connect(restart_system)

    shutdown_btn = CustomButton("Выключение")
    shutdown_btn.clicked.connect(shutdown_system)

    panel.add_widget(autostart_btn)
    panel.add_widget(sleep_btn)
    panel.add_widget(restart_btn)
    panel.add_widget(shutdown_btn)

    return panel
