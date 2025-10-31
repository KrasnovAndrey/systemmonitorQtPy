from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt
import psutil
import collections


class SimpleLineChart(QWidget):
    def __init__(self, title="График", max_points=50):
        super().__init__()
        self.title = title
        self.max_points = max_points
        self.data = collections.deque(maxlen=max_points)
        self.setMinimumHeight(200)

        for _ in range(max_points):
            self.data.append(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.darkGray))

        painter.setPen(QPen(Qt.GlobalColor.gray, 1))
        width = self.width()
        height = self.height()

        for i in range(0, height, 20):
            painter.drawLine(0, i, width, i)
        if len(self.data) > 1:
            painter.setPen(QPen(Qt.GlobalColor.cyan, 2))
            points = list(self.data)

            for i in range(len(points) - 1):
                x1 = int(i * width / len(points))
                y1 = int(height - (points[i] * height / 100))
                x2 = int((i + 1) * width / len(points))
                y2 = int(height - (points[i + 1] * height / 100))
                painter.drawLine(x1, y1, x2, y2)


class CPUChart(SimpleLineChart):
    def __init__(self):
        super().__init__("Загрузка ЦП (%)")

    def update_data(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        self.data.append(cpu_percent)
        self.update()


class MemoryChart(SimpleLineChart):
    def __init__(self):
        super().__init__("Использование памяти (%)")

    def update_data(self):
        mem = psutil.virtual_memory()
        self.data.append(mem.percent)
        self.update()


class DiskChart(SimpleLineChart):
    def __init__(self):
        super().__init__("Активность диска")

    def update_data(self):
        disk_io = psutil.disk_io_counters()
        if hasattr(self, "prev_read"):
            read_diff = disk_io.read_bytes - self.prev_read
            activity = min(100, read_diff / (1024 * 1024))
            self.data.append(activity)
        else:
            self.data.append(0)

        self.prev_read = disk_io.read_bytes
        self.update()
