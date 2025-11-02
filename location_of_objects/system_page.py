from PyQt6.QtWidgets import QHBoxLayout
from widgets.custom_widgets import CustomPanel, CustomLabel, CustomCard
import psutil
import platform
import subprocess
import socket
import datetime


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Недоступен"


def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}ч {minutes}м"
    except:
        return "Недоступно"


def get_cpu_name():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":")[1].strip()
    except:
        pass

    try:
        result = subprocess.run(["lscpu"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Model name:" in line:
                return line.split(":")[1].strip()
    except:
        pass

    try:
        result = subprocess.run(
            ["wmic", "cpu", "get", "name"], capture_output=True, text=True
        )
        lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
        if len(lines) > 1:
            return lines[1]
    except:
        pass

    return platform.processor() or "Неизвестно"


def get_gpus():
    gpus = []

    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "VGA" in line or "Display" in line or "3D" in line:
                gpu_name = line.split(": ")[-1]
                if gpu_name and gpu_name not in gpus:
                    gpus.append(gpu_name)
    except:
        pass

    if not gpus:
        try:
            result = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get", "name"],
                capture_output=True,
                text=True,
            )
            lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
            for line in lines[1:]:
                if line and line not in gpus:
                    gpus.append(line)
        except:
            pass

    return gpus if gpus else ["Информация недоступна"]


def create_system():
    panel = CustomPanel("Информация о системе", margins=(30, 25, 30, 25), spacing=20)

    cpu_name = get_cpu_name()
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()
    mem_total = f"{mem.total / (1024**3):.1f} GB"

    ip_addr = get_ip()
    uptime = get_uptime()
    boot_time = psutil.boot_time()
    boot_time_str = datetime.datetime.fromtimestamp(boot_time).strftime(
        "%d.%m.%Y %H:%M"
    )

    gpus = get_gpus()

    cards = QHBoxLayout()
    cards.setSpacing(20)
    cards.setContentsMargins(15, 15, 15, 15)

    cpu_card = CustomCard("Процессор", f"{cores} ядер", padding=22, spacing=8)
    mem_card = CustomCard("ОЗУ", mem_total, padding=22, spacing=8)
    ip_card = CustomCard("IP адрес", ip_addr, padding=22, spacing=8)
    uptime_card = CustomCard("Время работы", uptime, padding=22, spacing=8)

    cards.addWidget(cpu_card)
    cards.addWidget(mem_card)
    cards.addWidget(ip_card)
    cards.addWidget(uptime_card)

    gpu_list = "\n".join([f"  - {gpu}" for gpu in gpus])

    details = f"""Процессор: {cpu_name}
Ядра: {cores} физических, {threads} логических
Оперативная память: {mem_total}

Видеокарты ({len(gpus)} шт.):
{gpu_list}

ОС: {platform.system()} {platform.release()}
Архитектура: {platform.architecture()[0]}
IP адрес: {ip_addr}
Время работы: {uptime}
Запущен: {boot_time_str}
Имя компьютера: {platform.node()}"""

    info = CustomLabel(details)

    panel.add_layout(cards)
    panel.add_widget(info)
    return panel
