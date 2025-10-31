from widgets.custom_widgets import CustomPanel, CustomLabel


def create_monitoring():
    panel = CustomPanel("Мониторинг системы", margins=(30, 25, 30, 25), spacing=20)
    info = CustomLabel("Здесь будет мониторинг процессов и служб")
    panel.add_widget(info)
    return panel
