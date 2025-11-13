import sqlite3
import psutil
from datetime import datetime
import platform
import time
import os
from PyQt6.QtCore import QTimer


class SystemDatabase:
    def __init__(self):
        self.data_dir = self._get_data_dir()
        self.db_file = os.path.join(self.data_dir, "system_data.db")
        self._setup_tables()
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_save)
        self.timer.start(60000)

    def _get_data_dir(self):
        if platform.system() == "Windows":
            data_dir = os.path.join(os.environ.get("APPDATA", ""), "SystemMonitor")
        else:
            data_dir = os.path.join(os.path.expanduser("~"), ".systemmonitor")

        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    def _setup_tables(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute(
            """CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            swap_usage REAL,
            uptime_hours INTEGER,
            temperature REAL
        )"""
        )

        c.execute("DROP TABLE IF EXISTS system_info")
        c.execute(
            """CREATE TABLE system_info (
            id INTEGER PRIMARY KEY,
            os_name TEXT,
            os_version TEXT,
            cpu_model TEXT,
            cpu_cores_physical INTEGER,
            cpu_cores_logical INTEGER,
            memory_total REAL,
            disk_total REAL,
            ip_address TEXT,
            gpu_info TEXT,
            boot_time TEXT,
            last_updated TEXT
        )"""
        )

        c.execute(
            """CREATE TABLE IF NOT EXISTS health_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_status TEXT,
            memory_status TEXT,
            disk_status TEXT,
            swap_status TEXT,
            temp_status TEXT,
            uptime_hours INTEGER
        )"""
        )

        conn.commit()
        conn.close()

    def save_stats(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        swap = psutil.swap_memory()

        boot_time = psutil.boot_time()
        uptime_hours = int((time.time() - boot_time) // 3600)

        temp = 0
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current:
                            temp = entry.current
                            break
                    break
        except:
            pass

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(
            """INSERT INTO system_logs 
                    (timestamp, cpu_usage, memory_usage, disk_usage, swap_usage, uptime_hours, temperature) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().isoformat(),
                cpu,
                mem.percent,
                disk.percent,
                swap.percent,
                uptime_hours,
                temp,
            ),
        )
        conn.commit()
        conn.close()

    def save_info(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM system_info")

        cpu_info = platform.processor() or "Unknown"
        mem_total = psutil.virtual_memory().total / (1024**3)
        disk_total = psutil.disk_usage("/").total / (1024**3)
        boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()

        try:
            import socket

            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except:
            ip = "Unknown"

        gpu_info = "Unknown"
        try:
            import subprocess

            if platform.system().lower() == "linux":
                gpu_result = subprocess.run(
                    ["lspci", "-nn"], capture_output=True, text=True
                )
                gpu_lines = [
                    line
                    for line in gpu_result.stdout.split("\n")
                    if "VGA" in line or "Display" in line
                ]
                if gpu_lines:
                    gpu_info = (
                        gpu_lines[0].split(":")[2].strip()
                        if ":" in gpu_lines[0]
                        else "Unknown"
                    )
        except:
            pass

        c.execute(
            """INSERT INTO system_info 
                    (id, os_name, os_version, cpu_model, cpu_cores_physical, cpu_cores_logical, 
                     memory_total, disk_total, ip_address, gpu_info, boot_time, last_updated) 
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                platform.system(),
                platform.release(),
                cpu_info,
                psutil.cpu_count(logical=False),
                psutil.cpu_count(),
                mem_total,
                disk_total,
                ip,
                gpu_info,
                boot_time,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def get_logs_count(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM system_logs")
        count = c.fetchone()[0]
        conn.close()
        return count

    def get_info(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM system_info WHERE id = 1")
        data = c.fetchone()
        conn.close()
        return data

    def save_health_scan(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        swap = psutil.swap_memory()

        boot_time = psutil.boot_time()
        uptime_hours = int((time.time() - boot_time) // 3600)

        cpu_status = "Норма" if cpu < 80 else "Высокая нагрузка"
        mem_status = "Норма" if mem.percent < 85 else "Мало памяти"
        disk_status = "Норма" if disk.percent < 90 else "Мало места"
        swap_status = "Норма" if swap.percent < 50 else "Активно используется"

        temp_status = "Недоступно"
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current:
                            temp_status = "Норма" if entry.current < 75 else "Высокая"
                            break
                    break
        except:
            pass

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(
            """INSERT INTO health_scans 
                    (timestamp, cpu_status, memory_status, disk_status, swap_status, temp_status, uptime_hours) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().isoformat(),
                cpu_status,
                mem_status,
                disk_status,
                swap_status,
                temp_status,
                uptime_hours,
            ),
        )
        conn.commit()
        conn.close()

    def get_health_count(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM health_scans")
        count = c.fetchone()[0]
        conn.close()
        return count

    def get_last_health_scan(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM health_scans ORDER BY timestamp DESC LIMIT 1")
        data = c.fetchone()
        conn.close()
        return data

    def get_all_logs(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM system_logs ORDER BY timestamp DESC")
        data = c.fetchall()
        conn.close()
        return data

    def get_all_health_scans(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM health_scans ORDER BY timestamp DESC")
        data = c.fetchall()
        conn.close()
        return data

    def clear_logs(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM system_logs")
        before_logs = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM health_scans")
        before_health = c.fetchone()[0]

        c.execute("DELETE FROM system_logs")
        c.execute("DELETE FROM health_scans")

        conn.commit()
        conn.close()
        return before_logs + before_health

    def auto_save(self):
        try:
            self.save_stats()
            self.save_info()
        except:
            pass
