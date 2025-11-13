from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomButton
from database import SystemDatabase
import subprocess
import platform
import csv
import os
import psutil
import time


class ScanWorker(QThread):
    scan_complete = pyqtSignal(list)

    def __init__(self, scan_type):
        super().__init__()
        self.scan_type = scan_type

    def load_template(self, filename):
        services = []
        try:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(script_dir, "templates", filename)
            with open(template_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["required"].lower() == "true":
                        services.append(row["service_name"])
        except Exception as e:
            services.append(f"Ошибка загрузки шаблона: {str(e)}")
        return services

    def run(self):
        results = []
        system = platform.system().lower()

        if self.scan_type == "services":
            if system == "linux":
                services = self.load_template("linux_services.csv")
                for service in services:
                    try:
                        result = subprocess.run(
                            ["systemctl", "is-active", service],
                            capture_output=True,
                            text=True,
                        )
                        status = (
                            "Работает"
                            if result.stdout.strip() == "active"
                            else "Не работает"
                        )
                        results.append(f"{service}: {status}")
                    except:
                        results.append(f"{service}: Ошибка")

            elif system == "windows":
                services = self.load_template("windows_services.csv")
                for service in services:
                    try:
                        result = subprocess.run(
                            ["sc", "query", service], capture_output=True, text=True
                        )
                        status = (
                            "Работает" if "RUNNING" in result.stdout else "Не работает"
                        )
                        results.append(f"{service}: {status}")
                    except:
                        results.append(f"{service}: Ошибка")
            else:
                results.append("Система не поддерживается")
                return

        elif self.scan_type == "health":
            try:
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                if system == "windows":
                    disk = psutil.disk_usage("C:\\")
                else:
                    disk = psutil.disk_usage("/")
                boot_time = psutil.boot_time()
                uptime_seconds = time.time() - boot_time
                uptime_hours = int(uptime_seconds // 3600)

                results.append(
                    f"ЦП: {cpu:.1f}% {'Норма' if cpu < 80 else 'Высокая нагрузка'}"
                )
                results.append(
                    f"Память: {memory.percent:.1f}% {'Норма' if memory.percent < 85 else 'Мало памяти'}"
                )
                results.append(
                    f"Диск: {disk.percent:.1f}% {'Норма' if disk.percent < 90 else 'Мало места'}"
                )

                results.append(f"Время работы: {uptime_hours}ч ")

                swap = psutil.swap_memory()
                results.append(
                    f"Своп (вирт. память): {swap.percent:.1f}% {'Норма' if swap.percent < 50 else 'Активно используется'}"
                )

                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            for entry in entries:
                                if entry.current:
                                    temp_status = (
                                        "Норма" if entry.current < 75 else "Высокая"
                                    )
                                    results.append(
                                        f"Температура: {entry.current:.1f}°C {temp_status}"
                                    )
                                    break
                            break
                    else:
                        results.append("Температура: Недоступно")
                except:
                    results.append("Температура: Недоступно")

                if system != "windows":
                    try:
                        cpu_count = psutil.cpu_count(logical=False)
                        load_avg = os.getloadavg()
                        load_status = "Норма" if load_avg[0] < cpu_count else "Высокая"
                        results.append(
                            f"Коэф. нагрузки: {load_avg[0]:.2f}/{cpu_count} {load_status}"
                        )
                    except:
                        results.append("Коэф. нагрузки: Недоступно")

            except:
                results.append("Ошибка проверки системы")

        self.scan_complete.emit(results)


class ScanWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()
        self.services_btn = CustomButton("Проверить службы", min_height=40)
        self.health_btn = CustomButton("Проверить систему", min_height=40)

        self.services_btn.clicked.connect(lambda: self.start_scan("services"))
        self.health_btn.clicked.connect(lambda: self.start_scan("health"))

        buttons_layout.addWidget(self.services_btn)
        buttons_layout.addWidget(self.health_btn)

        self.status_label = CustomLabel("Выберите тип сканирования")

        layout.addLayout(buttons_layout)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def start_scan(self, scan_type):
        self.last_scan_type = scan_type
        self.services_btn.setEnabled(False)
        self.health_btn.setEnabled(False)
        self.status_label.setText("Сканирование...")

        self.worker = ScanWorker(scan_type)
        self.worker.scan_complete.connect(self.show_results)
        self.worker.start()

    def show_results(self, results):
        result_text = "Результаты сканирования:\n\n" + "\n".join(results)
        self.status_label.setText(result_text)
        self.services_btn.setEnabled(True)
        self.health_btn.setEnabled(True)

        if hasattr(self, "last_scan_type") and self.last_scan_type == "health":
            try:
                db = SystemDatabase()
                db.save_health_scan()
                print("Сканирование здоровья сохранено")
            except:
                pass


def create_scan_system():
    panel = CustomPanel("Сканирование системы", margins=(30, 25, 30, 25), spacing=20)
    scan_widget = ScanWidget()
    panel.add_widget(scan_widget)
    return panel
