from widgets.custom_widgets import CustomPanel, CustomLabel


def create_settings():
    panel = CustomPanel("Настройки", margins=(30, 25, 30, 25), spacing=20)
    info = CustomLabel("Здесь будут настройки")
    panel.add_widget(info)
    return panel
