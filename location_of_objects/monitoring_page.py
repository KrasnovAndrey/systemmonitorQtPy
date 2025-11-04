from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea, QWidget
from PyQt6.QtCore import QTimer
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomCard, CustomButton
import psutil


class MonitoringWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sort_by = "cpu"
        self.prev_proc_io = {}
        self.setup_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def setup_ui(self):
        layout = QVBoxLayout()

        stats_layout = QHBoxLayout()
        self.cpu_card = CustomCard("ЦП", "0%")
        self.memory_card = CustomCard("Память", "0%")
        self.processes_card = CustomCard("Процессы", "0")
        self.disk_card = CustomCard("Диск I/O", "0 MB/s")

        stats_layout.addWidget(self.cpu_card)
        stats_layout.addWidget(self.memory_card)
        stats_layout.addWidget(self.processes_card)
        stats_layout.addWidget(self.disk_card)

        buttons_layout = QHBoxLayout()
        cpu_btn = CustomButton("По ЦП", min_height=35)
        memory_btn = CustomButton("По ОЗУ", min_height=35)
        disk_btn = CustomButton("По диску", min_height=35)
        net_btn = CustomButton("По сети", min_height=35)

        cpu_btn.clicked.connect(lambda: self.change_sort("cpu"))
        memory_btn.clicked.connect(lambda: self.change_sort("memory"))
        disk_btn.clicked.connect(lambda: self.change_sort("disk"))
        net_btn.clicked.connect(lambda: self.change_sort("network"))

        buttons_layout.addWidget(cpu_btn)
        buttons_layout.addWidget(memory_btn)
        buttons_layout.addWidget(disk_btn)
        buttons_layout.addWidget(net_btn)
        buttons_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        self.processes_widget = QWidget()
        self.processes_layout = QVBoxLayout()
        self.processes_widget.setLayout(self.processes_layout)
        scroll.setWidget(self.processes_widget)

        layout.addLayout(stats_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(scroll)
        self.setLayout(layout)

    def change_sort(self, sort_type):
        self.sort_by = sort_type

    def update_data(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        process_count = len(psutil.pids())

        try:
            disk_io = psutil.disk_io_counters()
            if hasattr(self, "prev_disk_read"):
                read_speed = (disk_io.read_bytes - self.prev_disk_read) / (
                    1024 * 1024 * 2
                )
                disk_text = f"{read_speed:.1f} MB/s"
            else:
                disk_text = "0 MB/s"
            self.prev_disk_read = disk_io.read_bytes
        except:
            disk_text = "N/A"

        self.cpu_card.update_value(f"{cpu_percent:.1f}%")
        self.memory_card.update_value(f"{memory.percent:.1f}%")
        self.processes_card.update_value(str(process_count))
        self.disk_card.update_value(disk_text)

        for i in reversed(range(self.processes_layout.count())):
            self.processes_layout.itemAt(i).widget().setParent(None)

        processes = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(
                    attrs=["pid", "name", "cpu_percent", "memory_percent"]
                )

                try:
                    io_counters = proc.io_counters()
                    current_io = io_counters.read_bytes + io_counters.write_bytes

                    if pinfo["pid"] in self.prev_proc_io:
                        io_diff = current_io - self.prev_proc_io[pinfo["pid"]]
                        pinfo["disk_usage"] = max(0, io_diff / 1024)
                    else:
                        pinfo["disk_usage"] = 0

                    self.prev_proc_io[pinfo["pid"]] = current_io
                except:
                    pinfo["disk_usage"] = 0

                try:
                    connections = proc.connections()
                    pinfo["network_usage"] = len(connections)
                except:
                    pinfo["network_usage"] = 0

                processes.append(pinfo)
            except:
                continue

        if self.sort_by == "cpu":
            processes.sort(key=lambda x: x["cpu_percent"] or 0, reverse=True)
        elif self.sort_by == "memory":
            processes.sort(key=lambda x: x["memory_percent"] or 0, reverse=True)
        elif self.sort_by == "disk":
            processes.sort(key=lambda x: x["disk_usage"], reverse=True)
        elif self.sort_by == "network":
            processes.sort(key=lambda x: x["network_usage"], reverse=True)

        for proc in processes[:15]:
            proc_text = f"PID: {proc['pid']} | {proc['name']} | CPU: {proc['cpu_percent'] or 0:.1f}% | RAM: {proc['memory_percent'] or 0:.1f}% | Диск: {proc['disk_usage']:.1f}KB/s | Сеть: {proc['network_usage']}"
            proc_label = CustomLabel(proc_text)
            self.processes_layout.addWidget(proc_label)


def create_monitoring():
    panel = CustomPanel("Мониторинг системы", margins=(30, 25, 30, 25), spacing=20)
    monitoring_widget = MonitoringWidget()
    panel.add_widget(monitoring_widget)
    return panel
