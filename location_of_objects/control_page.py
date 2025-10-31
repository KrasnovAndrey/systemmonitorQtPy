from widgets.custom_widgets import CustomPanel, CustomLabel


def create_control():
    panel = CustomPanel("Управление системой", margins=(30, 25, 30, 25), spacing=20)
    info = CustomLabel("Здесь будет панель управления")
    panel.add_widget(info)
    return panel
