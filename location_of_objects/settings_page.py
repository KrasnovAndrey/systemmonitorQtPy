from PyQt6.QtWidgets import QSlider, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomButton
import subprocess
import os
import platform

system = platform.system().lower()
prev_volume = 50

def set_brightness(value):
    try:
        if system == "windows":
            subprocess.run(["powershell", "-Command", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{value})"], shell=True)
        else:
            brightness = value / 100.0
            subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", str(brightness)], shell=True)
    except:
        pass


def volume_up():
    try:
        if system == "windows":
            import keyboard
            keyboard.send("volume up")
        else:
            subprocess.run(["amixer", "set", "Master", "5%+"], shell=True)
    except:
        pass


def volume_down():
    try:
        if system == "windows":
            import keyboard
            keyboard.send("volume down")
        else:
            subprocess.run(["amixer", "set", "Master", "5%-"], shell=True)
    except:
        pass


def toggle_wifi(enabled):
    pass


def toggle_bluetooth(enabled):
    pass


def sleep_mode():
    try:
        if system == "windows":
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=True)
        else:
            subprocess.run(["systemctl", "suspend"], shell=True)
    except:
        pass


def restart_system():
    try:
        if system == "windows":
            subprocess.run(["shutdown", "/r", "/t", "0"], shell=True)
        else:
            subprocess.run(["shutdown", "-r", "now"], shell=True)
    except:
        pass


def shutdown_system():
    try:
        if system == "windows":
            subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)
        else:
            subprocess.run(["shutdown", "-h", "now"], shell=True)
    except:
        pass


def open_autostart_page():
    try:
        if system == "windows":
            subprocess.run(["msconfig"], shell=True)
        else:
            subprocess.run(["nautilus", os.path.expanduser("~/.config/autostart/")], shell=True)
    except:
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
    volume_down_btn = CustomButton("-", min_height=35)
    volume_up_btn = CustomButton("+", min_height=35)
    volume_down_btn.clicked.connect(volume_down)
    volume_up_btn.clicked.connect(volume_up)
    volume_layout.addWidget(volume_down_btn)
    volume_layout.addWidget(volume_up_btn)

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
